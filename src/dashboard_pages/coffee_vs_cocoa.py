import pandas as pd
import streamlit as st
import plotly.express as px

from src.ui import (
    VELLUTO_BACKGROUND,
    VELLUTO_GOLD,
    VELLUTO_SECONDARY_GOLD,
    VELLUTO_WHITE,
    VELLUTO_GREEN,
    render_kpi
)

from src.kpis import format_currency, format_weight


# ==========================================================
# CAFÉ VS CACAO
# ----------------------------------------------------------
# Compara el comportamiento del café frente al cacao y sus derivados.
# La vista sirve para entender diferencias de tamaño, evolución,
# precio medio y peso relativo de Europa frente al resto del mundo.
# ==========================================================

def render_coffee_vs_cocoa(filtered_data, eu_data, global_data):
    """
    Renderiza la vista comparativa entre café y cacao.

    filtered_data llega ya filtrado desde la sidebar.
    eu_data y global_data se utilizan para comparar Europa con el mercado global.
    """

    st.markdown("## Café vs cacao")

    st.markdown(
        """
        <div class="section-card">
            Comparativa estratégica entre café y cacao para evaluar el peso relativo de ambas categorías,
            su evolución temporal y la posición de Europa frente al mercado global.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # KPIS COMPARATIVOS
    # ------------------------------------------------------

    coffee_data = filtered_data[filtered_data["sector"] == "Coffee"]
    cocoa_data = filtered_data[filtered_data["sector"] == "Cocoa"]

    coffee_value = coffee_data["import_value_usd"].sum()
    cocoa_value = cocoa_data["import_value_usd"].sum()

    coffee_weight = coffee_data["net_weight_kg"].sum(skipna=True)
    cocoa_weight = cocoa_data["net_weight_kg"].sum(skipna=True)

    coffee_leader = (
        coffee_data.groupby("country")["import_value_usd"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
        if not coffee_data.empty else "N/A"
    )

    cocoa_leader = (
        cocoa_data.groupby("country")["import_value_usd"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
        if not cocoa_data.empty else "N/A"
    )

    # Precio medio del mercado actualmente seleccionado por los filtros.
    selected_market_price = (
        filtered_data["avg_price_usd_kg"]
        .replace([float("inf"), float("-inf")], pd.NA)
        .mean()
    )

    kpi_1, kpi_2, kpi_3, kpi_4, kpi_5, kpi_6, kpi_7 = st.columns(7)

    with kpi_1:
        render_kpi("Valor café", format_currency(coffee_value))

    with kpi_2:
        render_kpi("Valor cacao", format_currency(cocoa_value))

    with kpi_3:
        render_kpi("Volumen café", format_weight(coffee_weight))

    with kpi_4:
        render_kpi("Volumen cacao", format_weight(cocoa_weight))

    with kpi_5:
        render_kpi("Líder café", coffee_leader)

    with kpi_6:
        render_kpi("Líder cacao", cocoa_leader)
    
    with kpi_7:
        render_kpi(
            "Precio medio seleccionado",
            f"${selected_market_price:,.2f}/kg"
            if pd.notna(selected_market_price) else "N/A"
        )

    # ------------------------------------------------------
    # EVOLUCIÓN TEMPORAL CAFÉ VS CACAO
    # ------------------------------------------------------

    st.markdown("## Evolución temporal del valor importado")

    trend_data = (
        filtered_data.groupby(["year", "sector"], as_index=False)
        .agg(import_value_usd=("import_value_usd", "sum"))
    )

    fig_trend = px.line(
        trend_data,
        x="year",
        y="import_value_usd",
        color="sector",
        markers=True,
        color_discrete_map={
            "Coffee": VELLUTO_GOLD,
            "Cocoa": VELLUTO_GREEN
        },
        labels={
            "year": "Año",
            "sector": "Categoría",
            "import_value_usd": "Valor importado (USD)"
        }
    )

    fig_trend.update_layout(
        paper_bgcolor=VELLUTO_BACKGROUND,
        plot_bgcolor=VELLUTO_WHITE,
        xaxis_title="Año",
        yaxis_title="Valor importado (USD)",
        legend_title="Categoría"
    )

    fig_trend.update_xaxes(
        tickmode="array",
        tickvals=sorted(trend_data["year"].dropna().unique())
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    # ------------------------------------------------------
    # EUROPA VS RESTO DEL MUNDO POR AÑO
    # ------------------------------------------------------

    st.markdown("## Evolución del valor importado: Europa vs Mercado global")

    eu_country_codes = eu_data["country_code"].dropna().unique()
    global_comparison = global_data.copy()

    global_comparison["market_area"] = global_comparison["country_code"].apply(
        lambda country_code: "Unión Europea"
        if country_code in eu_country_codes
        else "Resto del mundo"
    )

    comparison_data = (
        global_comparison.groupby(["year", "sector", "market_area"], as_index=False)
        .agg(import_value_usd=("import_value_usd", "sum"))
    )

    fig_comparison = px.line(
        comparison_data,
        x="year",
        y="import_value_usd",
        color="market_area",
        line_dash="sector",
        markers=True,
        color_discrete_map={
            "Unión Europea": VELLUTO_GOLD,
            "Resto del mundo": VELLUTO_GREEN
        },
        labels={
            "year": "Año",
            "import_value_usd": "Valor importado (USD)",
            "market_area": "Área",
            "sector": "Categoría"
        }
    )

    fig_comparison.update_layout(
        paper_bgcolor=VELLUTO_BACKGROUND,
        plot_bgcolor=VELLUTO_WHITE,
        xaxis_title="Año",
        yaxis_title="Valor importado (USD)",
        legend_title="Área / Categoría"
    )

    fig_comparison.update_xaxes(
        tickmode="array",
        tickvals=sorted(comparison_data["year"].dropna().unique())
    )

    st.plotly_chart(fig_comparison, use_container_width=True)

    # ------------------------------------------------------
    # EVOLUCIÓN DEL PRECIO MEDIO: EUROPA VS GLOBAL
    # ------------------------------------------------------
    # Se compara el precio medio por kilogramo entre:
    #
    # - Unión Europea
    # - Mercado global
    #
    # La comparación permite detectar si Europa paga una prima
    # de precio respecto al mercado mundial en café, cacao o derivados.
    # ------------------------------------------------------

    st.markdown("## Evolución del precio medio por kilogramo: Europa vs Mercado global")

    eu_price_data = eu_data.copy()
    eu_price_data["market_area"] = "Unión Europea"

    global_price_data = global_data.copy()
    global_price_data["market_area"] = "Global"

    price_comparison_data = pd.concat(
        [
            eu_price_data,
            global_price_data
        ],
        ignore_index=True
    )

    price_trend_data = (
        price_comparison_data.groupby(
            ["year", "product_group", "market_area"],
            as_index=False
        )
        .agg(avg_price_usd_kg=("avg_price_usd_kg", "mean"))
    )

    fig_price = px.line(
        price_trend_data,
        x="year",
        y="avg_price_usd_kg",
        color="product_group",
        line_dash="market_area",
        markers=True,
        color_discrete_sequence=[
            VELLUTO_GOLD,
            VELLUTO_GREEN,
            VELLUTO_SECONDARY_GOLD
        ],
        labels={
            "year": "Año",
            "avg_price_usd_kg": "Precio medio (USD/kg)",
            "product_group": "Producto",
            "market_area": "Área"
        }
    )

    fig_price.update_layout(
        paper_bgcolor=VELLUTO_BACKGROUND,
        plot_bgcolor=VELLUTO_WHITE,
        xaxis_title="Año",
        yaxis_title="Precio medio (USD/kg)",
        legend_title="Producto / Área"
    )

    fig_price.update_xaxes(
        tickmode="array",
        tickvals=sorted(price_trend_data["year"].dropna().unique())
    )

    st.plotly_chart(fig_price, use_container_width=True)

    # ------------------------------------------------------
    # LECTURA ESTRATÉGICA
    # ------------------------------------------------------

    st.markdown("## Lectura estratégica")

    st.markdown(
        """
        <div class="section-card">
            El análisis muestra cómo se comportan café y cacao en términos de valor,
            volumen y precio medio. Para Velluto, esta comparación permite entender
            si el cacao actúa como categoría complementaria, referencia premium o
            alternativa estratégica en mercados sensibles al origen, la calidad y el valor percibido.
        </div>
        """,
        unsafe_allow_html=True
    )