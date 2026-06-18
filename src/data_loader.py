import pandas as pd
import streamlit as st
from pathlib import Path


# ==========================================================
# CARGA DE DATOS
# ----------------------------------------------------------
# Centralizamos aquí la lectura de datasets para no repetir rutas
# ni lógica de carga en cada página del dashboard.
# ==========================================================

@st.cache_data
def load_data():
    """
    Carga los dos datasets procesados del proyecto.

    - eu_data: dataset europeo enriquecido con población y PIB per cápita.
    - global_data: dataset global utilizado como benchmark internacional.

    El decorador st.cache_data evita recargar los CSV cada vez que
    el usuario cambia un filtro.
    """

    eu_path = Path("data/processed/trade_enriched_complete_2020_2024.csv")
    global_path = Path("data/processed/trade_global_2020_2025.csv")

    eu_data = pd.read_csv(eu_path)
    global_data = pd.read_csv(global_path)

    return eu_data, global_data