# Tasación Inmobiliaria Automatizada en Chile (IMT2220)

> **Proyecto Final - Introducción a la Ciencia de Datos**
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
* **Limpieza de Datos:** Eliminación de valores nulos, outliers y registros inconsistentes (ej. unidades monetarias erróneas). Se descartaron variables ruidosas como el título de la publicación y la dirección completa, priorizando las coordenadas geográficas para reducir el ruido en el modelo.
* **Modelamiento:** Entrenamiento de un modelo de Regresión Lineal Múltiple para estimar precios en UF.
* **Identificación de Comparables:** Validación de un enfoque basado en KNN (K-Nearest Neighbors) para identificar propiedades similares ("testigos") en el mercado.

---

## Resultados y Limitaciones

### Desempeño del Modelo
El modelo final alcanzó un coeficiente de determinación ($R^{2}$) de 0.9 tanto en los conjuntos de entrenamiento como de prueba, lo que indica un desempeño satisfactorio general.
* **Casas:** Los resultados fueron sólidos, con niveles de precisión entre 92% y 99% al comparar con valores reales, superando en algunos casos a herramientas comerciales.
* **Departamentos:** El rendimiento fue inferior en este segmento. Esto se atribuye a la ausencia de variables determinantes para departamentos en el proceso de extracción (orientación, número de piso, gastos comunes).

### Limitaciones Identificadas
* **Disponibilidad de datos:** En comunas con escasez de datos (menos de 100 viviendas disponibles), el modelo puede producir predicciones menos representativas o alejadas del valor real.
* **Mercado primario:** Los precios de proyectos nuevos o ventas "en verde" pueden distorsionar los valores reales en ciertos sectores.

---

## Estructura del Repositorio

El proyecto está organizado de la siguiente manera para facilitar la reproducibilidad:

```text
Proyecto/
├── Data/                   # Datos del proyecto
│   ├── raw/                # Dataset original sin procesar
│   └── Procesados/         # Dataset limpio y enriquecido (con lat/lon)
│
├── Docs/                   # Documentación formal
│   ├── Actualización_Final_del_Repositorio.pdf
│   ├── Entrega_Inicial_del_Repositorio.pdf
│   └── PDF Propuesta Proyecto.pdf
│
├── Figures/                # Gráficos y visualizaciones generadas
│   ├── boxplot_precio_uf_por_comuna.png
│   ├── matriz_correlacion.png
│   └── ... (otros gráficos de análisis)
│
├── Notebooks/              # Notebooks de Jupyter
│   ├── EDA/                # Notebooks de Análisis Exploratorio
│   ├── REGRESION/          # Notebooks de Modelamiento
│   └── agregacion_lat_lon_data.ipynb
│
├── Src/                    # Código de scrapping y scripts auxiliares
│   ├── portalinmo_scraper.py
│   ├── add_addresses.py
│   └── ...
│
├── Web/                    # Archivos para GitHub Pages
│
├── README.md               # Este archivo
└── requirements.txt        # Lista de dependencias 


## Instalación y Requisitos

Para ejecutar este proyecto localmente, se requiere Python 3.8 o superior.

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/Saaay20/PROYECTOIMT2200.git](https://github.com/Saaay20/PROYECTOIMT2200.git)
    cd PROYECTOIMT2200
    ```

2.  **Instalar dependencias:**
    Se recomienda utilizar un entorno virtual (venv o conda).

    ```bash
    pip install -r requirements.txt
    ```

    *Las librerías principales utilizadas son:*

      * **Análisis y Modelamiento:** `pandas`, `numpy`, `scikit-learn`, `geopy`, `joblib`.
      * **Visualización:** `matplotlib`, `seaborn`.
      * **Web Scraping:** `selenium` (Automatización de navegador), `beautifulsoup4` (Parsing HTML), `tqdm`.


-----

## Uso y Ejecución

El flujo de trabajo completo se encuentra distribuido en las carpetas `Notebooks/` y `Src/`.

1.  **Scraping y Datos:** Los scripts en `Src/` (`portalinmo_scraper.py`) se encargan de la obtención de datos crudos.
2.  **Preprocesamiento:** El notebook `Notebooks/agregacion_lat_lon_data.ipynb` gestiona la geocodificación.
3.  **Análisis y Modelo:**
      * Navegue a la carpeta `Notebooks/REGRESION/`.
      * Ejecute el notebook principal de modelamiento para entrenar el regresor y generar las predicciones.

-----

## Equipo y Roles

El desarrollo del proyecto se realizó en conjunto. Todos los integrantes participaron activamente y por igual en la toma de decisiones, la escritura del código y el análisis de datos desde un entorno de desarrollo compartido.

| Integrante | Rol / Responsabilidad |
|------------|-----------------------|
| **Javier Cuitiño** | **Co-Autor y Desarrollador:** Desarrollo de código, análisis de datos y documentación. |
| **Simón Saravia** | **Co-Autor y Desarrollador:** Desarrollo de código, análisis de datos y documentación. |
| **Alejandro Orellana** | **Co-Autor y Desarrollador:** Desarrollo de código, análisis de datos y documentación. |

-----

## Declaración de uso de IA


  * Se utilizaron herramientas de Inteligencia Artificial Generativa (ChatGPT/Gemini) para generar los códigos de **web scraping**, los **scripts auxiliares** y para implementar la lógica de **geolocalización** de las propiedades.
  
-----