# COFFEE-MARKET
Business intelligence project to identify blue ocean opportunities for specialty coffee expansion across European markets

# Coffee Market Intelligence: Oportunidades Blue Ocean para el Café de Especialidad en Europa

## Descripción del proyecto

Este proyecto analiza el mercado europeo del café con el objetivo de identificar oportunidades de expansión para empresas de café de especialidad.

A través de datos de comercio internacional, indicadores demográficos y variables económicas, se pretende detectar mercados con alto potencial de crecimiento y comparar su atractivo frente al mercado del cacao.

El resultado final será un dashboard interactivo desarrollado en Streamlit y desplegado en la nube para facilitar la toma de decisiones por parte de perfiles directivos y no técnicos.

---

## Pregunta de negocio

¿Qué países europeos presentan las mejores oportunidades para la expansión del café de especialidad y cómo se comparan estas oportunidades con el mercado del cacao?

---

## Objetivos

- Analizar la evolución del mercado del café y del cacao en Europa.
- Identificar países con alta demanda y potencial de crecimiento.
- Comparar tendencias de importación entre café y cacao.
- Construir un indicador propio de atractivo de mercado (Blue Ocean Score).
- Comunicar los resultados mediante un dashboard interactivo orientado a usuarios no técnicos.

---

Hipótesis de negocio

El consumo de café en Europa presenta diferencias significativas entre países. Sin embargo, los mercados con mayor volumen no siempre representan las mejores oportunidades para el café de especialidad.

Este proyecto parte de la hipótesis de que existen países europeos con una combinación favorable de crecimiento, poder adquisitivo y menor saturación competitiva que podrían representar oportunidades de expansión más atractivas que los mercados tradicionalmente dominantes.

Como contraste estratégico, se analizará también el mercado del cacao para evaluar si presenta mejores perspectivas comerciales que el café en determinados contextos.

---

## Herramientas utilizadas

### Análisis de datos

- Python
- Pandas
- NumPy

### Visualización

- Streamlit
- Plotly

### Desarrollo

- Git
- GitHub
- Jupyter Notebook

---

## Fuentes de datos

### Dataset principal

Base de datos de comercio internacional:

- UN Comtrade
- Categorías analizadas:
  - Café (HS 0901)
  - Cacao (HS 1801 / HS 1806)

### Datasets complementarios

- World Bank
  - Población
  - PIB per cápita

Fuentes adicionales potenciales:

- Eurostat
- FAOSTAT

---

## Indicadores clave (KPIs)

- Valor total importado
- Volumen importado
- Precio medio por kilogramo
- Crecimiento interanual
- Importaciones per cápita
- Ranking de mercados
- Blue Ocean Score

---

## Estructura del proyecto

```text
COFFEE-MARKET/
│
├── app/
│   ├── main.py
│   ├── pages/
│   │   ├── 1_market_overview.py
│   │   ├── 2_blue_ocean_score.py
│   │   ├── 3_coffee_vs_cocoa.py
│   │   └── 4_governance_biases.py
│   │
│   └── components/
│       ├── charts.py
│       ├── filters.py
│       └── kpis.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README_data_sources.md
│
├── notebooks/
│   └── 01_eda_un_comtrade.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── metrics.py
│   └── config.py
│
├── powerbi/
│   ├── coffee_cocoa_europe_dashboard.pbix
│   └── dax_measures.md
│
├── docs/
│   ├── data_governance_biases.md
│   ├── methodology.md
│   └── presentation_script.md
│
├── assets/
│   └── images/
│
├── .gitignore
├── README.md
├── requirements.txt
└── streamlit_app.py
```

### Descripción de carpetas

| Carpeta           | Descripción                                                           |
| ----------------- | --------------------------------------------------------------------- |
| `app/`            | Aplicación principal de Streamlit y páginas del dashboard.            |
| `components/`     | Componentes reutilizables para gráficos, filtros e indicadores KPI.   |
| `data/raw/`       | Datos originales descargados de las fuentes oficiales.                |
| `data/processed/` | Datos limpios y transformados para análisis y visualización.          |
| `notebooks/`      | Análisis exploratorio de datos (EDA) y validación de hipótesis.       |
| `src/`            | Scripts de limpieza, transformación y cálculo de métricas de negocio. |
| `powerbi/`        | Versión alternativa del proyecto en Power BI y documentación DAX.     |
| `docs/`           | Documentación metodológica, gobernanza y presentación ejecutiva.      |
| `assets/`         | Imágenes y recursos gráficos utilizados en el proyecto.               |

Esta estructura busca separar claramente la adquisición de datos, el análisis, la lógica de negocio y la visualización para facilitar el mantenimiento y la reproducibilidad del proyecto.

```
```

---

## Metodología

1. Recopilación de datos.
2. Limpieza y transformación de datos.
3. Análisis exploratorio (EDA).
4. Creación de variables de negocio.
5. Cálculo de indicadores clave.
6. Desarrollo del dashboard interactivo.
7. Elaboración de recomendaciones estratégicas.

---

## Consideraciones sobre gobernanza y sesgos

El análisis tendrá en cuenta diversas limitaciones inherentes a los datos:

- Las importaciones no representan necesariamente el consumo real.
- Algunos países funcionan como centros logísticos y de reexportación.
- Los datos agregados por país pueden ocultar diferencias regionales.
- El precio medio por kilogramo no refleja necesariamente la calidad del producto.
- Las categorías comerciales utilizadas pueden incluir distintos tipos de café y cacao.

Estas limitaciones serán documentadas y explicadas dentro del dashboard para evitar interpretaciones erróneas.

---

## Resultado esperado

Desarrollar un dashboard interactivo desplegado en la nube que permita identificar oportunidades de mercado para el café de especialidad en Europa, compararlas con el mercado del cacao y proporcionar recomendaciones estratégicas basadas en datos.