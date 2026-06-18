import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.ui import (
    VELLUTO_BACKGROUND,
    VELLUTO_GOLD,
    VELLUTO_GREEN,
    VELLUTO_SECONDARY_GOLD,
    VELLUTO_BLACK,
    VELLUTO_WHITE,
    render_kpi
)

from src.kpis import format_currency


# ==========================================================
# BLUE OCEAN SCORE
# ----------------------------------------------------------
# Esta vista construye un indicador propio para priorizar
# mercados europeos con potencial para Velluto.
#
# El score combina:
# - Importación per cápita
# - PIB per cápita
# - Crecimiento del valor importado
# - Menor saturación relativa del mercado
# ==========================================================

def normalize_series(series):
    """
    Normaliza una serie numérica en una escala 0-100.

    Si todos los valores son iguales, devuelve 50 para evitar
    divisiones por cero y mantener una escala neutra.
    """
    if series.max() == series.min():
        return pd.Series(50, index=series.index)

    return ((series - series.min()) / (series.max() - series.min())) * 100


def calculate_growth(data):
    """
    Calcula el crecimiento del valor importado por país.

    Se compara el primer año disponible con el último año disponible
    dentro del rango filtrado por el usuario.
    """
    yearly_data = (
        data.groupby(["country", "year"], as_index=False)
        .agg(import_value_usd=("import_value_usd", "sum"))
        .sort_values(["country", "year"])
    )

    growth_rows = []

    for country, country_data in yearly_data.groupby("country"):
        first_value = country_data.iloc[0]["import_value_usd"]
        last_value = country_data.iloc[-1]["import_value_usd"]

        if first_value > 0:
            growth = (last_value - first_value) / first_value
        else:
            growth = 0

        growth_rows.append(
            {
                "country": country,
                "growth_rate": growth
            }
        )

    return pd.DataFrame(growth_rows)


