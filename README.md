# 📊 Dashboard Financeiro & ETL de Cotações em Tempo Real

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dashboard-cotacoes-tef8znhsrqpzta9g5x59am.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75)

Aplicação web interativa focada no monitoramento e análise de indicadores do mercado financeiro em tempo real, além de contar com um conversor dinâmico de moedas. 

O projeto aplica conceitos de **Engenharia de Dados (ETL)**, consumo de APIs REST, visualização interativa de dados e arquitetura defensiva para alta disponibilidade na nuvem.

🔗 **Acesse a aplicação ao vivo:** [Dashboard de Cotações no Streamlit Cloud](https://dashboard-cotacoes-tef8znhsrqpzta9g5x59am.streamlit.app)

---

## 🎯 Funcionalidades Principais

* **📌 Visão Geral de Ativos (KPIs):** Monitoramento instantâneo do preço do Dólar (USD), Euro (EUR), Bitcoin (BTC), Libra (GBP) e Dólar Canadense (CAD).
* **📉 Análise Visual Interativa:**
  * Gráfico de Variação Percentual (%) no dia via Plotly.
  * Gráfico comparativo de amplitude de preço (Máxima vs Mínima do dia).
* **🔀 Conversor Dinâmico de Câmbio:** Conversão bidirecional (Moeda Estrangeira ↔ Real BRL) com cálculo instantâneo baseado nas taxas atualizadas.
* **⚡ Alta Disponibilidade & Resiliência:**
  * **Caching de Dados (`st.cache_data`):** Reduz requisições desnecessárias e otimiza o tempo de resposta da aplicação.
  * **Mecanismo de Fallback:** Tratamento defensivo para erros de conexão e limitação de taxa (*Rate Limit / HTTP 429*), garantindo que a interface permaneça funcional.

---

## 🛠️ Stack Tecnológico

* **Linguagem:** Python 3.10+
* **Consumo de Dados:** `Requests` (API REST - [AwesomeAPI](https://docs.awesomeapi.com.br/))
* **Tratamento & ETL:** `Pandas`
* **Visualização de Dados:** `Plotly Express` & `Plotly Graph Objects`
* **Interface & Deploy:** `Streamlit` & `Streamlit Community Cloud`

---

## 🏗️ Estrutura do Projeto

```text
├── app.py              # Código principal da aplicação (ETL + Layout Streamlit)
├── requirements.txt    # Dependências do projeto para deploy na nuvem
└── README.md           # Documentação do repositório

Como Executar o Projeto Localmente

    Clone este repositório:
    Bash

    git clone [https://github.com/7gaalves7/dashboard-cotacoes.git](https://github.com/7gaalves7/dashboard-cotacoes.git)
    cd dashboard-cotacoes

    Crie e ative um ambiente virtual:
    Bash

    python -m venv venv
    # No Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    # No Windows (CMD):
    venv\Scripts\activate.bat

    Instale as dependências:
    Bash

    pip install -r requirements.txt

    Execute a aplicação:
    Bash

    streamlit run app.py

👤 Autor

Desenvolvido por Gabriel Alves Macedo Queiroz

Estudante de Ciência de Dados e Inteligência Artificial na PUC Goiás.

    LinkedIn: Gabriel Alves

    GitHub: @7gaalves7

    E-mail: 7gaalves7.data@gmail.com
