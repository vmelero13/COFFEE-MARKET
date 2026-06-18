# Gobernanza de datos y análisis de sesgos

## Introducción

Todo análisis de negocio está condicionado por la calidad, cobertura y naturaleza de los datos utilizados.

Este documento identifica las principales limitaciones y sesgos presentes en las fuentes de datos empleadas en el proyecto, así como las acciones realizadas para minimizar su impacto en el análisis.

---

# Fuentes utilizadas

## UN Comtrade

Fuente oficial de Naciones Unidas para estadísticas de comercio internacional.

Variables principales utilizadas:

- País importador
- Año
- Código de producto (HS)
- Peso neto importado (kg)
- Valor importado (USD)

---

## World Bank Open Data

Indicadores socioeconómicos utilizados:

- Population, total
- GDP per capita (current US$)

---

# Sesgos y limitaciones identificados

## 1. Importaciones no equivalen a consumo

### Riesgo

El volumen importado por un país no representa necesariamente su consumo interno.

Algunos países actúan como centros logísticos o plataformas de redistribución hacia otros mercados.

Ejemplos conocidos dentro de Europa:

- Países Bajos
- Bélgica
- Alemania

Estos países pueden presentar volúmenes de importación elevados que no reflejan directamente la demanda final de los consumidores.

### Mitigación aplicada

El análisis incorpora métricas per cápita que permiten contextualizar los volúmenes importados respecto al tamaño de la población.

Variables utilizadas:

- `import_value_usd_per_capita`
- `net_weight_kg_per_capita`

---

## 2. Diferencias de tamaño entre países

### Riesgo

Las comparaciones basadas únicamente en volumen o valor importado favorecen sistemáticamente a los países más poblados.

Por ejemplo:

- Alemania
- Francia
- Italia
- España

podrían aparecer como los mercados más relevantes únicamente por su tamaño demográfico.

### Mitigación aplicada

Se incorporaron datos de población procedentes del World Bank y se generaron métricas normalizadas por habitante.

Esto permite comparar la intensidad relativa de las importaciones entre países de distinto tamaño.

---

## 3. Diferencias de poder adquisitivo

### Riesgo

Un elevado nivel de importaciones no implica necesariamente un mercado atractivo para productos premium o de especialidad.

La capacidad económica de los consumidores puede condicionar significativamente el potencial de crecimiento del café de especialidad.

### Mitigación aplicada

Se incorporó la variable:

- `gdp_per_capita`

procedente de World Bank.

Esta métrica permite contextualizar la capacidad económica media de cada mercado.

---

## 4. Limitaciones de las categorías comerciales

### Riesgo

Los códigos HS utilizados agrupan productos con diferentes niveles de transformación y valor añadido.

Por ejemplo:

### HS 0901

Incluye:

- Café verde
- Café tostado
- Café descafeinado

### HS 1806

Incluye:

- Chocolate
- Preparados alimenticios con cacao

Por tanto, las categorías no representan exclusivamente productos de especialidad.

### Mitigación aplicada

Se agruparon los productos en categorías homogéneas:

- Coffee total
- Cocoa beans
- Chocolate and cocoa preparations

y se documentaron explícitamente las limitaciones de cada categoría.

---

## 5. Ausencia de información sobre calidad

### Riesgo

Las bases de datos utilizadas no contienen información sobre:

- Calidad del café
- Certificaciones
- Origen específico
- Segmento premium

Por tanto, el análisis evalúa el mercado general de importación y no exclusivamente el mercado del café de especialidad.

### Mitigación aplicada

Esta limitación se reconoce explícitamente y se considera una posible línea de mejora mediante la incorporación futura de fuentes especializadas del sector cafetero.

---

## 6. Valores faltantes en el peso neto

### Riesgo

Algunos registros presentan valores nulos o iguales a cero en la variable `net_weight_kg`.

Esto impide calcular correctamente métricas derivadas como:

- `avg_price_usd_kg`

### Mitigación aplicada

Los registros se conservaron porque seguían aportando información válida sobre valor económico de importación.

