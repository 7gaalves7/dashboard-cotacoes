import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# ---------------------------------------------------------
# Configuração da Página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Financeiro | Cotações ao Vivo",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Funções de Dados (ETL)
# ---------------------------------------------------------
# ---------------------------------------------------------
# Funções de Dados (ETL) - Versão Corrigida para a Nuvem
# ---------------------------------------------------------
@st.cache_data(ttl=30)
def buscar_dados_cotacoes():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL,GBP-BRL,CAD-BRL"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # Verifica se a requisição deu certo (Status 200)
        if response.status_code == 200:
            data = response.json()

            # Garante que 'data' é realmente um dicionário de cotações
            if isinstance(data, dict):
                lista_moedas = []
                for chave, info in data.items():
                    if isinstance(info, dict):
                        lista_moedas.append(
                            {
                                "Código": info.get("code", ""),
                                "Nome": info.get("name", "").split("/")[0],
                                "Par": info.get("name", ""),
                                "Valor Atual (R$)": float(
                                    info.get("bid", 0)
                                ),
                                "Variação (%)": float(
                                    info.get("pctChange", 0)
                                ),
                                "Máxima (R$)": float(info.get("high", 0)),
                                "Mínima (R$)": float(info.get("low", 0)),
                                "Última Atualização": info.get(
                                    "create_date", ""
                                ),
                            }
                        )
                return pd.DataFrame(lista_moedas)

        st.error(
            f"A API respondeu com código de status: {response.status_code}"
        )
        return pd.DataFrame()

    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
        return pd.DataFrame()


df = buscar_dados_cotacoes()

# ---------------------------------------------------------
# Barra Lateral (Sidebar)
# ---------------------------------------------------------
st.sidebar.title("⚙️ Painel de Controle")
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Atualizar Cotações Agora"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.subheader("Filtros de Exibição")
moedas_disponiveis = df["Nome"].unique().tolist() if not df.empty else []
moedas_selecionadas = st.sidebar.multiselect(
    "Selecione as moedas para comparar:",
    options=moedas_disponiveis,
    default=moedas_disponiveis,
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Projeto de Engenharia de Dados & ETL**\n\n"
    "• Consumo de API REST em tempo real\n"
    "• Tratamento de Dados com Pandas\n"
    "• Conversor dinâmico e visualização interativa"
)

# ---------------------------------------------------------
# Corpo Principal com ABAS (Tabs)
# ---------------------------------------------------------
st.title("📊 Dashboard Financeiro & Conversor")
st.caption("Dados atualizados em tempo real via AwesomeAPI")

# Criando duas abas no topo
tab_dashboard, tab_conversor = st.tabs(
    ["📈 Visão Geral do Mercado", "🔀 Conversor de Moedas"]
)

if df.empty:
    st.warning("Não foi possível carregar os dados. Verifique sua conexão.")
