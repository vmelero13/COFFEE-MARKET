import streamlit as st


# ==========================================================
# FILTROS DEL DASHBOARD
# ----------------------------------------------------------
# Centralizamos aquí la lógica de filtros para evitar duplicarla
# en cada vista del dashboard.
# ==========================================================

def render_global_filters(eu_data, global_data):
    """
    Renderiza los filtros principales para el resumen ejecutivo.

    Esta vista permite elegir entre Unión Europea y Global.
    Los filtros socioeconómicos solo aparecen cuando el ámbito es Unión Europea.
    """

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

    filtered_data = active_data[
        (active_data["year"].isin(selected_years)) &
        (active_data["sector"].isin(selected_categories)) &
        (active_data["product_group"].isin(selected_products))
    ].copy()

    if selected_countries:
        filtered_data = filtered_data[
            filtered_data["country"].isin(selected_countries)
        ]

    # Los filtros de PIB y población solo se aplican cuando el usuario
    # está trabajando con el dataset europeo enriquecido.
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

        filtered_data = filtered_data[
            (filtered_data["gdp_per_capita"].between(*selected_gdp_range)) &
            (filtered_data["population"].between(*selected_population_range))
        ]

    return filtered_data, analysis_scope


def render_european_filters(eu_data):
    """
    Renderiza los filtros específicos para las vistas europeas.

    Aquí no se permite cambiar al dataset global porque estas vistas
    usan población, PIB per cápita y métricas per cápita.
    """

    st.sidebar.header("Filtros")

    selected_years = st.sidebar.multiselect(
        "Año",
        options=sorted(eu_data["year"].dropna().unique(), reverse=True),
        default=sorted(eu_data["year"].dropna().unique(), reverse=True)
    )

    selected_categories = st.sidebar.multiselect(
        "Categoría",
        options=sorted(eu_data["sector"].dropna().unique()),
        default=sorted(eu_data["sector"].dropna().unique())
    )

    selected_products = st.sidebar.multiselect(
        "Producto",
        options=sorted(eu_data["product_group"].dropna().unique()),
        default=sorted(eu_data["product_group"].dropna().unique())
    )

    selected_countries = st.sidebar.multiselect(
        "País",
        options=sorted(eu_data["country"].dropna().unique()),
        default=[]
    )

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

    filtered_data = eu_data[
        (eu_data["year"].isin(selected_years)) &
        (eu_data["sector"].isin(selected_categories)) &
        (eu_data["product_group"].isin(selected_products)) &
        (eu_data["gdp_per_capita"].between(*selected_gdp_range)) &
        (eu_data["population"].between(*selected_population_range))
    ].copy()

    if selected_countries:
        filtered_data = filtered_data[
            filtered_data["country"].isin(selected_countries)
        ]

    return filtered_data