import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit import title

# Configuração da página
# Define o título da página, o ícone e o layout para ocupar a lagura inteira
def configura_pagina():
    st.set_page_config(
        page_title = "Dashboard de Salários na Área de Dados",
        page_icon = "📊",
        layout = "wide"
    )

# Armazenamento dos dados e leitura

def armazena_dados():
    return pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

def cria_painel_filtro():
    # Cria os filtros de pesquisa
    st.sidebar.header("Filtros Disponíveis 🔎")

configura_pagina()
df = armazena_dados()
cria_painel_filtro()



# Programa filtro para o ano
anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default = anos_disponiveis)

# Programa filtros para senioridade
senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default = senioridades_disponiveis)

# Programa filtro por tipo de contrato
contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default = contratos_disponiveis)

# Programa filtro pelo tamanho da empresa
tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default = tamanhos_disponiveis)

# Programar a filtragem baseado nos valores selecionados pelo usuário
df_filtrado = df[
    (df["ano"].isin(anos_selecionados)) &
    (df["senioridade"].isin(senioridades_selecionadas)) &
    (df["contrato"].isin(contratos_selecionados)) &
    (df["tamanho_empresa"].isin(tamanhos_selecionados))
]

# Conteúdo explicativo sobre a aplicação
st.title("📈 Dashboard de Análise de Salários na Área de Dados 🎲")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# Métrica Principal KPI
st.markdown("Métricas gerais (Salario Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado["usd"].mean()
    salario_maximo = df_filtrado["usd"].max()
    total_registros = df_filtrado.shape[0]
    cargo_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_frequente = 0, 0, 0, ""

coluna1, coluna2, coluna3, coluna4 = st.columns(4)
coluna1.metric("Salário Médio", f"${salario_medio:,.0f}")
coluna2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
coluna3.metric("Total de Registros", f"${total_registros:,}")
coluna4.metric("Cargo Frequente", cargo_frequente)

# Análise Visual com Plotly
st.subheader("Gráficos")

coluna_grafico1, coluna_grafico2 = st.columns(2)

with coluna_grafico1:
    if not df_filtrado.empty:
        maiores_cargos = df_filtrado.groupby("cargo")["usd"].mean().nlargest(10).sort_values(ascending = True).reset_index()
        grafico_cargos = px.bar(
            maiores_cargos,
            x = "usd",
            y = "cargo",
            orientation = "h",
            title = "Os 10 Maiores Salários Médios",
            labels = {"usd": "Média Salarial Anual (USD)", "cargo": ""}
        )
        grafico_cargos.update_layout(title_x = 0.1, yaxis = {"categoryorder": "total ascending"})
        st.plotly_chart(grafico_cargos, use_container_width = True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos")

with coluna_grafico2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x = "usd",
            nbins = 30,
            title = "Distribuição de Salários Anuais",
            labels = {"usd": "Faixa Salarial (USD)", "count": ""}
        )
        grafico_hist.update_layout(title_x = 0.1)
        st.plotly_chart(grafico_hist, use_container_width = True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

coluna_grafico3, coluna_grafico4 = st.columns(2)

with coluna_grafico3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado["remoto"].value_counts().reset_index()
        remoto_contagem.columns = ["tipo_trabalho", "quantidade"]
        grafico_remoto = px.pie(
            remoto_contagem,
            names = "tipo_trabalho",
            values = "quantidade",
            title = "Proporção dos tipos de trabalhos",
            hole = 0.5
        )
        grafico_remoto.update_traces(textinfo = "percent+label")
        grafico_remoto.update_layout(title_x = 0.1)
        st.plotly_chart(grafico_remoto, use_container_width = True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with coluna_grafico4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado["cargo"] == "Data Scientist"]
        media_ds_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()
        grafico_paises = px.choropleth(
            media_ds_pais,
            locations = "residencia_iso3",
            color = "usd",
            color_continuous_scale = "rdylgn",
            title = "Salário Médio de Cientista de Dados por País",
            labels = {"usd": "Salário Médio (USD)", "residencia_iso3": "País"}
        )
        grafico_paises.update_layout(title_x = 0.1)
        st.plotly_chart(grafico_paises, use_container_width = True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos países.")

# Tabela dos dados detalhados
st.subheader("Dados detalhados")
st.dataframe(df_filtrado)