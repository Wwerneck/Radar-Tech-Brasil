"""Streamlit dashboard for Radar Tech Brasil."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
EXTERNAL_DIR = PROJECT_ROOT / "data" / "external"
COLOR_SEQUENCE = ["#2563eb", "#16a34a", "#dc2626", "#9333ea", "#ea580c", "#0891b2"]
AGE_GROUP_LABELS = {
    "Ate 20": "Até 20",
    "21-25": "21-25",
    "26-30": "26-30",
    "31-35": "31-35",
    "36-40": "36-40",
    "41-50": "41-50",
    "51+": "51+",
    "Nao informado": "Não informado",
}
EDUCATION_LABELS = {
    "Fundamental incompleto": "Ensino fundamental incompleto",
    "Fundamental completo": "Ensino fundamental completo",
    "Medio incompleto": "Ensino médio incompleto",
    "Medio completo": "Ensino médio completo",
    "Superior incompleto": "Ensino superior incompleto",
    "Superior completo": "Ensino superior completo",
    "Mestrado": "Mestrado",
    "Doutorado": "Doutorado",
    "Pos-graduacao completa": "Pós-graduação completa",
    "Pos-graduacao incompleta": "Pós-graduação incompleta",
}
UF_NAME_LABELS = {
    "Sao Paulo": "São Paulo",
    "Parana": "Paraná",
    "Ceara": "Ceará",
    "Goias": "Goiás",
    "Espirito Santo": "Espírito Santo",
    "Para": "Pará",
    "Maranhao": "Maranhão",
    "Paraiba": "Paraíba",
    "Piaui": "Piauí",
    "Rondonia": "Rondônia",
    "Amapa": "Amapá",
}
METRIC_LABELS = {
    "total_admissoes": "Admissões",
    "total_desligamentos": "Desligamentos",
    "saldo_empregos": "Saldo de empregos",
    "remuneracao_media": "Salário médio",
    "remuneracao_mediana": "Salário mediano",
}


st.set_page_config(page_title="Radar Tech Brasil", layout="wide")


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    """Load a semicolon-separated CSV."""
    return pd.read_csv(path, sep=";")


def format_number(value: float) -> str:
    """Format numbers using Brazilian separators."""
    return f"{value:,.0f}".replace(",", ".")


def format_currency(value: float) -> str:
    """Format currency using Brazilian separators."""
    formatted = f"{value:,.2f}"
    return "R$ " + formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value: float) -> str:
    """Format percentages using Brazilian separators."""
    formatted = f"{value:,.1f}%"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_competence(value: str) -> str:
    """Format YYYYMM competence as MM/YYYY for Brazilian readers."""
    value = str(value)
    return f"{value[4:6]}/{value[:4]}"


def variation(first: float, last: float) -> float:
    """Return percentage variation between two values."""
    if first == 0:
        return 0.0
    return ((last - first) / first) * 100


def csv_bytes(df: pd.DataFrame) -> bytes:
    """Return a dataframe as downloadable CSV bytes."""
    return df.to_csv(index=False, sep=";").encode("utf-8")


def format_display_table(df: pd.DataFrame, labels: dict[str, str]) -> pd.DataFrame:
    """Return a copy with user-facing column names for Streamlit tables."""
    return df.rename(columns=labels)


overview = load_csv(PROCESSED_DIR / "agg_tech_overview_mensal.csv")
by_category = load_csv(PROCESSED_DIR / "agg_tech_by_category_mensal.csv")
by_uf = load_csv(PROCESSED_DIR / "agg_tech_by_uf_mensal_enriched.csv")
by_occupation = load_csv(PROCESSED_DIR / "agg_tech_by_occupation_mensal.csv")
by_age_group = load_csv(PROCESSED_DIR / "agg_tech_by_age_group_mensal.csv")
by_education = load_csv(PROCESSED_DIR / "agg_tech_by_education_mensal_enriched.csv")
uf_centroids = load_csv(EXTERNAL_DIR / "uf_centroids.csv")

for frame in [overview, by_category, by_uf, by_occupation, by_age_group, by_education]:
    frame["competencia"] = frame["competencia"].astype(str)
    frame["competencia_label"] = frame["competencia"].map(format_competence)

competences = sorted(overview["competencia"].unique())
categories = sorted(by_category["categoria_tech"].unique())
regions = sorted(by_uf["regiao_nome"].dropna().unique())
states = sorted(by_uf["uf_sigla"].dropna().unique())
occupations = sorted(by_occupation["ocupacao"].dropna().unique())
by_education = by_education[by_education["escolaridade"] != "Analfabeto"]
age_groups = ["Ate 20", "21-25", "26-30", "31-35", "36-40", "41-50", "51+", "Nao informado"]
education_labels = sorted(by_education["escolaridade"].dropna().unique())

st.title("Radar Tech Brasil")
st.caption("Inteligência de Dados sobre o Mercado de Tecnologia Brasileiro")

with st.sidebar:
    st.header("Filtros")
    selected_period = st.select_slider(
        "Periodo",
        options=competences,
        value=(competences[0], competences[-1]),
        format_func=format_competence,
    )
    start_period, end_period = selected_period
    selected_competences = [
        competence for competence in competences if start_period <= competence <= end_period
    ]
    st.caption(
        f"{format_competence(selected_competences[0])} a "
        f"{format_competence(selected_competences[-1])}"
    )

    st.divider()
    category_action = st.radio("Categorias", ["Todas", "Personalizada"], horizontal=True)
    if category_action == "Todas":
        selected_categories = categories
        st.caption(f"{len(categories)} categorias selecionadas")
    else:
        selected_categories = [
            category
            for category in categories
            if st.checkbox(category, value=True, key=f"category_{category}")
        ]

    selected_regions = st.multiselect(
        "Região",
        regions,
        default=[],
        placeholder="Selecione uma ou mais regiões",
    )
    selected_states = st.multiselect(
        "UF",
        states,
        default=[],
        placeholder="Escolha as UFs",
    )
    selected_age_groups = st.multiselect(
        "Faixa etária",
        age_groups,
        default=[],
        format_func=lambda value: AGE_GROUP_LABELS.get(value, value),
        placeholder="Selecione uma ou mais faixas etárias",
    )
    selected_education = st.multiselect(
        "Escolaridade",
        education_labels,
        default=[],
        format_func=lambda value: EDUCATION_LABELS.get(value, value),
        placeholder="Selecione um ou mais níveis de escolaridade",
    )
    selected_occupations = st.multiselect(
        "Ocupação",
        occupations,
        default=[],
        placeholder="Selecione uma ou mais ocupações",
    )

if not selected_categories:
    st.warning("Selecione pelo menos uma categoria para visualizar os dados.")
    st.stop()

filtered_overview = overview[overview["competencia"].isin(selected_competences)]
filtered_category = by_category[
    by_category["competencia"].isin(selected_competences)
    & by_category["categoria_tech"].isin(selected_categories)
]
filtered_uf = by_uf[by_uf["competencia"].isin(selected_competences)]
if selected_regions:
    filtered_uf = filtered_uf[filtered_uf["regiao_nome"].isin(selected_regions)]
if selected_states:
    filtered_uf = filtered_uf[filtered_uf["uf_sigla"].isin(selected_states)]
filtered_occupation = by_occupation[
    by_occupation["competencia"].isin(selected_competences)
    & by_occupation["categoria_tech"].isin(selected_categories)
]
if selected_occupations:
    filtered_occupation = filtered_occupation[
        filtered_occupation["ocupacao"].isin(selected_occupations)
    ]
filtered_age = by_age_group[by_age_group["competencia"].isin(selected_competences)]
if selected_age_groups:
    filtered_age = filtered_age[filtered_age["faixa_etaria"].isin(selected_age_groups)]
filtered_education = by_education[by_education["competencia"].isin(selected_competences)]
if selected_education:
    filtered_education = filtered_education[
        filtered_education["escolaridade"].isin(selected_education)
    ]

total_records = int(filtered_overview["total_registros_tech"].sum())
total_admissions = int(filtered_overview["total_admissoes"].sum())
total_dismissals = int(filtered_overview["total_desligamentos"].sum())
total_balance = int(filtered_overview["saldo_empregos"].sum())
weighted_salary = 0.0
if total_records:
    weighted_salary = (
        filtered_overview["remuneracao_media"] * filtered_overview["total_registros_tech"]
    ).sum() / total_records

first_month = filtered_overview.sort_values("competencia").iloc[0]
last_month = filtered_overview.sort_values("competencia").iloc[-1]
admission_delta = variation(first_month["total_admissoes"], last_month["total_admissoes"])
median_salary_delta = variation(first_month["remuneracao_mediana"], last_month["remuneracao_mediana"])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Registros tech", format_number(total_records))
col2.metric("Admissões", format_number(total_admissions), format_percent(admission_delta))
col3.metric("Desligamentos", format_number(total_dismissals))
col4.metric("Saldo", format_number(total_balance))
col5.metric("Salário médio", format_currency(weighted_salary))

best_month = filtered_overview.sort_values("saldo_empregos", ascending=False).iloc[0]
worst_month = filtered_overview.sort_values("saldo_empregos").iloc[0]
top_category = (
    filtered_category.groupby("categoria_tech", as_index=False)["registros"]
    .sum()
    .sort_values("registros", ascending=False)
    .iloc[0]
)
top_uf = None
if not filtered_uf.empty:
    top_uf = (
        filtered_uf.groupby("uf_sigla", as_index=False)["registros"]
        .sum()
        .sort_values("registros", ascending=False)
        .iloc[0]
    )

ctx1, ctx2, ctx3, ctx4 = st.columns(4)
ctx1.info(f"Maior saldo mensal: {format_competence(best_month['competencia'])}")
ctx2.info(f"Menor saldo mensal: {format_competence(worst_month['competencia'])}")
ctx3.info(f"Categoria com maior volume: {top_category['categoria_tech']}")
ctx4.info(
    f"UF com maior volume: {top_uf['uf_sigla']}"
    if top_uf is not None
    else "UF com maior volume: sem dados no filtro"
)

tabs = st.tabs(
    [
        "Visão Geral",
        "Mercado",
        "Profissões",
        "Salários",
        "Estados",
        "Perfil Profissional",
        "Insights",
        "Metodologia",
    ]
)

with tabs[0]:
    overview_long = filtered_overview.melt(
        id_vars=["competencia_label"],
        value_vars=["total_admissoes", "total_desligamentos", "saldo_empregos"],
        var_name="metrica",
        value_name="valor",
    )
    overview_long["metrica"] = overview_long["metrica"].map(METRIC_LABELS)
    fig = px.line(
        overview_long,
        x="competencia_label",
        y="valor",
        color="metrica",
        markers=True,
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"valor": "Registros", "competencia_label": "Competência", "metrica": "Métrica"},
        title="Evolução mensal do mercado tech formal",
    )
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, use_container_width=True)

    salary_long = filtered_overview.melt(
        id_vars=["competencia_label"],
        value_vars=["remuneracao_media", "remuneracao_mediana"],
        var_name="metrica",
        value_name="valor",
    )
    salary_long["metrica"] = salary_long["metrica"].map(METRIC_LABELS)
    salary_fig = px.line(
        salary_long,
        x="competencia_label",
        y="valor",
        color="metrica",
        markers=True,
        color_discrete_sequence=["#2563eb", "#16a34a"],
        labels={"valor": "Salário", "competencia_label": "Competência", "metrica": "Métrica"},
        title="Evolução salarial",
    )
    salary_fig.update_xaxes(type="category")
    st.plotly_chart(salary_fig, use_container_width=True)
    st.markdown(
        """
        <div style="font-size: 0.92rem; line-height: 1.55; margin-top: -0.75rem; color: #64748b;">
          <div><span style="display: inline-block; width: 10px; height: 10px; border-radius: 999px; background: #2563eb; margin-right: 8px;"></span><strong>Salário médio:</strong> soma dos salários válidos dividida pela quantidade de registros.</div>
          <div><span style="display: inline-block; width: 10px; height: 10px; border-radius: 999px; background: #16a34a; margin-right: 8px;"></span><strong>Salário mediano:</strong> valor central da distribuição salarial, menos sensível a salários muito altos.</div>
          <div style="margin-top: 0.35rem;">Ambas excluem salários iguais a zero e registros marcados como salário extremo.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
    category_table = format_display_table(
        category_total,
        {
            "categoria_tech": "Categoria",
            "registros": "Registros",
            "admissoes": "Admissões",
            "desligamentos": "Desligamentos",
            "saldo_empregos": "Saldo de empregos",
        },
    )
    st.download_button("Baixar tabela de categorias", csv_bytes(category_table), "categorias.csv")
    st.dataframe(category_table, use_container_width=True, hide_index=True)

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
    )
    fig = px.bar(
        occupation_total.head(25).sort_values("registros"),
        x="registros",
        y="ocupacao",
        color="categoria_tech",
        orientation="h",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"registros": "Registros", "ocupacao": "Ocupação"},
        title="Top ocupações tech por volume",
    )
    st.plotly_chart(fig, use_container_width=True)
    occupation_table = format_display_table(
        occupation_total,
        {
            "codigo_cbo": "Código CBO",
            "ocupacao": "Ocupação",
            "categoria_tech": "Categoria",
            "registros": "Registros",
            "admissoes": "Admissões",
            "desligamentos": "Desligamentos",
            "saldo_empregos": "Saldo de empregos",
        },
    )
    st.download_button("Baixar tabela de ocupações", csv_bytes(occupation_table), "ocupacoes.csv")
    st.dataframe(occupation_table.head(100), use_container_width=True, hide_index=True)

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
        labels={"remuneracao_mediana": "Salário mediano", "categoria_tech": "Categoria"},
        title="Salário mediano por categoria",
    )
    st.plotly_chart(fig, use_container_width=True)

    salary_by_uf = (
        filtered_uf.groupby(["uf_sigla", "uf_nome", "regiao_nome"], as_index=False)
        .agg(
            remuneracao_media=("remuneracao_media", "mean"),
            remuneracao_mediana=("remuneracao_mediana", "median"),
            registros=("registros", "sum"),
        )
        .sort_values("remuneracao_mediana", ascending=False)
    )
    salary_by_uf["uf_nome"] = salary_by_uf["uf_nome"].map(
        lambda value: UF_NAME_LABELS.get(value, value)
    )
    fig = px.bar(
        salary_by_uf.head(15),
        x="uf_sigla",
        y="remuneracao_mediana",
        color="regiao_nome",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"uf_sigla": "UF", "remuneracao_mediana": "Salário mediano"},
        title="Top UFs por salário mediano",
    )
    st.plotly_chart(fig, use_container_width=True)
    salary_category_table = format_display_table(
        salary_by_category,
        {
            "categoria_tech": "Categoria",
            "remuneracao_media": "Salário médio",
            "remuneracao_mediana": "Salário mediano",
            "registros": "Registros",
        },
    )
    salary_uf_table = format_display_table(
        salary_by_uf,
        {
            "uf_sigla": "UF",
            "uf_nome": "Estado",
            "regiao_nome": "Região",
            "remuneracao_media": "Salário médio",
            "remuneracao_mediana": "Salário mediano",
            "registros": "Registros",
        },
    )
    st.download_button("Baixar tabela de salários por UF", csv_bytes(salary_uf_table), "salarios_uf.csv")
    st.dataframe(salary_category_table, use_container_width=True, hide_index=True)

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
    uf_total["uf_nome"] = uf_total["uf_nome"].map(lambda value: UF_NAME_LABELS.get(value, value))
    map_data = uf_total.merge(uf_centroids, on="uf", how="left")
    fig = px.scatter_geo(
        map_data,
        lat="latitude",
        lon="longitude",
        size="registros",
        color="saldo_empregos",
        hover_name="uf_nome",
        hover_data={
            "uf_sigla": True,
            "registros": ":,.0f",
            "saldo_empregos": ":,.0f",
            "latitude": False,
            "longitude": False,
        },
        scope="south america",
        color_continuous_scale="RdYlGn",
        labels={
            "uf_sigla": "UF",
            "saldo_empregos": "Saldo",
            "registros": "Registros",
            "uf_nome": "Estado",
        },
        title="Distribuição geográfica por UF",
    )
    fig.update_geos(
        fitbounds="locations",
        visible=True,
        bgcolor="#0b0f17",
        landcolor="#1f2937",
        countrycolor="#475569",
        coastlinecolor="#475569",
        showcountries=True,
        showcoastlines=True,
        showland=True,
    )
    fig.update_layout(
        paper_bgcolor="#0b0f17",
        plot_bgcolor="#0b0f17",
        margin=dict(l=0, r=0, t=55, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        uf_total.head(20),
        x="uf_sigla",
        y="saldo_empregos",
        color="regiao_nome",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"uf_sigla": "UF", "saldo_empregos": "Saldo", "regiao_nome": "Região"},
        title="Saldo tech por UF",
    )
    st.plotly_chart(fig, use_container_width=True)
    uf_table = format_display_table(
        uf_total,
        {
            "uf": "Código da UF",
            "uf_sigla": "UF",
            "uf_nome": "Estado",
            "regiao_nome": "Região",
            "registros": "Registros",
            "admissoes": "Admissões",
            "desligamentos": "Desligamentos",
            "saldo_empregos": "Saldo de empregos",
        },
    )
    st.download_button("Baixar tabela de UFs", csv_bytes(uf_table), "ufs.csv")
    st.dataframe(uf_table, use_container_width=True, hide_index=True)

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
    age_total["ordem"] = age_total["faixa_etaria"].apply(
        lambda value: age_groups.index(value) if value in age_groups else 99
    )
    age_total = age_total.sort_values("ordem").drop(columns="ordem")
    age_total["faixa_etaria"] = age_total["faixa_etaria"].map(
        lambda value: AGE_GROUP_LABELS.get(value, value)
    )
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
    education_total["escolaridade"] = education_total["escolaridade"].map(
        lambda value: EDUCATION_LABELS.get(value, value)
    )
    left, right = st.columns(2)
    with left:
        fig = px.bar(age_total, x="faixa_etaria", y="registros", title="Distribuição por faixa etária")
        st.plotly_chart(fig, use_container_width=True)
        age_table = format_display_table(
            age_total,
            {
                "faixa_etaria": "Faixa etária",
                "registros": "Registros",
                "admissoes": "Admissões",
                "desligamentos": "Desligamentos",
                "saldo_empregos": "Saldo de empregos",
            },
        )
        st.download_button("Baixar faixa etária", csv_bytes(age_table), "faixa_etaria.csv")
        st.dataframe(age_table, use_container_width=True, hide_index=True)
    with right:
        fig = px.bar(education_total, x="escolaridade", y="registros", title="Distribuição por escolaridade")
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)
        education_table = format_display_table(
            education_total,
            {
                "grau_instrucao": "Código de escolaridade",
                "escolaridade": "Escolaridade",
                "registros": "Registros",
                "admissoes": "Admissões",
                "desligamentos": "Desligamentos",
                "saldo_empregos": "Saldo de empregos",
            },
        )
        st.download_button("Baixar escolaridade", csv_bytes(education_table), "escolaridade.csv")
        st.dataframe(education_table, use_container_width=True, hide_index=True)

