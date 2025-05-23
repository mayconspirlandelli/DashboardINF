#######
#  Codigo para Mostrar os totalizadores do RADOC filtrados por Ano
#########


import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv("dados/Dados-RADOCs-2023-2024.csv")

# Sidebar com filtros
st.sidebar.title("Filtros")
anos = df["Ano"].unique()
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(anos, reverse=True))

df_filtrado = df[df["Ano"] == ano_selecionado]

# Título
st.title("Painel de Produção Acadêmica e Tecnológica - INF")

# Mapear os grupos principais às suas subcolunas
grupos = {
    "I Atividades de Ensino": [
        "I-1 Graduação", "I-2 Pós-Graduação stricto e lato sensu", "I-3 Projetos de Ensino"
    ],
    "II Produção Intelectual": [
        "II-1 Produção Científica", "II-2 Produção Artística e Cultural",
        "II-3 Produção Técnica e Tecnológica", "II-4 Outro Tipo de Produção"
    ],
    "III Atividades de Pesquisa e Extensão": [
        "III-1 Atividades de Coordenação de Pesquisa e Inovação", "III-2 Atividades de Extensão"
    ],
    "IV Atividades Administrativas e de Representação": [
        "IV-1 Direção e Função Gratificada", "IV-2 Atividades Administrativas",
        "IV-3 Outras Atividades Administrativas", "IV-4 Atividades de Representação Fora da UFG"
    ],
    "V Outras Atividades": [
        "V-1 Atividades Acadêmicas – Orientação", "V-2 Atividades Acadêmicas – Bancas e Cursos",
        "V-3 Atividades de Aprendizado e Aperfeiçoamento"
    ]
}

# Calcular os totais por grupo
dados = {
    "Grupo": [],
    "Total": []
}

for grupo, colunas in grupos.items():
    #total = df_filtrado[colunas].sum(axis=1).values[0]  # soma linha única (ano selecionado)
    total = df_filtrado[colunas].sum().sum()
    dados["Grupo"].append(grupo)
    dados["Total"].append(total)

# Criar DataFrame para plotar
df_grupos = pd.DataFrame(dados)

# Criar gráfico de barras verticais
fig = px.bar(
    df_grupos,
    x="Grupo",
    y="Total",
    text="Total",
    title=f"Total de Atividades por Atividade - {ano_selecionado}",
    labels={"Grupo": "Grupo de Atividades", "Total": "Pontuação"},
)

fig.update_traces(textposition="outside")
fig.update_layout(xaxis_tickangle=-30)

# Mostrar no Streamlit
st.plotly_chart(fig, use_container_width=True)
