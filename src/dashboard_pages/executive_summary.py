import streamlit as st
import numpy as np
import plotly.express as px

from src.ui import (
    VELLUTO_BACKGROUND,
    VELLUTO_CREAM,
    VELLUTO_GOLD,
    VELLUTO_SECONDARY_GOLD,
    VELLUTO_BLACK,
    VELLUTO_WHITE,
    render_kpi,
    render_download_button
)

from src.kpis import (
    calculate_summary_kpis,
    format_currency,
    format_weight
)


# ==========================================================
# RESUMEN EJECUTIVO
# ----------------------------------------------------------
# Esta vista funciona como portada analítica del dashboard.
# Resume el tamaño del mercado, los principales países importadores
# y la distribución geográfica de las importaciones.
# ==========================================================

def render_executive_summary(filtered_data):
    """
    Renderiza la vista de resumen ejecutivo.

    Recibe un dataframe ya filtrado desde la sidebar.
    """

    # ------------------------------------------------------
    # KPIS PRINCIPALES
    # ------------------------------------------------------
    # Los KPIs se calculan sobre los datos filtrados para que
    # respondan a la selección del usuario.
    # ------------------------------------------------------

    st.markdown("## Resumen ejecutivo")

    kpis = calculate_summary_kpis(filtered_data)

    kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)

    with kpi_1:
        render_kpi(
            "Valor importado",
            format_currency(kpis["total_import_value"])
        )

    with kpi_2:
        render_kpi(
            "Volumen importado",
            format_weight(kpis["total_weight"])
        )

    with kpi_3:
        avg_price = kpis["avg_price"]
        render_kpi(
            "Precio medio",
            f"${avg_price:,.2f}/kg" if not np.isnan(avg_price) else "N/A"
        )

    with kpi_4:
        render_kpi(
            "Países analizados",
            kpis["countries_count"]
        )

    with kpi_5:
        render_kpi(
            "Mercado líder",
            kpis["leader_country"]
        )

    # ------------------------------------------------------
    # MAPA DE IMPORTACIONES
    # ------------------------------------------------------
    # El mapa permite ver la distribución geográfica del valor
    # importado. Se utiliza escala logarítmica para evitar que los
    # grandes mercados oculten visualmente a los países pequeños.
    # ------------------------------------------------------

    st.markdown("## Mapa de importaciones")

    map_data = (
        filtered_data.groupby(["country_code", "country"], as_index=False)
        .agg(import_value_usd=("import_value_usd", "sum"))
    )

    map_data["import_value_log"] = np.log10(
        map_data["import_value_usd"] + 1
    )

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

    # ------------------------------------------------------
    # RANKING DE MERCADOS
    # ------------------------------------------------------
    # Muestra los principales países importadores del contexto
    # seleccionado por el usuario.
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # DESCARGA DE DATOS
    # ------------------------------------------------------
    # Permite descargar los datos resultantes de los filtros
    # aplicados en la vista de resumen ejecutivo.
    # ------------------------------------------------------

    render_download_button(
        filtered_data,
        "resumen_ejecutivo_datos_filtrados.csv"
    )