else:
    # ---------------------------------------------------------
    # ABA 1: DASHBOARD
    # ---------------------------------------------------------
    with tab_dashboard:
        df_filtrado = df[df["Nome"].isin(moedas_selecionadas)]

        # KPIs
        st.subheader("📌 Principais Ativos")
        cols = st.columns(min(len(df_filtrado), 4))
        for idx, (_, row) in enumerate(df_filtrado.head(4).iterrows()):
            with cols[idx % 4]:
                val_formatado = (
                    f"R$ {row['Valor Atual (R$)']:,.2f}"
                    if row["Valor Atual (R$)"] < 1000
                    else f"R$ {row['Valor Atual (R$)']:,.0f}"
                )
                st.metric(
                    label=f"{row['Nome']} ({row['Código']})",
                    value=val_formatado,
                    delta=f"{row['Variação (%)']:.2f}%",
                )

        st.markdown("---")

        # Gráficos
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.subheader("📉 Variação do Dia (%)")
            fig_var = px.bar(
                df_filtrado,
                x="Nome",
                y="Variação (%)",
                color="Variação (%)",
                color_continuous_scale=["#EF553B", "#00CC96"],
                text_auto=".2f",
                template="plotly_dark",
            )
            fig_var.update_layout(
                showlegend=False,
                height=350,
                xaxis_title="",
                yaxis_title="Variação Percentual (%)",
            )
            st.plotly_chart(fig_var, use_container_width=True)

        with col_graf2:
            st.subheader("📊 Amplitude de Preço (Máx vs Mín)")
            fig_amp = go.Figure()
            fig_amp.add_trace(
                go.Bar(
                    name="Mínima (R$)",
                    x=df_filtrado["Nome"],
                    y=df_filtrado["Mínima (R$)"],
                    marker_color="#FFA15A",
                )
            )
            fig_amp.add_trace(
                go.Bar(
                    name="Máxima (R$)",
                    x=df_filtrado["Nome"],
                    y=df_filtrado["Máxima (R$)"],
                    marker_color="#19D3F3",
                )
            )
            fig_amp.update_layout(
                barmode="group",
                template="plotly_dark",
                height=350,
                xaxis_title="",
                yaxis_title="Valor em Reais (R$)",
            )
            st.plotly_chart(fig_amp, use_container_width=True)

        # Tabela
        st.markdown("---")
        st.subheader("📋 Tabela Completa")
        df_exibicao = df_filtrado.copy()
        df_exibicao["Valor Atual (R$)"] = df_exibicao["Valor Atual (R$)"].map(
            "{:,.2f}".format
        )
        df_exibicao["Máxima (R$)"] = df_exibicao["Máxima (R$)"].map(
            "{:,.2f}".format
        )
        df_exibicao["Mínima (R$)"] = df_exibicao["Mínima (R$)"].map(
            "{:,.2f}".format
        )
        df_exibicao["Variação (%)"] = df_exibicao["Variação (%)"].map(
            "{:+.2f}%".format
        )

        st.dataframe(
            df_exibicao[
                [
                    "Nome",
                    "Código",
                    "Valor Atual (R$)",
                    "Variação (%)",
                    "Máxima (R$)",
                    "Mínima (R$)",
                    "Última Atualização",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    # ---------------------------------------------------------
    # ABA 2: CONVERSOR DE MOEDAS
    # ---------------------------------------------------------
    with tab_conversor:
        st.subheader("🔀 Conversor Dinâmico de Moedas")
        st.write(
            "Calcule a conversão instantânea de qualquer moeda monitorada para Real (BRL) ou vice-versa."
        )

        st.markdown("---")

        col_conv1, col_conv2, col_conv3 = st.columns(3)

        with col_conv1:
            direcao = st.radio(
                "Tipo de Conversão:",
                ["Moeda Estrangeira ➔ Real (BRL)", "Real (BRL) ➔ Moeda Estrangeira"],
            )

        with col_conv2:
            moeda_selecionada = st.selectbox(
                "Selecione a Moeda:", options=df["Nome"].unique()
            )

        with col_conv3:
            valor_input = st.number_input(
                "Valor a converter:", min_value=0.01, value=100.0, step=10.0
            )

        # Resgate da cotação
        linha_moeda = df[df["Nome"] == moeda_selecionada].iloc[0]
        cotacao = linha_moeda["Valor Atual (R$)"]
        codigo = linha_moeda["Código"]

        st.markdown("---")

        # Lógica de Cálculo
        if "Estrangeira ➔ Real" in direcao:
            resultado = valor_input * cotacao
            st.success(
                f"### **{valor_input:,.2f} {codigo}** = **R$ {resultado:,.2f} BRL**"
            )
            st.info(f"Taxa de câmbio aplicada: 1 {codigo} = R$ {cotacao:,.4f} BRL")
        else:
            resultado = valor_input / cotacao
            st.success(
                f"### **R$ {valor_input:,.2f} BRL** = **{resultado:,.4f} {codigo}**"
            )
            st.info(f"Taxa de câmbio aplicada: 1 BRL = {1/cotacao:,.4f} {codigo}")
