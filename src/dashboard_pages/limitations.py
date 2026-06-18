import streamlit as st


# ==========================================================
# LIMITACIONES Y SESGOS
# ----------------------------------------------------------
# Esta vista documenta las principales limitaciones del análisis.
#
# El objetivo es aportar transparencia metodológica y evitar
# interpretaciones incorrectas de los resultados.
# ==========================================================


def render_limitations():
    """
    Renderiza la página de limitaciones y sesgos.
    """

    st.markdown("## Limitaciones y sesgos")

    st.markdown(
        """
        <div class="section-card">
            Ningún dataset representa perfectamente la realidad del mercado.
            Por este motivo, los resultados deben interpretarse como una herramienta
            de apoyo a la decisión y no como una predicción exacta del comportamiento futuro.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # SESGOS DEL COMERCIO INTERNACIONAL
    # ------------------------------------------------------

    st.markdown("### Comercio internacional ≠ consumo real")

    st.info(
        """
        Las importaciones no representan necesariamente el consumo final.

        Algunos países importan productos para transformarlos,
        redistribuirlos o reexportarlos posteriormente.
        """
    )

    # ------------------------------------------------------
    # HUBS LOGÍSTICOS
    # ------------------------------------------------------

    st.markdown("### Países con función logística")

    st.info(
        """
        Mercados como Países Bajos o Bélgica pueden registrar volúmenes
        de importación superiores a su consumo interno debido a su papel
        como centros logísticos europeos.
        """
    )

    # ------------------------------------------------------
    # LIMITACIONES DEL PRECIO MEDIO
    # ------------------------------------------------------

    st.markdown("### Interpretación del precio medio")

    st.info(
        """
        El precio medio por kilogramo no mide calidad.

        Las diferencias observadas pueden deberse a:
        - Mezclas de productos.
        - Diferentes grados de transformación.
        - Distintas cadenas de suministro.
        - Efectos de inflación o tipo de cambio.
        """
    )

    # ------------------------------------------------------
    # BLUE OCEAN SCORE
    # ------------------------------------------------------

    st.markdown("### Limitaciones del Blue Ocean Score")

    st.info(
        """
        El Blue Ocean Score es un indicador propio diseñado para priorizar mercados.

        No representa una medida oficial ni una predicción de ventas.

        Su utilidad principal consiste en comparar oportunidades relativas
        entre países utilizando criterios homogéneos.
        """
    )

    # ------------------------------------------------------
    # COBERTURA TEMPORAL
    # ------------------------------------------------------

    st.markdown("### Cobertura temporal")

    st.info(
        """
        El análisis principal utiliza el periodo 2020-2024.

        El año 2025 se excluye del dataset europeo enriquecido debido
        a la ausencia de indicadores socioeconómicos completos en World Bank.
        """
    )

    # ------------------------------------------------------
    # CONCLUSIÓN
    # ------------------------------------------------------

    st.markdown("### Conclusión metodológica")

    st.success(
        """
        A pesar de estas limitaciones, la combinación de comercio internacional,
        población y PIB per cápita proporciona una aproximación sólida para
        identificar mercados potencialmente atractivos para la expansión de Velluto.
        """
    )