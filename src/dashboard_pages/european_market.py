import streamlit as st
import plotly.express as px

from src.ui import (
    VELLUTO_BACKGROUND,
    VELLUTO_CREAM,
    VELLUTO_GOLD,
    VELLUTO_GREEN,
    VELLUTO_SECONDARY_GOLD,
    VELLUTO_BLACK,
    VELLUTO_WHITE,
    render_kpi,
    render_download_button
)

from src.kpis import format_currency


# ==========================================================
# MERCADO EUROPEO
# ----------------------------------------------------------
# Esta vista analiza el mercado europeo desde una perspectiva
# de oportunidad, combinando tamaño de mercado, poder adquisitivo
# e intensidad importadora por habitante.
# ==========================================================

def render_european_market(filtered_data):
    """
    Renderiza la vista de mercado europeo.

    Recibe un dataframe europeo ya filtrado desde la sidebar.
    """

    st.markdown("## Mercado europeo")

    st.markdown(
        """
        <div class="section-card">
            Análisis del mercado europeo desde una perspectiva de oportunidad,
            combinando tamaño de mercado, poder adquisitivo e intensidad importadora por habitante.
        </div>
        """,
        unsafe_allow_html=True
    )

   # ------------------------------------------------------
    # KPIS EUROPEOS
    # ------------------------------------------------------
    # Se muestran indicadores principales del mercado europeo
    # según los filtros seleccionados por el usuario.
    # ------------------------------------------------------

    market_value = filtered_data["import_value_usd"].sum()
    avg_gdp = filtered_data["gdp_per_capita"].mean()
    avg_import_pc = filtered_data["import_value_usd_per_capita"].mean()
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
        render_kpi("Valor importado UE", format_currency(market_value))

    with kpi_2:
        render_kpi("PIB per cápita medio", format_currency(avg_gdp))

    with kpi_3:
        render_kpi("Importación per cápita media", format_currency(avg_import_pc))

    with kpi_4:
        render_kpi("Países analizados", countries_count)

    with kpi_5:
        render_kpi("Mercado líder", leader_country)

    # ------------------------------------------------------
    # MAPA EUROPEO DE CALOR
    # ------------------------------------------------------
    # Se muestra el valor importado por país dentro del contexto europeo.
    # El scope europe mejora el foco visual frente al mapa mundial.
    # ------------------------------------------------------

    st.markdown("## Mapa europeo de importaciones")

    map_data = (
        filtered_data.groupby(["country_code", "country"], as_index=False)
        .agg(import_value_usd=("import_value_usd", "sum"))
    )

    fig_map = px.choropleth(
        map_data,
        locations="country_code",
        locationmode="ISO-3",
        color="import_value_usd",
        hover_name="country",
        hover_data={"import_value_usd": ":,.0f"},
        color_continuous_scale=[
            VELLUTO_CREAM,
            VELLUTO_GOLD,
            VELLUTO_SECONDARY_GOLD,
            VELLUTO_BLACK
        ],
        labels={"import_value_usd": "Valor importado (USD)"}
    )

    fig_map.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor=VELLUTO_BACKGROUND,
        plot_bgcolor=VELLUTO_BACKGROUND,
        geo=dict(
            scope="europe",
            showframe=False,
            showcoastlines=True
        )
    )

    st.plotly_chart(fig_map, use_container_width=True)

    # ------------------------------------------------------
    # SCATTER DE OPORTUNIDAD
    # ------------------------------------------------------
    # Cruza PIB per cápita e importación per cápita.
    # La hipótesis es que países con mayor capacidad económica
    # e intensidad importadora pueden ser mercados atractivos.
    # ------------------------------------------------------

    st.markdown("## Poder adquisitivo vs importación per cápita")

    scatter_data = (
        filtered_data.groupby("country", as_index=False)
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
        color_discrete_sequence=[VELLUTO_GOLD],
        labels={
            "gdp_per_capita": "PIB per cápita (USD)",
            "import_value_usd_per_capita": "Importación per cápita (USD)",
            "import_value_usd": "Valor importado"
        }
    )

    fig_scatter.update_layout(
        paper_bgcolor=VELLUTO_BACKGROUND,
        plot_bgcolor=VELLUTO_WHITE,
        xaxis_title="PIB per cápita (USD)",
        yaxis_title="Importación per cápita (USD)"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    # ------------------------------------------------------
    # RANKING EUROPEO
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # DESCARGA DE DATOS
    # ------------------------------------------------------
    # Exporta los datos europeos filtrados utilizados
    # en esta vista.
    # ------------------------------------------------------

    render_download_button(
        filtered_data,
        "mercado_europeo_datos_filtrados.csv"
    )