import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px


# Codigo para Mostrar os totalizadores do RADOC por compentencia  
# Carregar dados
df = pd.read_csv("dados/Dados-RADOCs-2023-2024.csv")

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
    "Pesquisa": [
        "III-1 Atividades de Coordenação de Pesquisa e Inovação"
    ],
    "Extensão": [
        "III-2 Atividades de Extensão"
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

# Selecionar múltiplos anos
anos = df["Ano"].unique()
anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos:", sorted(anos), default=sorted(anos)
)

# Dados para o gráfico: cada linha será (Grupo, Ano, Total)
dados = {
    "Grupo": [],
    "Ano": [],
    "Total": []
}

# Calcular totais por grupo e por ano
for ano in anos_selecionados:
    df_ano = df[df["Ano"] == ano]
    for grupo, colunas in grupos.items():
        total = df_ano[colunas].sum().sum()  # soma total das colunas do grupo no ano
        dados["Grupo"].append(grupo)
        dados["Ano"].append(str(ano))  # converter para string para legenda mais limpa
        dados["Total"].append(total)

# Criar DataFrame para plotar
df_resultado = pd.DataFrame(dados)

# Substituir os nomes longos dos grupos por rótulos mais curtos
mapeamento_rotulos = {
    "I Atividades de Ensino": "Ensino",
    "II Produção Intelectual": "Produção Intelectual",
    "III Atividades de Pesquisa e Extensão": "Pesquisa e Extensão",
    "IV Atividades Administrativas e de Representação": "Administrativas",
    "V Outras Atividades": "Outras Atividades"
}

df_resultado["Grupo"] = df_resultado["Grupo"].replace(mapeamento_rotulos)


# Criar gráfico de barras agrupado por grupo, colorido por ano
fig = px.bar(
    df_resultado,
    x="Grupo",
    y="Total",
    color="Ano",
    barmode="group",
    text_auto=True,
    title="Atividades por Grupo e por Ano",
    labels={"Grupo": "Grupo de Atividades", "Total": "Pontuação"},
    color_discrete_sequence=["green", "blue", "gray", "orange"]
)


# Ensino, Produção Intelectual, Pesquisa, Extensão, Administrativas, Outras Atividades
fig.update_layout(xaxis_tickangle=-30)

# Mostrar no Streamlit
st.plotly_chart(fig, use_container_width=True)


# Agrupar dados por grupo (somando todos os anos selecionados)
df_pizza = df_resultado.groupby("Grupo")["Total"].sum().reset_index()

# Criar gráfico de pizza
fig_pizza = px.pie(
    df_pizza,
    names="Grupo",
    values="Total",
    title="Distribuição das Atividades por Grupo",
    hole=0.5  # se quiser tipo "donut", senão use hole=0 ou remova esse argumento
)

# Exibir no Streamlit
st.plotly_chart(fig_pizza, use_container_width=True)
