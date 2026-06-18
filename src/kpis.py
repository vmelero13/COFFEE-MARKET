import pandas as pd
import numpy as np


# ==========================================================
# FORMATO DE VALORES
# ----------------------------------------------------------
# Estas funciones convierten valores grandes en formatos legibles
# para los KPIs del dashboard.
# ==========================================================

def format_currency(value):
    """
    Formatea importes monetarios adaptando la unidad al tamaño del valor.

    Ejemplos:
    - 2.500.000.000 -> $2.50 B
    - 35.000.000 -> $35.00 M
    - 750.000 -> $750.0 K
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


def format_weight(value):
    """
    Formatea el volumen importado adaptando la unidad al tamaño del valor.

    Esto evita que países pequeños aparezcan como 0.0 M kg.
    """

    if pd.isna(value):
        return "N/A"

    if value >= 1_000_000:
        return f"{value / 1_000_000:,.1f} M kg"

    if value >= 1_000:
        return f"{value / 1_000:,.1f} K kg"

    return f"{value:,.0f} kg"


# ==========================================================
# CÁLCULO DE KPIS
# ----------------------------------------------------------
# Funciones reutilizables para calcular indicadores principales
# a partir del dataframe filtrado.
# ==========================================================

def calculate_summary_kpis(data):
    """
    Calcula los KPIs principales del dashboard.

    Se espera recibir un dataframe ya filtrado por año, categoría,
    producto, país o cualquier otro filtro activo.
    """

    total_import_value = data["import_value_usd"].sum()
    total_weight = data["net_weight_kg"].sum(skipna=True)
    avg_price = data["avg_price_usd_kg"].replace([np.inf, -np.inf], np.nan).mean()
    countries_count = data["country"].nunique()

    if not data.empty:
        leader_country = (
            data.groupby("country")["import_value_usd"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )
    else:
        leader_country = "N/A"

    return {
        "total_import_value": total_import_value,
        "total_weight": total_weight,
        "avg_price": avg_price,
        "countries_count": countries_count,
        "leader_country": leader_country
    }