import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
# Define o título da página, o ícone e o layout para ocupar a lagura inteira
st.set_page_config(
    page_title = "Dashboard de Salários na Área de Dados",
    page_icon = "📊",
    layout = "wide"
)

# Armazenamento dos dados e leitura
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Cria os filtros de pesquisa
st.sidebar.header("Filtros Disponíveis 🔎")

# Programa filtro para o ano
anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default = anos_disponiveis)

# Programa filtros para senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default = senioridades_disponiveis)