def render_blue_ocean(filtered_data):
    """
    Renderiza la vista Blue Ocean Score.

    Recibe un dataframe europeo ya filtrado desde la sidebar.
    """

    st.markdown("## Blue Ocean Score")

    st.markdown(
        """
        <div class="section-card">
            Ranking de oportunidad para priorizar países europeos con potencial de expansión.
            El indicador combina demanda relativa, poder adquisitivo, crecimiento y menor saturación
            del mercado importador.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # AGRUPACIÓN POR PAÍS
    # ------------------------------------------------------
    # Se construye una tabla país-país con las variables necesarias
    # para calcular el indicador.
    # ------------------------------------------------------

    country_data = (
        filtered_data.groupby(["country_code", "country"], as_index=False)
        .agg(
            import_value_usd=("import_value_usd", "sum"),
            import_value_usd_per_capita=("import_value_usd_per_capita", "mean"),
            net_weight_kg_per_capita=("net_weight_kg_per_capita", "mean"),
            gdp_per_capita=("gdp_per_capita", "mean"),
            population=("population", "mean")
        )
    )

    growth_data = calculate_growth(filtered_data)

    country_data = country_data.merge(
        growth_data,
        on="country",
        how="left"
    )

    country_data["growth_rate"] = country_data["growth_rate"].fillna(0)

    # ------------------------------------------------------
    # NORMALIZACIÓN DE VARIABLES
    # ------------------------------------------------------
    # Todas las variables se convierten a escala 0-100 para poder
    # combinarlas en un único indicador.
    # ------------------------------------------------------

    country_data["demand_score"] = normalize_series(
        country_data["import_value_usd_per_capita"]
    )

    country_data["income_score"] = normalize_series(
        country_data["gdp_per_capita"]
    )

    country_data["growth_score"] = normalize_series(
        country_data["growth_rate"]
    )

    country_data["saturation_score"] = 100 - normalize_series(
        country_data["import_value_usd"]
    )

    # ------------------------------------------------------
    # CÁLCULO DEL BLUE OCEAN SCORE
    # ------------------------------------------------------
    # Pesos utilizados:
    # - 30% demanda per cápita
    # - 25% PIB per cápita
    # - 25% crecimiento
    # - 20% menor saturación relativa
    # ------------------------------------------------------

    country_data["blue_ocean_score"] = (
        country_data["demand_score"] * 0.30 +
        country_data["income_score"] * 0.25 +
        country_data["growth_score"] * 0.25 +
        country_data["saturation_score"] * 0.20
    )

    country_data = country_data.sort_values(
        "blue_ocean_score",
        ascending=False
    )

    # ------------------------------------------------------
    # KPIS DEL SCORE
    # ------------------------------------------------------

    top_country = country_data.iloc[0]["country"] if not country_data.empty else "N/A"
    top_score = country_data.iloc[0]["blue_ocean_score"] if not country_data.empty else np.nan

    top_growth_country = (
        country_data.sort_values("growth_rate", ascending=False)
        .iloc[0]["country"]
        if not country_data.empty else "N/A"
    )

    avg_score = country_data["blue_ocean_score"].mean()

    kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)

    with kpi_1:
        render_kpi("Mejor oportunidad", top_country)

    with kpi_2:
        render_kpi(
            "Blue Ocean Score",
            f"{top_score:,.1f}" if not np.isnan(top_score) else "N/A"
        )

    with kpi_3:
        render_kpi("Mayor crecimiento", top_growth_country)

    with kpi_4:
        render_kpi(
            "Score medio",
            f"{avg_score:,.1f}" if not np.isnan(avg_score) else "N/A"
        )

    # ------------------------------------------------------
    # RANKING DE OPORTUNIDAD
    # ------------------------------------------------------

    st.markdown("## Ranking de oportunidad")

    ranking_data = country_data.sort_values(
        "blue_ocean_score",
        ascending=True
    ).tail(15)

    fig_ranking = px.bar(
        ranking_data,
        x="blue_ocean_score",
        y="country",
        orientation="h",
        color="blue_ocean_score",
        color_continuous_scale=[
            VELLUTO_SECONDARY_GOLD,
            VELLUTO_GOLD,
            VELLUTO_GREEN
        ],
        labels={
            "blue_ocean_score": "Blue Ocean Score",
            "country": "País"
        }
    )

    fig_ranking.update_layout(
        paper_bgcolor=VELLUTO_BACKGROUND,
        plot_bgcolor=VELLUTO_WHITE,
        xaxis_title="Blue Ocean Score",
        yaxis_title="País",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_ranking, use_container_width=True)

    # ------------------------------------------------------
    # MAPA EUROPEO DEL SCORE
    # ------------------------------------------------------

    st.markdown("## Mapa de oportunidad en Europa")

    fig_map = px.choropleth(
        country_data,
        locations="country_code",
        locationmode="ISO-3",
        color="blue_ocean_score",
        hover_name="country",
        hover_data={
            "blue_ocean_score": ":.1f",
            "import_value_usd": ":,.0f",
            "gdp_per_capita": ":,.0f",
            "growth_rate": ":.2%"
        },
        color_continuous_scale=[
            VELLUTO_SECONDARY_GOLD,
            VELLUTO_GOLD,
            VELLUTO_GREEN,
            VELLUTO_BLACK
        ],
        labels={"blue_ocean_score": "Blue Ocean Score"}
    )

    fig_map.update_layout(
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
    # RELACIÓN ENTRE RENTA Y OPORTUNIDAD
    # ------------------------------------------------------

    st.markdown("## Renta, demanda y oportunidad")

    fig_scatter = px.scatter(
        country_data,
        x="gdp_per_capita",
        y="import_value_usd_per_capita",
        size="import_value_usd",
        color="blue_ocean_score",
        hover_name="country",
        color_continuous_scale=[
            VELLUTO_SECONDARY_GOLD,
            VELLUTO_GOLD,
            VELLUTO_GREEN
        ],
        labels={
            "gdp_per_capita": "PIB per cápita (USD)",
            "import_value_usd_per_capita": "Importación per cápita (USD)",
            "blue_ocean_score": "Blue Ocean Score",
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
    # METODOLOGÍA
    # ------------------------------------------------------
    # Se explica el indicador en lenguaje ejecutivo.
    # El objetivo es que el usuario entienda la lógica del score
    # sin necesidad de revisar el código.
    # ------------------------------------------------------

    st.markdown("## Metodología del Blue Ocean Score")

    st.markdown(
        """
        <div class="section-card">
            El Blue Ocean Score es un indicador compuesto diseñado para identificar
            mercados europeos con potencial de expansión para Velluto.
            El modelo prioriza países que combinan señales favorables de demanda,
            capacidad adquisitiva, crecimiento reciente y menor saturación relativa.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Componentes del indicador")

    st.info(
        """
        El indicador combina cuatro variables normalizadas en escala 0-100:

        - 30% Importación per cápita.
        - 25% PIB per cápita.
        - 25% Crecimiento de las importaciones.
        - 20% Menor saturación relativa.
        """
    )

    st.markdown("### Interpretación")

    st.success(
        """
        Una puntuación elevada no implica necesariamente que el país sea el mayor mercado,
        sino que presenta una combinación atractiva de poder adquisitivo, intensidad importadora,
        crecimiento y espacio relativo para competir.
        """
    )