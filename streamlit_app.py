import streamlit as st

from src.ui import (
    apply_velluto_style,
    render_sidebar_brand,
    render_navigation,
    render_main_header,
    render_intro_card
)

from src.data_loader import load_data

from src.filters import (
    render_global_filters,
    render_european_filters
)

from src.dashboard_pages.executive_summary import render_executive_summary
from src.dashboard_pages.european_market import render_european_market
from src.dashboard_pages.coffee_vs_cocoa import render_coffee_vs_cocoa
from src.dashboard_pages.blue_ocean import render_blue_ocean
from src.dashboard_pages.limitations import render_limitations


# ==========================================================
# CONFIGURACIÓN GENERAL DE LA APP
# ----------------------------------------------------------
# Este archivo funciona como controlador principal del dashboard.
# Desde aquí se cargan los datos, se aplica la identidad visual,
# se renderiza la navegación y se llama a cada vista del análisis.
# ==========================================================

st.set_page_config(
    page_title="Velluto Market Intelligence",
    page_icon="☕",
    layout="wide"
)


# ==========================================================
# ESTILO Y DATOS
# ==========================================================

apply_velluto_style()

eu_data, global_data = load_data()


# ==========================================================
# SIDEBAR
# ----------------------------------------------------------
# La sidebar contiene:
# - Logo y marca Velluto
# - Menú interno del dashboard
# - Filtros dinámicos según la vista seleccionada
# ==========================================================

render_sidebar_brand()

selected_page = render_navigation()


# ==========================================================
# CABECERA GENERAL
# ==========================================================

render_main_header()

if selected_page == "Resumen ejecutivo":
    render_intro_card()


# ==========================================================
# ROUTER INTERNO DEL DASHBOARD
# ----------------------------------------------------------
# En lugar de usar el sistema multipágina nativo de Streamlit,
# se usa una navegación interna controlada por el selector del sidebar.
# Esto evita que Streamlit coloque su menú automático por encima del logo.
# ==========================================================

if selected_page == "Resumen ejecutivo":
    filtered_data, analysis_scope = render_global_filters(
        eu_data,
        global_data
    )

    render_executive_summary(filtered_data)


elif selected_page == "Mercado europeo":
    filtered_data = render_european_filters(eu_data)

    render_european_market(filtered_data)


elif selected_page == "Café vs cacao":
    filtered_data, analysis_scope = render_global_filters(
        eu_data,
        global_data
    )

    render_coffee_vs_cocoa(
        filtered_data,
        eu_data,
        global_data
    )


elif selected_page == "Blue Ocean Score":
    filtered_data = render_european_filters(eu_data)

    render_blue_ocean(filtered_data)


elif selected_page == "Limitaciones y sesgos":
    render_limitations()