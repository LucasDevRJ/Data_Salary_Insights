import streamlit as st
import pandas as pd
import plotly.express as px

def configura_pagina():
    st.set_page_config(
        page_title = "Dashboard de Salários na Área de Dados",
        page_icon = "📊",
        layout = "wide"
    )

def armazena_dados():
    return pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

def cria_painel_filtro():
    st.sidebar.header("Filtros Disponíveis 🔎")

def cria_filtro(tipo_filtro, nome_filtro):
    valores_disponiveis = sorted(df[tipo_filtro].unique())
    valores_selecionados = st.sidebar.multiselect(nome_filtro, valores_disponiveis, default = valores_disponiveis)
    return valores_selecionados

def programa_filtro():
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
            st.title("📈 Dashboard de Análise de Salários na Área de Dados 🎲")
            st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")
        case "kpi":
            st.markdown("Métricas gerais (Salario Anual em USD)")
        case "analise":
            st.subheader("Gráficos")

def adiciona_valor(valor):
    if not df_filtrado.empty:
        match valor:
            case 1:
                return df_filtrado["usd"].mean()
            case 2:
                return df_filtrado["usd"].max()
            case 3:
                return df_filtrado.shape[0]
            case 4:
                return df_filtrado["cargo"].mode()[0]
            case _:
                return 0


def cria_colunas_valores():
    coluna1, coluna2, coluna3, coluna4 = st.columns(4)
    coluna1.metric("Salário Médio", f"${salario_medio:,.0f}")
    coluna2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
    coluna3.metric("Total de Registros", f"{total_registros:,}")
    coluna4.metric("Cargo Frequente", cargo_frequente)

def cria_grafico_maiores_salarios():
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

def cria_grafico_distribuicao_salarial():
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

def cria_grafico_proporcao_tipo_trabalho():
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

def cria_grafico_salario_medio():
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

def exibe_tabela_dados():
    st.subheader("Dados detalhados")
    st.dataframe(df_filtrado)

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
salario_medio = adiciona_valor(1)
salario_maximo = adiciona_valor(2)
total_registros = adiciona_valor(3)
cargo_frequente = adiciona_valor(4)
cria_colunas_valores()
coluna_grafico1, coluna_grafico2 = st.columns(2)
coluna_grafico3, coluna_grafico4 = st.columns(2)
cria_grafico_maiores_salarios()
cria_grafico_distribuicao_salarial()
cria_grafico_proporcao_tipo_trabalho()
cria_grafico_salario_medio()
exibe_tabela_dados()
