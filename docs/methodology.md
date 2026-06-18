# Metodología

## Introducción

Este documento describe la metodología seguida para desarrollar el proyecto **Coffee Market Intelligence: Oportunidades Blue Ocean para el Café de Especialidad en Europa**.

El objetivo del análisis es identificar mercados europeos potencialmente atractivos para la expansión de una marca de café de especialidad utilizando datos de comercio internacional e indicadores socioeconómicos.

La metodología combina procesos de adquisición, transformación, enriquecimiento y visualización de datos para construir un sistema de apoyo a la toma de decisiones basado en evidencia.

---

# Fase 1. Obtención de datos

## Comercio internacional

La fuente principal utilizada es la base de datos **UN Comtrade**, que proporciona información sobre comercio internacional desagregada por país, producto y periodo temporal.

Se seleccionaron las siguientes categorías de producto:

| Código HS | Producto |
|------------|------------|
| 0901 | Café |
| 1801 | Cacao en grano |
| 1806 | Chocolate y preparados con cacao |

Los datos incluyen información sobre:

- País importador.
- Año.
- Valor de importación (USD).
- Peso neto (kg).
- Código de producto.
- Descripción del producto.

Periodo descargado:

- 2020-2025.

---

## Indicadores socioeconómicos

Para contextualizar el comportamiento comercial de cada país se utilizaron indicadores procedentes de **World Bank Open Data**.

Indicadores seleccionados:

| Indicador | Código |
|------------|------------|
| Population, total | SP.POP.TOTL |
| GDP per capita (current US$) | NY.GDP.PCAP.CD |

Periodo utilizado:

- 2020-2024.

---

# Fase 2. Limpieza y preparación de datos

Una vez obtenidos los datasets originales, se realizó un proceso de limpieza orientado a mejorar la calidad de los datos.

Las principales transformaciones fueron:

- Eliminación de columnas no relevantes para el análisis.
- Estandarización de nombres de variables.
- Conversión de tipos de datos.
- Tratamiento de registros incompletos.
- Validación de códigos de país.
- Control de valores nulos.

Además, se revisaron los registros con peso neto igual a cero para evitar errores en el cálculo de precios medios.

---

# Fase 3. Construcción del dataset enriquecido

Los datos comerciales se combinaron con los indicadores socioeconómicos mediante un proceso de enriquecimiento basado en:

- Código ISO del país.
- Año de referencia.

Como resultado se obtuvo un dataset integrado que combina información comercial y variables macroeconómicas.

---

## Variables derivadas

Se construyeron nuevas variables de negocio para facilitar el análisis comparativo entre países.

### Precio medio por kilogramo

```text
avg_price_usd_kg =
import_value_usd / net_weight_kg
```

Permite aproximar el valor medio pagado por kilogramo importado.

### Importación per cápita

```text
import_value_usd_per_capita =
import_value_usd / population
```

Permite comparar mercados independientemente de su tamaño poblacional.

### Volumen per cápita

```text
net_weight_kg_per_capita =
net_weight_kg / population
```

Permite medir la intensidad relativa de las importaciones.

---

# Fase 4. Análisis exploratorio de datos

Se realizó un análisis exploratorio (EDA) para identificar:

- Evolución temporal de las importaciones.
- Diferencias entre países.
- Distribución de valores.
- Posibles anomalías.
- Relación entre variables económicas y comerciales.

Esta fase permitió validar la calidad de los datos y orientar el diseño posterior del dashboard.

---

# Fase 5. Comparación entre café y cacao

El análisis incorpora una comparación estratégica entre las categorías de café y cacao.

Los objetivos de esta comparación son:

- Evaluar diferencias de tamaño de mercado.
- Analizar la evolución temporal de ambas categorías.
- Comparar niveles de precio medio.
- Identificar posibles tendencias de consumo premium.

Esta comparación se utiliza como contexto estratégico y no como una evaluación de sustitución directa entre productos.

---

# Fase 6. Construcción del Blue Ocean Score

## Objetivo

El Blue Ocean Score es un indicador diseñado específicamente para este proyecto con el objetivo de priorizar mercados europeos potencialmente atractivos para una estrategia de expansión internacional.

El indicador no pretende predecir ventas futuras ni rentabilidad, sino facilitar la comparación homogénea entre países.

---

## Variables utilizadas

El score combina cuatro dimensiones:

| Variable | Peso |
|-----------|------:|
| Importación per cápita | 30% |
| PIB per cápita | 25% |
| Crecimiento de las importaciones | 25% |
| Menor saturación relativa | 20% |

---

## Normalización

Las variables se transforman a una escala común de 0 a 100 para permitir su combinación.

Esta normalización evita que variables con magnitudes diferentes dominen el resultado final.

---

## Interpretación

Un valor elevado del Blue Ocean Score indica una combinación favorable de:

- Capacidad adquisitiva.
- Intensidad importadora.
- Crecimiento.
- Menor concentración relativa del mercado.

El resultado permite identificar mercados potencialmente interesantes para futuras fases de análisis comercial.

---

# Fase 7. Desarrollo del dashboard

El dashboard se desarrolló utilizando Streamlit y Plotly.

La aplicación se estructura en cinco áreas principales:

## Resumen ejecutivo

Visión global del mercado mediante KPIs, mapas y rankings.

## Mercado europeo

Análisis específico de los países europeos utilizando indicadores relativos y variables socioeconómicas.

## Café vs cacao

Comparación estratégica entre ambas categorías y análisis de posicionamiento relativo.

## Blue Ocean Score

Priorización de mercados mediante el indicador compuesto desarrollado para el proyecto.

## Limitaciones y sesgos

Documentación de restricciones metodológicas y consideraciones para la interpretación de resultados.

---

# Fase 8. Elaboración de recomendaciones

Finalmente, los resultados obtenidos se sintetizan en recomendaciones orientadas a negocio.

Estas recomendaciones se documentan en:

```text
docs/conclusions.md
```

y tienen como objetivo apoyar procesos de expansión internacional basados en datos.

---

# Resumen metodológico

La metodología desarrollada combina:

1. Obtención de datos oficiales.
2. Limpieza y validación.
3. Enriquecimiento con indicadores socioeconómicos.
4. Construcción de variables de negocio.
5. Comparación entre categorías.
6. Creación de un indicador propio de oportunidad.
7. Desarrollo de una herramienta visual de análisis.

Este enfoque permite transformar datos de comercio internacional en información accionable para apoyar la toma de decisiones estratégicas.