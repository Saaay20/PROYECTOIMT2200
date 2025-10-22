# 🏡 Análisis Exploratorio de Datos: Mercado de Viviendas en Santiago

Este proyecto corresponde a la **Entrega Inicial del Repositorio** y tiene como objetivo realizar un
**Análisis Exploratorio de Datos (EDA)** sobre un conjunto de viviendas en la Región Metropolitana,
obtenido desde portales inmobiliarios.

---

## 📋 Objetivos

1. Comprender la estructura del dataset y sus principales variables.
2. Identificar los factores que más influyen en el precio de las viviendas.
3. Analizar la distribución de precios y su dispersión.
4. Explorar diferencias territoriales entre comunas.
5. Evaluar el impacto de las amenidades (piscina, jardín, quincho, etc.) en el valor del inmueble.

---

## 🧾 Dataset utilizado

**Archivo:** `Dataset_viviendas_final.csv`

**Tamaño:** 6.232 registros y 19 variables.

**Principales columnas:**
- `comuna`: comuna donde se ubica la vivienda  
- `precio_uf`: precio total en UF  
- `m2_construidos`, `m2_totales`: superficies del inmueble  
- `dormitorios`, `banos`, `estacionamientos`: características físicas  
- `jardin`, `piscina`, `quincho`, `condominio_cerrado`: amenidades booleanas  
- `educacion`, `salud`, `comercios`: servicios cercanos  
- `tipo_vivienda`: categoría del inmueble (casa, departamento, etc.)

---

## ⚙️ Metodología

1. **Limpieza de datos:**  
   - Eliminación de valores nulos y ceros en columnas críticas.  
   - Filtrado de outliers (percentiles 95 y 99.5).  

2. **Creación de variables derivadas:**  
   - `precio_m2 = precio_uf / m2_construidos`  
   - Indicadores por comuna y tipo de vivienda.

3. **Análisis exploratorio:**  
   - Distribuciones de precios y precios por m².  
   - Correlaciones entre variables numéricas.  
   - Comparaciones por comuna, tipo de vivienda y amenidades.  
   - Visualizaciones de dispersión, boxplots y rankings.

---

## 📊 Principales hallazgos

- Alta **heterogeneidad del mercado inmobiliario**: coeficiente de variación ≈ 85%.
- Comunas del oriente (Vitacura, Lo Barnechea, Las Condes) presentan precios por m² más altos.
- Amenidades como **piscina y condominio cerrado** incrementan el valor promedio.
- Existe una **asimetría significativa** en las distribuciones de precios (cola derecha).
- Las viviendas más pequeñas tienden a tener **mayor valor por metro cuadrado**.

---

## 💻 Requisitos técnicos

El notebook fue desarrollado en **Python 3.11** con las siguientes librerías:
```bash
pandas
matplotlib
numpy
scipy
