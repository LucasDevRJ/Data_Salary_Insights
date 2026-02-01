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

def cria_filtro(tipo_filtro, nome_filtro):
    # Programa filtro para o ano
    valores_disponiveis = sorted(df[tipo_filtro].unique())
    valores_selecionados = st.sidebar.multiselect(nome_filtro, valores_disponiveis, default = valores_disponiveis)
    return valores_selecionados

def programa_filtro():
    # Programar a filtragem baseado nos valores selecionados pelo usuário
    df_filtrado = df[
        (df["ano"].isin(anos_selecionados)) &
        (df["senioridade"].isin(senioridades_selecionadas)) &
        (df["contrato"].isin(contratos_selecionados)) &
        (df["tamanho_empresa"].isin(tamanhos_selecionados))
    ]
    return df_filtrado

def adiciona_conteudo(conteudo):
    match conteudo:
        case "explicativo":
            # Conteúdo explicativo sobre a aplicação
            st.title("📈 Dashboard de Análise de Salários na Área de Dados 🎲")
            st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")
        case "kpi":
            # Métrica Principal KPI
            st.markdown("Métricas gerais (Salario Anual em USD)")
        case "analise":
            # Análise Visual com Plotly
            st.subheader("Gráficos")

def adiciona_valor_salario_medio():
    if not df_filtrado.empty:
        salario_medio = df_filtrado["usd"].mean()
    else:
        salario_medio = 0.0

    return salario_medio

def adiciona_valor_salario_maximo():
    if not df_filtrado.empty:
        salario_maximo = df_filtrado["usd"].max()
    else:
        salario_maximo = 0.0

    return salario_maximo

def adiciona_valor_total_registros():
    if not df_filtrado.empty:
        total_registros = df_filtrado.shape[0]
    else:
        total_registros = 0

    return total_registros

def adiciona_cargo_frequente():
    if not df_filtrado.empty:
        cargo_frequente = df_filtrado["cargo"].mode()[0]
    else:
        cargo_frequente = ""

    return cargo_frequente

# def adiciona_valores_filtro():
#     if not df_filtrado.empty:
#         salario_medio = df_filtrado["usd"].mean()
#         salario_maximo = df_filtrado["usd"].max()
#         total_registros = df_filtrado.shape[0]
#         cargo_frequente = df_filtrado["cargo"].mode()[0]
#     else:
#         salario_medio, salario_mediano, salario_maximo, total_registros, cargo_frequente = 0, 0, 0, ""


configura_pagina()
df = armazena_dados()
cria_painel_filtro()
anos_selecionados = cria_filtro("ano", "Ano")
senioridades_selecionadas = cria_filtro("senioridade", "Senioridade")
contratos_selecionados = cria_filtro("contrato", "Tipo de Contrato")
tamanhos_selecionados = cria_filtro("tamanho_empresa", "Tamanho da Empresa")
df_filtrado = programa_filtro()
adiciona_conteudo("explicativo")
adiciona_conteudo("kpi")
adiciona_conteudo("analise")
salario_medio = adiciona_valor_salario_medio()
salario_maximo = adiciona_valor_salario_maximo()
total_registros = adiciona_valor_total_registros()
cargo_frequente = adiciona_cargo_frequente()
# if not df_filtrado.empty:
#     salario_medio = df_filtrado["usd"].mean()
#     salario_maximo = df_filtrado["usd"].max()
#     total_registros = df_filtrado.shape[0]
#     cargo_frequente = df_filtrado["cargo"].mode()[0]
# else:
#     salario_medio, salario_mediano, salario_maximo, total_registros, cargo_frequente = 0, 0, 0, ""

coluna1, coluna2, coluna3, coluna4 = st.columns(4)
coluna1.metric("Salário Médio", f"${salario_medio:,.0f}")
coluna2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
coluna3.metric("Total de Registros", f"{total_registros:,}")
coluna4.metric("Cargo Frequente", cargo_frequente)

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