"""Streamlit dashboard for Radar Tech Brasil."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
COLOR_SEQUENCE = ["#2563eb", "#16a34a", "#dc2626", "#9333ea", "#ea580c", "#0891b2"]


st.set_page_config(page_title="Radar Tech Brasil", layout="wide")


@st.cache_data(show_spinner=False)
def load_csv(name: str) -> pd.DataFrame:
    """Load a processed aggregate CSV."""
    return pd.read_csv(PROCESSED_DIR / name, sep=";")


def format_number(value: float) -> str:
    """Format numbers using Brazilian separators."""
    return f"{value:,.0f}".replace(",", ".")


def format_currency(value: float) -> str:
    """Format currency using Brazilian separators."""
    formatted = f"{value:,.2f}"
    return "R$ " + formatted.replace(",", "X").replace(".", ",").replace("X", ".")


overview = load_csv("agg_tech_overview_mensal.csv")
by_category = load_csv("agg_tech_by_category_mensal.csv")
by_uf = load_csv("agg_tech_by_uf_mensal_enriched.csv")
by_occupation = load_csv("agg_tech_by_occupation_mensal.csv")
by_age_group = load_csv("agg_tech_by_age_group_mensal.csv")
by_education = load_csv("agg_tech_by_education_mensal_enriched.csv")

for frame in [overview, by_category, by_uf, by_occupation, by_age_group, by_education]:
    frame["competencia"] = frame["competencia"].astype(str)

competences = sorted(overview["competencia"].unique())
categories = sorted(by_category["categoria_tech"].unique())

st.title("Radar Tech Brasil")
st.caption("Inteligencia de Dados sobre o Mercado de Tecnologia Brasileiro")

with st.sidebar:
    st.header("Filtros")
    selected_period = st.select_slider(
        "Periodo",
        options=competences,
        value=(competences[0], competences[-1]),
    )
    start_period, end_period = selected_period
    selected_competences = [
        competence for competence in competences if start_period <= competence <= end_period
    ]

    st.caption(f"{selected_competences[0]} a {selected_competences[-1]}")

    st.divider()
    st.subheader("Categorias")

    category_action = st.radio(
        "Selecao",
        ["Todas", "Personalizada"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if category_action == "Todas":
        selected_categories = categories
        st.caption(f"{len(categories)} categorias selecionadas")
    else:
        selected_categories = []
        for category in categories:
            if st.checkbox(category, value=True, key=f"category_{category}"):
                selected_categories.append(category)

        if not selected_categories:
            st.warning("Selecione pelo menos uma categoria.")

filtered_overview = overview[overview["competencia"].isin(selected_competences)]
filtered_category = by_category[
    by_category["competencia"].isin(selected_competences)
    & by_category["categoria_tech"].isin(selected_categories)
]
filtered_uf = by_uf[by_uf["competencia"].isin(selected_competences)]
filtered_occupation = by_occupation[
    by_occupation["competencia"].isin(selected_competences)
    & by_occupation["categoria_tech"].isin(selected_categories)
]
filtered_age = by_age_group[by_age_group["competencia"].isin(selected_competences)]
filtered_education = by_education[by_education["competencia"].isin(selected_competences)]

total_records = int(filtered_overview["total_registros_tech"].sum())
total_admissions = int(filtered_overview["total_admissoes"].sum())
total_dismissals = int(filtered_overview["total_desligamentos"].sum())
total_balance = int(filtered_overview["saldo_empregos"].sum())
weighted_salary = 0.0
if total_records:
    weighted_salary = (
        filtered_overview["remuneracao_media"] * filtered_overview["total_registros_tech"]
    ).sum() / total_records

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Registros tech", format_number(total_records))
col2.metric("Admissoes", format_number(total_admissions))
col3.metric("Desligamentos", format_number(total_dismissals))
col4.metric("Saldo", format_number(total_balance))
col5.metric("Remuneracao media", format_currency(weighted_salary))

tabs = st.tabs(
    [
        "Visao Geral",
        "Mercado",
        "Profissoes",
        "Salarios",
        "Estados",
        "Perfil Profissional",
        "Metodologia",
    ]
)

with tabs[0]:
    fig = px.line(
        filtered_overview,
        x="competencia",
        y=["total_admissoes", "total_desligamentos", "saldo_empregos"],
        markers=True,
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"value": "Registros", "competencia": "Competencia", "variable": "Metrica"},
        title="Evolucao mensal do mercado tech formal",
    )
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, use_container_width=True)

    salary_fig = px.line(
        filtered_overview,
        x="competencia",
        y=["remuneracao_media", "remuneracao_mediana"],
        markers=True,
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"value": "Remuneracao", "competencia": "Competencia", "variable": "Metrica"},
        title="Evolucao salarial",
    )
    salary_fig.update_xaxes(type="category")
    st.plotly_chart(salary_fig, use_container_width=True)

with tabs[1]:
    category_total = (
        filtered_category.groupby("categoria_tech", as_index=False)
        .agg(
            registros=("registros", "sum"),
            admissoes=("admissoes", "sum"),
            desligamentos=("desligamentos", "sum"),
            saldo_empregos=("saldo_empregos", "sum"),
        )
        .sort_values("registros", ascending=False)
    )
    fig = px.bar(
        category_total.sort_values("registros"),
        x="registros",
        y="categoria_tech",
        orientation="h",
        color="saldo_empregos",
        color_continuous_scale="RdYlGn",
        labels={"registros": "Registros", "categoria_tech": "Categoria", "saldo_empregos": "Saldo"},
        title="Volume e saldo por categoria tech",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(category_total, use_container_width=True, hide_index=True)

with tabs[2]:
    occupation_total = (
        filtered_occupation.groupby(["codigo_cbo", "ocupacao", "categoria_tech"], as_index=False)
        .agg(
            registros=("registros", "sum"),
            admissoes=("admissoes", "sum"),
            desligamentos=("desligamentos", "sum"),
            saldo_empregos=("saldo_empregos", "sum"),
        )
        .sort_values("registros", ascending=False)
        .head(25)
    )
    fig = px.bar(
        occupation_total.sort_values("registros"),
        x="registros",
        y="ocupacao",
        color="categoria_tech",
        orientation="h",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"registros": "Registros", "ocupacao": "Ocupacao"},
        title="Top ocupacoes tech por volume",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(occupation_total, use_container_width=True, hide_index=True)

with tabs[3]:
    salary_by_category = (
        filtered_category.groupby("categoria_tech", as_index=False)
        .agg(
            remuneracao_media=("remuneracao_media", "mean"),
            remuneracao_mediana=("remuneracao_mediana", "median"),
            registros=("registros", "sum"),
        )
        .sort_values("remuneracao_mediana", ascending=False)
    )
    fig = px.bar(
        salary_by_category.sort_values("remuneracao_mediana"),
        x="remuneracao_mediana",
        y="categoria_tech",
        orientation="h",
        color_discrete_sequence=["#2563eb"],
        labels={"remuneracao_mediana": "Remuneracao mediana", "categoria_tech": "Categoria"},
        title="Remuneracao mediana por categoria",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(salary_by_category, use_container_width=True, hide_index=True)

with tabs[4]:
    uf_total = (
        filtered_uf.groupby(["uf", "uf_sigla", "uf_nome", "regiao_nome"], as_index=False)
        .agg(
            registros=("registros", "sum"),
            admissoes=("admissoes", "sum"),
            desligamentos=("desligamentos", "sum"),
            saldo_empregos=("saldo_empregos", "sum"),
        )
        .sort_values("registros", ascending=False)
    )
    fig = px.bar(
        uf_total.head(20),
        x="uf_sigla",
        y="saldo_empregos",
        color="regiao_nome",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"uf_sigla": "UF", "saldo_empregos": "Saldo", "regiao_nome": "Regiao"},
        title="Saldo tech por UF",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(uf_total, use_container_width=True, hide_index=True)

with tabs[5]:
    age_total = (
        filtered_age.groupby("faixa_etaria", as_index=False)
        .agg(
            registros=("registros", "sum"),
            admissoes=("admissoes", "sum"),
            desligamentos=("desligamentos", "sum"),
            saldo_empregos=("saldo_empregos", "sum"),
        )
    )
    age_order = ["Ate 20", "21-25", "26-30", "31-35", "36-40", "41-50", "51+", "Nao informado"]
    age_total["ordem"] = age_total["faixa_etaria"].apply(
        lambda value: age_order.index(value) if value in age_order else 99
    )
    age_total = age_total.sort_values("ordem").drop(columns="ordem")

    education_total = (
        filtered_education.groupby(["grau_instrucao", "escolaridade"], as_index=False)
        .agg(
            registros=("registros", "sum"),
            admissoes=("admissoes", "sum"),
            desligamentos=("desligamentos", "sum"),
            saldo_empregos=("saldo_empregos", "sum"),
        )
        .sort_values("grau_instrucao")
    )

    left, right = st.columns(2)
    with left:
        fig = px.bar(
            age_total,
            x="faixa_etaria",
            y="registros",
            color_discrete_sequence=["#16a34a"],
            labels={"faixa_etaria": "Faixa etaria", "registros": "Registros"},
            title="Distribuicao por faixa etaria",
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.bar(
            education_total,
            x="escolaridade",
            y="registros",
            color_discrete_sequence=["#9333ea"],
            labels={"escolaridade": "Escolaridade", "registros": "Registros"},
            title="Distribuicao por escolaridade",
        )
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(age_total, use_container_width=True, hide_index=True)
    st.dataframe(education_total, use_container_width=True, hide_index=True)

with tabs[6]:
    st.subheader("Definicoes")
    st.write(
        "As metricas usam registros do Novo CAGED classificados como tecnologia pelo "
        "mapeamento versionado `data/external/cbo_tech_mapping.csv`."
    )
    st.write(
        "Remuneracao media e mediana consideram salarios maiores que zero e removem "
        "registros marcados com `flag_salario_extremo`."
    )
    st.write("A janela inicial consolidada cobre as competencias de 202507 a 202606.")
