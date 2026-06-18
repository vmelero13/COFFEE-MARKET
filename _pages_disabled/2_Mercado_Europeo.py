import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path


# ==========================================================
# CONFIGURACIÓN DE PÁGINA
# ----------------------------------------------------------
# Esta página analiza únicamente el mercado europeo.
# Se utiliza el dataset enriquecido con población y PIB per cápita.
# ==========================================================

st.set_page_config(
    page_title="Mercado Europeo",
    page_icon="🇪🇺",
    layout="wide"
)


# Paleta visual Velluto.
VELLUTO_GOLD = "#B48D57"
VELLUTO_SECONDARY_GOLD = "#856F4A"
VELLUTO_BLACK = "#101820"
VELLUTO_CREAM = "#D9D4CF"
VELLUTO_BACKGROUND = "#F7F3EE"
VELLUTO_WHITE = "#FFFFFF"
VELLUTO_GREEN = "#556B4D"


# ==========================================================
# ESTILOS VISUALES
# ----------------------------------------------------------
# Se reutiliza la estética corporativa definida para el dashboard:
# fondo crema, tarjetas blancas y acentos dorados.
# ==========================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {VELLUTO_BACKGROUND};
        color: {VELLUTO_BLACK};
    }}

    h1, h2, h3 {{
        color: {VELLUTO_BLACK};
    }}

    .section-card {{
        background-color: {VELLUTO_WHITE};
        padding: 1.4rem;
        border-radius: 16px;
        border-left: 6px solid {VELLUTO_GOLD};
        margin-bottom: 1rem;
    }}

    .kpi-card {{
        background-color: {VELLUTO_WHITE};
        padding: 1.2rem;
        border-radius: 16px;
        border-top: 5px solid {VELLUTO_GOLD};
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        min-height: 105px;
    }}

    .kpi-label {{
        font-size: 0.85rem;
        color: {VELLUTO_SECONDARY_GOLD};
        margin-bottom: 0.3rem;
    }}

    .kpi-value {{
        font-size: 1.45rem;
        font-weight: 800;
        color: {VELLUTO_BLACK};
    }}
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_eu_data():
    """
    Carga el dataset europeo enriquecido.

    Este dataset contiene importaciones, población, PIB per cápita
    y métricas per cápita para países de la Unión Europea.
    """
    path = Path("data/processed/trade_enriched_complete_2020_2024.csv")
    return pd.read_csv(path)


def format_currency(value):
    """
    Formatea importes monetarios adaptando la unidad al tamaño del valor.
    """
    if pd.isna(value):
        return "N/A"

    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f} B"

    if value >= 1_000_000:
        return f"${value / 1_000_000:,.2f} M"

    if value >= 1_000:
        return f"${value / 1_000:,.1f} K"

    return f"${value:,.0f}"


def render_kpi(label, value):
    """
    Renderiza una tarjeta KPI.
    """
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# CARGA Y FILTROS
# ==========================================================

eu_data = load_eu_data()

st.title("🇪🇺 Mercado Europeo")
st.markdown(
    """
    <div class="section-card">
    Esta página analiza los países de la Unión Europea desde una perspectiva de oportunidad:
    tamaño del mercado, poder adquisitivo e intensidad importadora por habitante.
    </div>
    """,
    unsafe_allow_html=True
)


# Filtros principales de la página.
selected_year = st.selectbox(
    "Año",
    sorted(eu_data["year"].unique(), reverse=True)
)

selected_category = st.multiselect(
    "Categoría",
    options=sorted(eu_data["sector"].unique()),
    default=sorted(eu_data["sector"].unique())
)

filtered_data = eu_data[
    (eu_data["year"] == selected_year) &
    (eu_data["sector"].isin(selected_category))
].copy()


# ==========================================================
# KPIS DE MERCADO EUROPEO
# ==========================================================

market_value = filtered_data["import_value_usd"].sum()
avg_gdp = filtered_data["gdp_per_capita"].mean()
avg_import_pc = filtered_data["import_value_usd_per_capita"].mean()
countries_count = filtered_data["country"].nunique()

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)

with kpi_1:
    render_kpi("Valor importado UE", format_currency(market_value))

with kpi_2:
    render_kpi("PIB per cápita medio", format_currency(avg_gdp))

with kpi_3:
    render_kpi("Importación per cápita media", format_currency(avg_import_pc))

with kpi_4:
    render_kpi("Países analizados", countries_count)


# ==========================================================
# ANÁLISIS VISUAL
# ==========================================================

st.markdown("## Relación entre poder adquisitivo e importación per cápita")

scatter_data = (
    filtered_data.groupby(["country"], as_index=False)
    .agg(
        gdp_per_capita=("gdp_per_capita", "mean"),
        import_value_usd_per_capita=("import_value_usd_per_capita", "mean"),
        import_value_usd=("import_value_usd", "sum"),
        population=("population", "mean")
    )
)

fig_scatter = px.scatter(
    scatter_data,
    x="gdp_per_capita",
    y="import_value_usd_per_capita",
    size="import_value_usd",
    hover_name="country",
    labels={
        "gdp_per_capita": "PIB per cápita (USD)",
        "import_value_usd_per_capita": "Importación per cápita (USD)",
        "import_value_usd": "Valor importado"
    },
    color_discrete_sequence=[VELLUTO_GOLD]
)

fig_scatter.update_layout(
    paper_bgcolor=VELLUTO_BACKGROUND,
    plot_bgcolor=VELLUTO_WHITE
)

st.plotly_chart(fig_scatter, use_container_width=True)


st.markdown("## Ranking europeo por importación per cápita")

ranking_pc = (
    scatter_data.sort_values("import_value_usd_per_capita", ascending=True)
    .tail(15)
)

fig_ranking_pc = px.bar(
    ranking_pc,
    x="import_value_usd_per_capita",
    y="country",
    orientation="h",
    color_discrete_sequence=[VELLUTO_GREEN],
    labels={
        "import_value_usd_per_capita": "Importación per cápita (USD)",
        "country": "País"
    }
)

fig_ranking_pc.update_layout(
    paper_bgcolor=VELLUTO_BACKGROUND,
    plot_bgcolor=VELLUTO_WHITE,
    yaxis_title="País",
    xaxis_title="Importación per cápita (USD)"
)

st.plotly_chart(fig_ranking_pc, use_container_width=True)