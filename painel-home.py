import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
#df = pd.read_excel("painel_INF.xlsx")
df = pd.read_csv("dados/Dados-RADOCs-2023-2024.csv")

# Sidebar com filtros
st.sidebar.title("Filtros")
anos = df["Ano"].unique()
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(anos, reverse=True))

df_filtrado = df[df["Ano"] == ano_selecionado]

# Título
st.title("Painel de Produção Acadêmica e Tecnológica - INF")

# Abas
abas = st.tabs(["🎓 Ensino", "📚 Produção Intelectual", "🔬 Pesquisa e Extensão", "🏛️ Administrativo", "📘 Outras Atividades"])

# Aba 1 - Ensino
with abas[0]:
    st.subheader("Atividades de Ensino")
    colunas_ensino = ["I-1 Graduação", "I-2 Pós-Graduação stricto e lato sensu", "I-3 Projetos de Ensino"]
    # st.dataframe(df_filtrado[["Ano"] + colunas_ensino])
    # fig_ensino = px.bar(df_filtrado, x="Ano", y=colunas_ensino, barmode="group", title="Atividades de Ensino")
    # st.plotly_chart(fig_ensino, use_container_width=True)

    df_ensino = df_filtrado[["Ano"] + colunas_ensino]
    st.bar_chart(df_ensino.set_index("Ano"))

# Aba 2 - Produção Intelectual
with abas[1]:
    st.subheader("Produção Intelectual")
    colunas_pi = ["II-1 Produção Científica", "II-2 Produção Artística e Cultural", "II-3 Produção Técnica e Tecnológica", "II-4 Outro Tipo de Produção"]
    st.dataframe(df_filtrado[["Ano"] + colunas_pi])
    fig = px.bar(df_filtrado, x="Ano", y=colunas_pi, barmode="group", title="Produção Intelectual")
    st.plotly_chart(fig, use_container_width=True)
