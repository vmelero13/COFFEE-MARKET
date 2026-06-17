# COFFEE-MARKET

Business Intelligence project to identify Blue Ocean opportunities for specialty coffee expansion across European markets.

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
- Diseñar un indicador propio de atractivo de mercado (Blue Ocean Score).
- Comunicar los resultados mediante un dashboard interactivo orientado a usuarios no técnicos.

---

## Hipótesis de negocio

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

### Dataset principal: Comercio internacional

**UN Comtrade Database**

Datos de importaciones de café y cacao para países de la Unión Europea.

Productos analizados:

- HS 0901 – Café
- HS 1801 – Cacao en grano
- HS 1806 – Chocolate y preparados con cacao

Periodo analizado:

- 2020–2024

Variables principales:

- País importador
- Año
- Valor comercial (USD)
- Peso neto (kg)
- País socio comercial
- Código de producto
- Descripción del producto

Fuente:

- https://comtradeplus.un.org/

---

### Dataset complementario: Indicadores socioeconómicos

**World Bank Open Data**

Indicadores utilizados:

- Population, total (SP.POP.TOTL)
- GDP per capita, current US$ (NY.GDP.PCAP.CD)

Periodo analizado:

- 2020–2024

Fuente:

- https://data.worldbank.org/

---

### Nota sobre el periodo de análisis

Aunque los datos de comercio incluyen registros de 2025, el análisis final se limita al periodo 2020–2024 debido a la ausencia de indicadores socioeconómicos completos para 2025 en World Bank.

---

## Organización de los datos

Los datasets utilizados en el proyecto se almacenan siguiendo una estructura que separa los datos originales descargados de las fuentes oficiales de los datos procesados utilizados para el análisis y el dashboard.

```text
data/
│
├── raw/
│   │
│   ├── un_comtrade/
│   │   └── un_comtrade_coffee_cocoa_2020_2025.csv
│   │
│   ├── worldbank_population/
│   │   ├── wb_population_data.csv
│   │   ├── wb_population_country_metadata.csv
│   │   └── wb_population_indicator_metadata.csv
│   │
│   └── worldbank_gdp/
│       ├── wb_gdp_per_capita_data.csv
│       ├── wb_gdp_country_metadata.csv
│       └── wb_gdp_indicator_metadata.csv
│
└── processed/
    └── trade_enriched_complete_2020_2024.csv
```

La carpeta `raw/` contiene los datos originales descargados de las fuentes oficiales sin modificaciones.

La carpeta `processed/` contiene los datasets limpios, transformados y enriquecidos utilizados tanto en el análisis exploratorio como en el dashboard interactivo.

---

## Documentación adicional

La documentación técnica del proyecto se encuentra en la carpeta `docs/`:

- `data_dictionary.md`
- `data_model.md`
- `methodology.md`
- `data_governance_biases.md`

---

## Indicadores clave (KPIs)

- Valor total importado.
- Volumen importado.
- Precio medio por kilogramo.
- Crecimiento interanual.
- Importaciones per cápita.
- Ranking de mercados.
- Blue Ocean Score.

---

## Estructura del proyecto

```text
COFFEE-MARKET/
│
├── app/
│   ├── components/
│   └── pages/
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── trade_enriched_complete_2020_2024.csv
│       └── trade_global_2020_2025.csv
│
├── notebooks/
│   └── 01_eda_un_comtrade.ipynb
│
├── src/
│   ├── config.py
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   └── metrics.py
│
├── docs/
│   ├── data_dictionary.md
│   ├── data_model.md
│   ├── methodology.md
│   └── data_governance_biases.md
│
├── assets/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Descripción de carpetas

| Carpeta | Descripción |
|----------|----------|
| `app/` | Aplicación principal de Streamlit y páginas del dashboard. |
| `data/raw/` | Datos originales descargados de las fuentes oficiales. |
| `data/processed/` | Datos limpios y transformados para análisis y visualización. |
| `notebooks/` | Análisis exploratorio de datos (EDA) y validación de hipótesis. |
| `src/` | Scripts de limpieza, transformación y cálculo de métricas de negocio. |
| `docs/` | Documentación metodológica, modelo de datos y diccionario de variables. |
| `assets/` | Imágenes y recursos gráficos utilizados en el proyecto. |

Esta estructura busca separar claramente la adquisición de datos, el análisis, la lógica de negocio y la visualización para facilitar el mantenimiento y la reproducibilidad del proyecto.

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

El análisis tiene en cuenta diversas limitaciones inherentes a los datos:

- Las importaciones no representan necesariamente el consumo real.
- Algunos países funcionan como centros logísticos y de reexportación.
- Los datos agregados por país pueden ocultar diferencias regionales.
- El precio medio por kilogramo no refleja necesariamente la calidad del producto.
- Las categorías comerciales utilizadas pueden incluir distintos tipos de café y cacao.

Estas limitaciones serán documentadas y explicadas dentro del dashboard para evitar interpretaciones erróneas.

---

## Resultado esperado

Desarrollar un dashboard interactivo desplegado en la nube que permita identificar oportunidades de mercado para el café de especialidad en Europa, compararlas con el mercado del cacao y proporcionar recomendaciones estratégicas basadas en datos.