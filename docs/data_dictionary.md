# Diccionario de datos

## Dataset principal

**Archivo:** `trade_enriched_complete_2020_2024.csv`

Dataset analítico final utilizado para el dashboard.

---

## Columnas

| Columna | Tipo | Descripción | Fuente |
|----------|----------|----------|----------|
| `year` | Integer | Año de referencia. | UN Comtrade / World Bank |
| `country_code` | String | Código ISO del país importador. | UN Comtrade / World Bank |
| `country` | String | Nombre del país importador. | UN Comtrade / World Bank |
| `commodity_code` | Integer | Código HS del producto comercializado. | UN Comtrade |
| `commodity_description` | String | Descripción oficial del producto. | UN Comtrade |
| `sector` | String | Categoría general del producto (Coffee / Cocoa). | Derivada |
| `product_group` | String | Grupo de producto simplificado para el análisis. | Derivada |
| `net_weight_kg` | Float | Peso neto importado en kilogramos. | UN Comtrade |
| `import_value_usd` | Float | Valor total importado en dólares estadounidenses. | UN Comtrade |
| `avg_price_usd_kg` | Float | Precio medio por kilogramo importado. | Calculada |
| `population` | Float | Población total del país. | World Bank |
| `gdp_per_capita` | Float | PIB per cápita en dólares corrientes. | World Bank |
| `import_value_usd_per_capita` | Float | Valor importado por habitante. | Calculada |
| `net_weight_kg_per_capita` | Float | Kilogramos importados por habitante. | Calculada |

---

## Variables derivadas

### `avg_price_usd_kg`

Precio medio de importación por kilogramo.

**Fórmula:**

`import_value_usd / net_weight_kg`

---

### `import_value_usd_per_capita`

Valor importado por habitante.

**Fórmula:**

`import_value_usd / population`

---

### `net_weight_kg_per_capita`

Volumen importado por habitante.

**Fórmula:**

`net_weight_kg / population`

---

## Productos incluidos

| Código HS | Producto |
|------------|------------|
| `0901` | Café |
| `1801` | Cacao en grano |
| `1806` | Chocolate y preparados de cacao |

---

## Claves de integración entre datasets

Los datasets de UN Comtrade y World Bank se integran mediante las siguientes claves:

- `country_code`
- `country`
- `year`

Estas variables permiten relacionar los datos de comercio internacional con los indicadores demográficos y económicos de cada país.

--- 

## Dataset global complementario

**Archivo:** `trade_global_2020_2025.csv`

Dataset procesado utilizado como benchmark internacional dentro del dashboard.

Este dataset conserva todos los países disponibles en UN Comtrade y permite contextualizar el mercado europeo frente al mercado global.

---

## Columnas del dataset global

| Columna | Tipo | Descripción | Fuente |
|----------|----------|----------|----------|
| `year` | Integer | Año de referencia. | UN Comtrade |
| `country_code` | String | Código ISO del país importador. | UN Comtrade |
| `country` | String | Nombre del país importador. | UN Comtrade |
| `commodity_code` | Integer | Código HS del producto comercializado. | UN Comtrade |
| `commodity_description` | String | Descripción oficial del producto. | UN Comtrade |
| `net_weight_kg` | Float | Peso neto importado en kilogramos. | UN Comtrade |
| `import_value_usd` | Float | Valor total importado en dólares estadounidenses. | UN Comtrade |
| `sector` | String | Categoría general del producto: Coffee o Cocoa. | Derivada |
| `product_group` | String | Grupo de producto simplificado para el análisis. | Derivada |
| `avg_price_usd_kg` | Float | Precio medio por kilogramo importado. | Calculada |

---

## Observaciones

- El análisis principal se realiza para el periodo 2020-2024.
- El dataset global complementario conserva información hasta 2025 al no depender de variables procedentes de World Bank.
- Los datos de población y PIB per cápita proceden de World Bank.
- Algunos registros presentan valores nulos o iguales a cero en `net_weight_kg`, por lo que no es posible calcular `avg_price_usd_kg`.
- Estos registros se conservan para los análisis basados en valor de importación.
- El año 2025 se excluye del dataset final enriquecido porque World Bank no dispone todavía de datos completos de población y PIB per cápita para ese periodo.