Las métricas afectadas se calcularon únicamente cuando existía información suficiente.

---

## 7. Cobertura temporal incompleta para 2025

### Riesgo

Los datos de comercio incluían registros correspondientes a 2025.

Sin embargo, los indicadores socioeconómicos del World Bank para dicho año no estaban disponibles de forma consistente.

### Mitigación aplicada

Se excluyó el año 2025 del dataset analítico final.

El análisis se limita al periodo:

**2020–2024**

garantizando así una cobertura homogénea de todas las variables utilizadas.

## 8. Sesgos derivados del Blue Ocean Score

El Blue Ocean Score es un indicador compuesto diseñado específicamente para este proyecto con el objetivo de priorizar mercados potencialmente atractivos para una estrategia de expansión internacional.

Su construcción implica decisiones metodológicas que pueden influir en los resultados obtenidos.

### Selección de variables

El indicador se construye a partir de cuatro dimensiones:

- Importación per cápita.
- PIB per cápita.
- Crecimiento de las importaciones.
- Saturación relativa.

### Definición de saturación relativa

La saturación relativa se utiliza como una aproximación al nivel de madurez de cada mercado.

En este proyecto se estima indirectamente a partir del peso relativo de las importaciones dentro del conjunto de países analizados.

La hipótesis subyacente es que los mercados con mayores niveles de importación suelen presentar una competencia más intensa y un menor espacio relativo para nuevos entrantes.

Esta aproximación no mide directamente la competencia real del mercado y debe interpretarse como una simplificación metodológica.

La inclusión de estas variables responde a una hipótesis de negocio concreta y no constituye una medida universalmente aceptada del atractivo de mercado.

### Asignación de pesos

Los pesos utilizados son:

| Variable | Peso |
|-----------|------:|
| Importación per cápita | 30% |
| PIB per cápita | 25% |
| Crecimiento de las importaciones | 25% |
| Saturación relativa | 20% |

Estos pesos han sido definidos mediante criterio analítico y no mediante técnicas estadísticas avanzadas ni validación externa.

Por tanto, pequeñas modificaciones en los pesos podrían alterar parcialmente la clasificación final de los países.

### Interpretación del resultado

El Blue Ocean Score debe interpretarse como una herramienta de priorización relativa entre mercados y no como una predicción de ventas, rentabilidad o éxito comercial.

Su principal utilidad consiste en facilitar la comparación homogénea entre países utilizando criterios consistentes.

### Limitaciones del indicador

El Blue Ocean Score no incorpora variables relevantes que podrían influir en el atractivo real de un mercado, tales como:

- Consumo real de café.
- Número de competidores.
- Presencia de marcas premium.
- Canales de distribución especializados.
- Indicadores de hostelería y restauración.
- Preferencias del consumidor.

Por tanto, el indicador debe entenderse como una herramienta exploratoria de priorización y no como una medida exhaustiva del potencial comercial.

---

# Transformaciones realizadas para mejorar la calidad del dato

Durante el proceso de preparación se realizaron las siguientes acciones:

- Selección exclusiva de países de la Unión Europea.
- Normalización de nombres de países.
- Homogeneización de códigos ISO.
- Transformación de indicadores World Bank a formato longitudinal.
- Integración de datasets mediante país y año.
- Eliminación del año 2025.
- Creación de métricas per cápita.
- Creación de métricas de precio medio por kilogramo.
- Verificación de registros duplicados.
- Validación de consistencia entre fuentes.
- Construcción del indicador compuesto Blue Ocean Score.

---

# Conclusiones

Los datos utilizados proceden de fuentes oficiales y presentan un nivel de calidad adecuado para un análisis exploratorio de oportunidades de mercado.

No obstante, deben interpretarse teniendo en cuenta que el comercio internacional constituye una aproximación indirecta a la demanda real y que las categorías analizadas no permiten identificar de forma específica el mercado del café de especialidad.

Las medidas de limpieza, normalización y enriquecimiento aplicadas permiten reducir parte de estos sesgos y proporcionar una base sólida para la toma de decisiones basada en datos.