with tabs[6]:
    st.subheader("Insights automáticos")
    st.write(
        f"Saldo positivo de {format_number(total_balance)} vagas no período filtrado, "
        f"com {format_number(total_admissions)} admissões e {format_number(total_dismissals)} desligamentos."
    )
    st.write(
        f"A categoria com maior volume no filtro atual é {top_category['categoria_tech']}, "
        f"com {format_number(top_category['registros'])} registros."
    )
    st.write(
        f"A variação de admissões entre {format_competence(first_month['competencia'])} e "
        f"{format_competence(last_month['competencia'])} foi de {format_percent(admission_delta)}."
    )
    st.write(
        f"A variação do salário mediano no mesmo intervalo foi de {format_percent(median_salary_delta)}."
    )
    st.caption(
        "Esses insights são descritivos. Eles indicam associações e movimentos observados, "
        "mas não provam causalidade."
    )

with tabs[7]:
    st.subheader("Metodologia")
    st.write("Fonte principal: microdados públicos do Novo CAGED.")
    st.write("Fonte complementar: CBO 2002 oficial para identificação das ocupações.")
    st.write("Período consolidado: 07/2025 a 06/2026.")
    st.write("Recorte tech: mapeamento versionado em `data/external/cbo_tech_mapping.csv`.")
    st.write(
        "Salário médio e salário mediano consideram salários maiores que zero e removem "
        "registros marcados como salário extremo."
    )
    st.write(
        "Limitações: CBO não informa stack, senioridade, modalidade remota ou detalhes modernos "
        "da função exercida. Domínios marcados como pendentes devem ser revisados contra layout oficial."
    )
