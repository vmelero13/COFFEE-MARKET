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

---

# Conclusiones

Los datos utilizados proceden de fuentes oficiales y presentan un nivel de calidad adecuado para un análisis exploratorio de oportunidades de mercado.

No obstante, deben interpretarse teniendo en cuenta que el comercio internacional constituye una aproximación indirecta a la demanda real y que las categorías analizadas no permiten identificar de forma específica el mercado del café de especialidad.

Las medidas de limpieza, normalización y enriquecimiento aplicadas permiten reducir parte de estos sesgos y proporcionar una base sólida para la toma de decisiones basada en datos.