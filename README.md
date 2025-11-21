# Tasación Inmobiliaria Automatizada en Santiago, Región Metropolitana, Chile.

> **Proyecto - Introducción a la Ciencia de Datos**
> *Pontificia Universidad Católica de Chile*

Este repositorio contiene el desarrollo completo del proyecto final para el curso IMT2220. El objetivo principal es desarrollar un modelo de **Machine Learning** capaz de predecir el valor de mercado de propiedades residenciales en la Región Metropolitana, utilizando datos enriquecidos geoespacialmente.

---

## Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Resultados y Limitaciones](#resultados-y-limitaciones)
3. [Estructura del Repositorio](#estructura-del-repositorio)
4. [Instalación y Requisitos](#instalación-y-requisitos)
5. [Uso y Ejecución](#uso-y-ejecución)
6. [Equipo y Roles](#equipo-y-roles)
7. [Declaración de uso de IA](#declaración-de-uso-de-ia)

---

## Descripción del Proyecto

El problema abordado es la necesidad de contar con un valor de referencia objetivo para la compra-venta de viviendas, dada la dificultad de estimar precios de forma rápida y precisa. La solución implementa un flujo de trabajo de Ciencia de Datos que automatiza la tasación aprovechando la información pública disponible en portales inmobiliarios.

Las principales etapas del proyecto incluyen:

* **Adquisición de Datos:** Extracción de información mediante web scraping de portalinmobiliario.com. Se generaron datasets de casas y departamentos, los cuales fueron unificados posteriormente.
* **Geocodificación:** Implementación de un proceso para obtener latitud y longitud a partir de las direcciones registradas, permitiendo el cálculo de distancias a puntos de interés.
* **Limpieza de Datos:** Eliminación de valores nulos, outliers y registros inconsistentes. Se descartaron variables ruidosas como el título de la publicación y la dirección completa, priorizando las coordenadas geográficas.
* **Modelamiento:** Entrenamiento de un modelo de Regresión Lineal Múltiple para estimar precios en UF.


---

## Resultados y Limitaciones

### Desempeño del Modelo

El modelo final alcanzó un coeficiente de determinación ($R^{2}$) de **0.9** en los conjuntos de entrenamiento y prueba.

* **Casas:** Precisión entre 92% y 99%, comparativamente mejor que algunas herramientas comerciales.
* **Departamentos:** Menor rendimiento debido a variables ausentes relevantes para este tipo de inmueble.

### Limitaciones Identificadas

* **Escasez de datos en ciertas comunas** (menos de 100 viviendas).
* **Mercado primario:** Publicaciones en verde o en blanco pueden distorsionar los precios.

---

## Estructura del Repositorio

```text
Proyecto/
├── Data/                   # Datos del proyecto
│   ├── raw/                # Dataset original sin procesar
│   └── Procesados/         # Dataset limpio y enriquecido (con lat/lon)
│
├── Docs/                   # Documentación formal *(Lectura recomendada: contiene preguntas planteadas antes y durante el desarrollo, además de las conclusiones finales)**
│   ├── Actualización_Final_del_Repositorio.pdf
│   ├── Entrega_Inicial_del_Repositorio.pdf
│   └── PDF_Propuesta_Proyecto.pdf
│
├── Figures/                # Visualizaciones
│   ├── boxplot_precio_uf_por_comuna.png
│   ├── matriz_correlacion.png
│   └── ...
│
├── Notebooks/              # Notebooks de análisis y modelamiento
│   ├── EDA/
│   ├── REGRESION/
│   └── agregacion_lat_lon_data.ipynb
│
├── Src/                    # Scripts de scraping y utilidades
│   ├── portalinmo_scraper.py
│   ├── add_addresses.py
│   └── ...
│
├── Web/                    # Archivos para GitHub Pages
│
├── README.md               # Este archivo
└── requirements.txt        # Dependencias del proyecto
```

---

## Instalación y Requisitos

Para ejecutar este proyecto localmente se requiere Python 3.8 o superior.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Saaay20/PROYECTOIMT2200.git
cd PROYECTOIMT2200
```

### 2. Instalar dependencias

Se recomienda usar un entorno virtual.

```bash
pip install -r requirements.txt
```

**Librerías principales:** pandas, numpy, scikit-learn, geopy, joblib, matplotlib, seaborn, selenium, beautifulsoup4, tqdm.

---

## Uso y Ejecución

1. **Scraping:** scripts en `Src/`.
2. **Preprocesamiento:** `agregacion_lat_lon_data.ipynb`.
3. **Modelamiento:** Notebooks en `Notebooks/REGRESION/`.

---

## Equipo y Roles

| Integrante             | Rol / Responsabilidad    |
| ---------------------- | ------------------------ |
| **Javier Cuitiño**     | Co-autor y desarrollador |
| **Simón Saravia**      | Co-autor y desarrollador |
| **Alejandro Orellana** | Co-autor y desarrollador |

---

## Declaración de uso de IA

Se utilizaron herramientas de IA generativa para apoyar la creación de scripts de scraping, funciones auxiliares y lógica de geolocalización.

---
