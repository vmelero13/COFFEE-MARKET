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

    st.markdown(
        """
        <div class="section-card">
            <strong>Importaciones ≠ consumo final</strong><br><br>
            Las importaciones no representan necesariamente el consumo final.<br><br>
            Algunos países importan productos para transformarlos,
            redistribuirlos o reexportarlos posteriormente.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # HUBS LOGÍSTICOS
    # ------------------------------------------------------

    st.markdown(
        """
        <div class="section-card">
            <strong>Países con función logística</strong><br><br>
            Mercados como Países Bajos o Bélgica pueden registrar volúmenes
            de importación superiores a su consumo interno debido a su papel
            como centros logísticos europeos.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # LIMITACIONES DEL PRECIO MEDIO
    # ------------------------------------------------------

    st.markdown(
        """
        <div class="section-card">
            <strong>Interpretación del precio medio</strong><br><br>
            El precio medio por kilogramo no mide calidad.<br><br>
            Las diferencias observadas pueden deberse a:<br><br>
            • Mezclas de productos.<br>
            • Diferentes grados de transformación.<br>
            • Distintas cadenas de suministro.<br>
            • Efectos de inflación o tipo de cambio.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # BLUE OCEAN SCORE
    # ------------------------------------------------------

    st.markdown(
        """
        <div class="section-card">
            <strong>Limitaciones del Blue Ocean Score</strong><br><br>
            El Blue Ocean Score es un indicador propio diseñado para priorizar mercados.<br><br>
            No representa una medida oficial ni una predicción de ventas.<br><br>
            Su utilidad principal consiste en comparar oportunidades relativas
            entre países utilizando criterios homogéneos.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # COBERTURA TEMPORAL
    # ------------------------------------------------------

    st.markdown(
        """
        <div class="section-card">
            <strong>Cobertura temporal</strong><br><br>
            El análisis principal utiliza el periodo 2020–2024.<br><br>
            El año 2025 se excluye del dataset europeo enriquecido debido
            a la ausencia de indicadores socioeconómicos completos disponibles
            en World Bank para todos los países analizados.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # CONCLUSIÓN
    # ------------------------------------------------------

    st.markdown(
        """
        <div class="section-card">
            <strong>Conclusión metodológica</strong><br><br>
            A pesar de las limitaciones inherentes a los datos de comercio internacional,
            la combinación de importaciones, población y PIB per cápita proporciona una
            aproximación sólida para identificar mercados potencialmente atractivos para
            la expansión internacional de Velluto.<br><br>
            Los resultados deben interpretarse como una herramienta de apoyo a la decisión
            y no como una predicción exacta del comportamiento futuro del mercado.
        </div>
        """,
        unsafe_allow_html=True
    )