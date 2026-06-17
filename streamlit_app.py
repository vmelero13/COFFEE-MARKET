import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path


# Configuración general de la página.
st.set_page_config(
    page_title="Análisis del Mercado del Café",
    page_icon="☕",
    layout="wide"
)


# Paleta visual inspirada en la identidad de Velluto.
VELLUTO_GOLD = "#B48D57"
VELLUTO_SECONDARY_GOLD = "#856F4A"
VELLUTO_BLACK = "#101820"
VELLUTO_LOGO_BLACK = "#0B0D0E"
VELLUTO_CREAM = "#D9D4CF"
VELLUTO_BACKGROUND = "#F7F3EE"
VELLUTO_WHITE = "#FFFFFF"


# ==========================================================
# ESTILOS CORPORATIVOS VELLUTO
# ----------------------------------------------------------
# Se personaliza Streamlit para adaptar la aplicación
# a la identidad visual de la marca:
#
# - Negro corporativo para sidebar
# - Dorado para elementos destacados
# - Fondo crema para mejorar legibilidad
# - Tarjetas KPI con estética premium
# ==========================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {VELLUTO_BACKGROUND};
        color: {VELLUTO_BLACK};
    }}

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {{
        background-color: {VELLUTO_LOGO_BLACK} !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: {VELLUTO_CREAM};
    }}

    h1, h2, h3 {{
        color: {VELLUTO_BLACK};
    }}

    .main-header {{
        background-color: {VELLUTO_WHITE};
        padding: 2rem;
        border-radius: 18px;
        border-left: 8px solid {VELLUTO_GOLD};
        margin-bottom: 1.5rem;
    }}

    .main-title {{
        font-size: 2.4rem;
        font-weight: 800;
        color: {VELLUTO_BLACK};
        margin-bottom: 0.3rem;
    }}

    .main-subtitle {{
        font-size: 1.05rem;
        color: {VELLUTO_SECONDARY_GOLD};
        margin-bottom: 0;
    }}

    .section-card {{
        background-color: {VELLUTO_WHITE};
        padding: 1.4rem;
        border-radius: 16px;
        border: 1px solid {VELLUTO_CREAM};
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

    .brand-name {{
        font-size: 1.25rem;
        font-weight: 800;
        color: {VELLUTO_GOLD};
        text-align: center;
        margin-top: 0.5rem;
    }}

    .brand-subtitle {{
        font-size: 0.85rem;
        color: {VELLUTO_CREAM};
        text-align: center;
        margin-bottom: 1.2rem;
    }}

    .small-note {{
        color: {VELLUTO_SECONDARY_GOLD};
        font-size: 0.9rem;
    }}

    /* Chips seleccionados en filtros multiselección */
    span[data-baseweb="tag"] {{
        background-color: {VELLUTO_GOLD} !important;
        color: {VELLUTO_WHITE} !important;
    }}

    /* Color del borde al enfocar inputs */
    div[data-baseweb="select"] > div {{
        border-color: {VELLUTO_GOLD} !important;
    }}

    /* Ajuste visual de botones de radio */
    label[data-baseweb="radio"] div {{
        border-color: {VELLUTO_GOLD} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    """
    Carga los datasets procesados del proyecto.

    El dataset europeo está enriquecido con población y PIB per cápita.
    El dataset global se utiliza como benchmark internacional de comercio.
    """
    eu_path = Path("data/processed/trade_enriched_complete_2020_2024.csv")
    global_path = Path("data/processed/trade_global_2020_2025.csv")

    eu_data = pd.read_csv(eu_path)
    global_data = pd.read_csv(global_path)

    return eu_data, global_data


def format_weight(value):
    """
    Formatea el volumen importado según el tamaño del valor.

    Esto evita que países pequeños aparezcan como 0.0 M kg
    cuando tienen importaciones relevantes pero de menor escala.
    """
    if pd.isna(value):
        return "N/A"

    if value >= 1_000_000:
        return f"{value / 1_000_000:,.1f} M kg"

    if value >= 1_000:
        return f"{value / 1_000:,.1f} K kg"

    return f"{value:,.0f} kg"


def format_currency(value):
    """
    Formatea importes monetarios adaptando automáticamente
    la unidad al tamaño del valor.
    """

    if pd.isna(value):
        return "N/A"

    # Billones americanos (Billions)
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f} B"

    # Millones
    if value >= 1_000_000:
        return f"${value / 1_000_000:,.2f} M"

    # Miles
    if value >= 1_000:
        return f"${value / 1_000:,.1f} K"

    return f"${value:,.0f}"


def render_kpi(label, value):
    """Renderiza una tarjeta KPI con estética corporativa."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Carga inicial de datos.
eu_data, global_data = load_data()


# Sidebar de marca.
logo_path = Path("assets/images/velluto_logo.png")

if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

st.sidebar.markdown(
    """
    <div class="brand-name">VELLUTO</div>
    <div class="brand-subtitle">Café de Origen · Market Intelligence</div>
    """,
    unsafe_allow_html=True
)


# Filtros principales.
st.sidebar.header("Filtros")

analysis_scope = st.sidebar.radio(
    "Ámbito del análisis",
    ["Unión Europea", "Global"],
    index=0
)

active_data = eu_data if analysis_scope == "Unión Europea" else global_data

selected_years = st.sidebar.multiselect(
    "Año",
    options=sorted(active_data["year"].dropna().unique(), reverse=True),
    default=sorted(active_data["year"].dropna().unique(), reverse=True)
)

selected_categories = st.sidebar.multiselect(
    "Categoría",
    options=sorted(active_data["sector"].dropna().unique()),
    default=sorted(active_data["sector"].dropna().unique())
)

selected_products = st.sidebar.multiselect(
    "Producto",
    options=sorted(active_data["product_group"].dropna().unique()),
    default=sorted(active_data["product_group"].dropna().unique())
)

selected_countries = st.sidebar.multiselect(
    "País",
    options=sorted(active_data["country"].dropna().unique()),
    default=[]
)


# Filtros avanzados solo disponibles para Unión Europea.
if analysis_scope == "Unión Europea":
    selected_gdp_range = st.sidebar.slider(
        "Rango de PIB per cápita",
        min_value=int(eu_data["gdp_per_capita"].min()),
        max_value=int(eu_data["gdp_per_capita"].max()),
        value=(
            int(eu_data["gdp_per_capita"].min()),
            int(eu_data["gdp_per_capita"].max())
        )
    )

    selected_population_range = st.sidebar.slider(
        "Rango de población",
        min_value=int(eu_data["population"].min()),
        max_value=int(eu_data["population"].max()),
        value=(
            int(eu_data["population"].min()),
            int(eu_data["population"].max())
        )
    )


# Aplicación de filtros.
filtered_data = active_data[
    (active_data["year"].isin(selected_years)) &
    (active_data["sector"].isin(selected_categories)) &
    (active_data["product_group"].isin(selected_products))
].copy()

if selected_countries:
    filtered_data = filtered_data[
        filtered_data["country"].isin(selected_countries)
    ]

if analysis_scope == "Unión Europea":
    filtered_data = filtered_data[
        (filtered_data["gdp_per_capita"].between(*selected_gdp_range)) &
        (filtered_data["population"].between(*selected_population_range))
    ]


# Cabecera principal.
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">Análisis del Mercado del Café</div>
        <p class="main-subtitle">
            Estudio estratégico para Velluto Café de Origen · Café, cacao y oportunidades de expansión
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-card">
        Este dashboard analiza las importaciones de café y cacao para identificar mercados atractivos,
        comparar categorías de producto y contextualizar las oportunidades europeas frente al mercado global.
    </div>
    """,
    unsafe_allow_html=True
)


# KPIs superiores.
st.markdown("## Resumen ejecutivo")

total_import_value = filtered_data["import_value_usd"].sum()
total_weight = filtered_data["net_weight_kg"].sum(skipna=True)
avg_price = filtered_data["avg_price_usd_kg"].replace([np.inf, -np.inf], np.nan).mean()
countries_count = filtered_data["country"].nunique()

leader_country = (
    filtered_data.groupby("country")["import_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
    if not filtered_data.empty else "N/A"
)

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)

with kpi_1:
    render_kpi("Valor importado", format_currency(total_import_value))

with kpi_2:
    render_kpi("Volumen importado", format_weight(total_weight))

with kpi_3:
    render_kpi("Precio medio", f"${avg_price:,.2f}/kg" if not np.isnan(avg_price) else "N/A")

with kpi_4:
    render_kpi("Países analizados", f"{countries_count}")

with kpi_5:
    render_kpi("Mercado líder", leader_country)


# Mapa de calor de importaciones.
st.markdown("## Mapa de importaciones")

map_data = (
    filtered_data.groupby(["country_code", "country"], as_index=False)
    .agg(import_value_usd=("import_value_usd", "sum"))
)

map_data["import_value_log"] = np.log10(map_data["import_value_usd"] + 1)

fig_map = px.choropleth(
    map_data,
    locations="country_code",
    locationmode="ISO-3",
    color="import_value_log",
    hover_name="country",
    hover_data={
        "import_value_usd": ":,.0f",
        "import_value_log": False
    },
    color_continuous_scale=[
        VELLUTO_CREAM,
        VELLUTO_GOLD,
        VELLUTO_SECONDARY_GOLD,
        VELLUTO_BLACK
    ],
    labels={"import_value_log": "Intensidad importadora"}
)

fig_map.update_layout(
    margin=dict(l=0, r=0, t=20, b=0),
    paper_bgcolor=VELLUTO_BACKGROUND,
    plot_bgcolor=VELLUTO_BACKGROUND,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth"
    )
)

st.plotly_chart(fig_map, use_container_width=True)


# Ranking de mercados.
st.markdown("## Ranking de mercados")

ranking_data = (
    filtered_data.groupby("country", as_index=False)
    .agg(import_value_usd=("import_value_usd", "sum"))
    .sort_values("import_value_usd", ascending=True)
    .tail(15)
)

fig_ranking = px.bar(
    ranking_data,
    x="import_value_usd",
    y="country",
    orientation="h",
    color_discrete_sequence=[VELLUTO_GOLD],
    labels={
        "import_value_usd": "Valor importado (USD)",
        "country": "País"
    }
)

fig_ranking.update_layout(
    paper_bgcolor=VELLUTO_BACKGROUND,
    plot_bgcolor=VELLUTO_WHITE,
    margin=dict(l=0, r=0, t=20, b=0),
    yaxis_title="País",
    xaxis_title="Valor importado (USD)"
)

st.plotly_chart(fig_ranking, use_container_width=True)


# Tabla de datos filtrados.
st.markdown("## Datos filtrados")

st.dataframe(
    filtered_data,
    use_container_width=True
)

st.markdown(
    f"""
    <p class="small-note">
        Registros mostrados: <strong>{filtered_data.shape[0]}</strong>
    </p>
    """,
    unsafe_allow_html=True
)