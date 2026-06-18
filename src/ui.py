import streamlit as st
from pathlib import Path


# ==========================================================
# PALETA CORPORATIVA VELLUTO
# ----------------------------------------------------------
# Centralizamos los colores de marca para reutilizarlos
# en todas las páginas del dashboard.
# ==========================================================

VELLUTO_GOLD = "#B48D57"
VELLUTO_SECONDARY_GOLD = "#856F4A"
VELLUTO_BLACK = "#101820"
VELLUTO_LOGO_BLACK = "#0B0D0E"
VELLUTO_CREAM = "#D9D4CF"
VELLUTO_BACKGROUND = "#F7F3EE"
VELLUTO_WHITE = "#FFFFFF"
VELLUTO_GREEN = "#556B4D"


def apply_velluto_style():
    """
    Aplica los estilos visuales corporativos de Velluto.

    Esta función evita repetir CSS en cada página del dashboard.
    """
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

        span[data-baseweb="tag"] {{
            background-color: {VELLUTO_GOLD} !important;
            color: {VELLUTO_WHITE} !important;
        }}

        /* Ajuste de textos en selectbox y multiselect */
        div[data-baseweb="select"] span {{
            color: {VELLUTO_BLACK} !important;
        }}

        div[data-baseweb="select"] input {{
            color: {VELLUTO_BLACK} !important;
        }}

        /* Título del menú más visible que el bloque de filtros */
        .sidebar-menu-title {{
            font-size: 1.35rem;
            font-weight: 800;
            color: {VELLUTO_GOLD};
            margin-top: 1rem;
            margin-bottom: 0.8rem;
        }}

        /* Forzamos texto oscuro dentro de selectbox/multiselect */
        div[data-baseweb="select"] span {{
            color: {VELLUTO_BLACK} !important;
        }}

        div[data-baseweb="select"] input {{
            color: {VELLUTO_BLACK} !important;
        }}

        /* Selector de vista del análisis */
        div[data-baseweb="select"] > div {{
            background-color: {VELLUTO_WHITE} !important;
            border: 1px solid {VELLUTO_GOLD} !important;
        }}

        div[data-baseweb="select"] span {{
            color: {VELLUTO_BLACK} !important;
        }}

        div[data-baseweb="select"] input {{
            color: {VELLUTO_BLACK} !important;
        }}

        div[data-baseweb="popover"] {{
            background-color: {VELLUTO_WHITE} !important;
        }}

        div[data-baseweb="menu"] {{
            background-color: {VELLUTO_WHITE} !important;
        }}

        div[role="option"] {{
            color: {VELLUTO_BLACK} !important;
            background-color: {VELLUTO_WHITE} !important;
        }}

        div[role="option"]:hover {{
            background-color: {VELLUTO_CREAM} !important;
            color: {VELLUTO_BLACK} !important;
        }}

        /* Texto seleccionado dentro de selectbox */
        div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] {{
            color: {VELLUTO_BLACK} !important;
        }}

        div[data-baseweb="select"] div {{
            color: {VELLUTO_BLACK} !important;
        }}

        div[data-baseweb="select"] span {{
            color: {VELLUTO_BLACK} !important;
        }}

        div[data-baseweb="select"] input {{
            color: {VELLUTO_BLACK} !important;
            -webkit-text-fill-color: {VELLUTO_BLACK} !important;
        }}

        div[data-baseweb="select"] svg {{
            color: {VELLUTO_SECONDARY_GOLD} !important;
            fill: {VELLUTO_SECONDARY_GOLD} !important;
        }}

        /* ==========================================================
       TARJETAS PARA LIMITACIONES Y SESGOS
       ----------------------------------------------------------
       Variante visual alineada con la identidad Velluto.
       Se utiliza en la página de Limitaciones para sustituir
       los componentes azules por tarjetas corporativas.
       ========================================================== */

        .bias-card {{
        background-color: {VELLUTO_WHITE};
        border-left: 6px solid {VELLUTO_GOLD};
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }}

        </style>
        """,
        unsafe_allow_html=True
    )


def render_sidebar_brand():
    """
    Renderiza el logo y la marca en la sidebar.
    """
    logo_path = Path("assets/images/velluto_logo.png")

    if logo_path.exists():
        st.sidebar.image(str(logo_path), use_container_width=True)

    st.sidebar.markdown(
        """
        <div class="brand-subtitle">Café de Origen · Market Intelligence</div>
        """,
        unsafe_allow_html=True
    )


def render_navigation():
    """
    Renderiza el menú interno del dashboard.

    Usamos este menú en lugar del sistema multipágina nativo de Streamlit
    para mantener el control visual de la sidebar.
    """
    st.sidebar.markdown(
    '<div class="sidebar-menu-title">Menú</div>',
    unsafe_allow_html=True
)

    selected_page = st.sidebar.selectbox(
    "Vista de análisis",
        [
            "Resumen ejecutivo",
            "Mercado europeo",
            "Café vs cacao",
            "Blue Ocean Score",
            "Limitaciones y sesgos"
        ]
    )

    return selected_page


def render_main_header():
    """
    Renderiza la cabecera principal del dashboard.
    """
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


def render_intro_card():
    """
    Renderiza el texto introductorio general del dashboard.
    """
    st.markdown(
        """
        <div class="section-card">
            Este dashboard analiza las importaciones de café y cacao para identificar mercados atractivos,
            comparar categorías de producto y contextualizar las oportunidades europeas frente al mercado global.
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi(label, value):
    """
    Renderiza una tarjeta KPI con estética corporativa.
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

def render_download_button(data, file_name):
    """
    Renderiza un botón para descargar los datos filtrados.

    El usuario descarga exactamente el dataframe que está viendo
    según los filtros aplicados en el dashboard.
    """

    csv_data = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar datos filtrados",
        data=csv_data,
        file_name=file_name,
        mime="text/csv"
    )