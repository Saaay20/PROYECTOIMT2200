
## Descripción general

Este proyecto implementa un **scraper automatizado** para recolectar información de propiedades publicadas en [PortalInmobiliario.com](https://www.portalinmobiliario.com).  
El objetivo fue construir un **dataset propio** de viviendas en la Región Metropolitana de Chile, incluyendo variables como:

- Comuna  
- Precio en UF  
- Superficie total y construida  
- Cantidad de baños, dormitorios y estacionamientos  
- Antigüedad  
- Presencia de amenities (jardín, piscina, quincho, condominio cerrado)  
- Cercanía a servicios (educación, comercios, salud)  
- URL del aviso  

El flujo principal está distribuido en varios archivos Python y automatizado mediante un script principal.

---

## Estructura de los scripts

### `test_login.py`
Permite **iniciar sesión manualmente** en Portal Inmobiliario utilizando Selenium.  
Una vez completado el login, guarda las **cookies de sesión** en un archivo `ml_cookies.pkl`, que luego se reutiliza en los demás scripts para **evitar el muro de autenticación de Mercado Libre**.

**Flujo:**
1. Abre el navegador.  
2. El usuario inicia sesión manualmente.  
3. Se guardan las cookies locales.  
4. Cierra el navegador.

---

### `portalinmo_scraper.py`
Este es el **núcleo del sistema de scraping**.  
Utiliza **Selenium** y **BeautifulSoup** para navegar por cada página de resultados y extraer la información detallada de cada propiedad.

**Principales características:**
- Extrae automáticamente datos estructurados desde cada publicación.  
- Soporta **cookies persistentes** para mantener sesiones activas.  
- Implementa **reanudación automática** (si el CSV ya existe, continúa desde donde quedó).  
- Limpieza y conversión de datos (`m2`, precios, UF → float, int, bool, etc.).  
- Control de errores y pausas entre requests para evitar bloqueos.  
- Límite de propiedades por comuna (`--max`) configurable por parámetro.

**Límites:**  
Durante el desarrollo se observó que enviar demasiadas solicitudes consecutivas provocaba bloqueos temporales por parte del sitio, especialmente desde IPs residenciales.  
Por esa razón, se **limitó el número de requests y se introdujeron esperas aleatorias** entre 1 y 3 segundos por página.

---

### `run_all.py`
Automatiza el proceso para **todas las comunas de la Región Metropolitana**.  
Contiene una lista de comunas con sus respectivas URLs de búsqueda y ejecuta el scraper en cada una en serie.

**Funciones clave:**
- Genera automáticamente archivos CSV individuales por comuna en la carpeta `resultados_csv/`.  
- Crea la carpeta de salida si no existe.  
- Realiza pausas de seguridad entre ejecuciones.  
- Detecta errores y continúa con la siguiente comuna sin interrumpir el flujo.

---

### `add_addresses.py`
Una vez generado el dataset base, se olvido agregar las direcciones, por lo tanto **las direcciones exactas no estaban siendo capturadas**.  
Este script se encarga de **añadir las direcciones** posteriormente.

**Funcionamiento:**
- Lee las URLs desde un CSV ya scrapeado.  
- Usa Selenium para renderizar la página completamente.  
- Con BeautifulSoup busca las secciones de ubicación (por ejemplo, “Ubicación” o el bloque superior del precio).  
- Guarda progresivamente los resultados en un nuevo CSV con columna `direccion`.



---

### `run_add_addresses.bat`
Archivo batch de Windows que ejecuta automáticamente el script `add_addresses.py` con los parámetros correspondientes.  
Facilita repetir el proceso sin abrir manualmente el entorno Python.

---

## Uso de IA y restricciones de IP

Durante las pruebas, **uno de los miembros del grupo fue bloqueado temporalmente** por Portal Inmobiliario al realizar demasiadas solicitudes desde su IP residencial.  
Para evitar más bloqueos y pérdida de acceso, se **optó por utilizar una herramienta de IA** para:

- Analizar y reestructurar el código de scraping.  
- Implementar mecanismos más humanos (esperas aleatorias, simulación de scroll).  
- Mejorar la robustez del parser HTML.  
- Reducir la frecuencia de requests y prevenir bloqueos.  

Gracias a esto, el scraper pudo **seguir funcionando sin sobrecargar los servidores del sitio** y con un flujo mucho más estable.

---


## Flujo de ejecución completo

1. **Generar cookies:**

   ```bash
   python test_login.py
   ```

   Abre una ventana de navegador donde deberás **iniciar sesión manualmente** en [PortalInmobiliario.com](https://www.portalinmobiliario.com).
   Una vez completado el proceso de login, presiona **ENTER** en la consola para guardar las cookies en el archivo `ml_cookies.pkl`.

2. **Ejecutar el scraping completo:**

   ```bash
   python run_all.py
   ```

   Este script recorrerá automáticamente las **comunas configuradas**, generando archivos CSV individuales con las propiedades de cada una.
   Si una comuna falla, el proceso continúa con la siguiente para evitar interrupciones.

3. **Agregar direcciones faltantes:**

   ```bash
   python add_addresses.py --input resultados_csv/merged.csv --output resultados_csv/with_address.csv --cookies ml_cookies.pkl
   ```

   Este paso se utiliza para **añadir las direcciones exactas** a los registros que no las incluían originalmente.
   El script carga las cookies para mantener la sesión iniciada y utiliza **Selenium + BeautifulSoup** para obtener las direcciones visibles en la sección de “Ubicación”.

---

## Observaciones finales

* Se limitó el número máximo de propiedades por comuna para **evitar bloqueos del sitio**.
* Se introdujeron **esperas aleatorias entre solicitudes (1–3 segundos)** para simular un comportamiento humano y reducir la carga en el servidor.
* Las direcciones fueron añadidas posteriormente con el script complementario `add_addresses.py`.
* El uso de cookies y Selenium permitió acceder a datos tras el login sin recurrir a scraping agresivo.
* Durante las pruebas, uno de los miembros del grupo sufrió un **bloqueo temporal de IP** al acceder repetidamente al sitio desde su red doméstica.
  Por esta razón, se decidió **apoyarse en herramientas de IA (ChatGPT)** para reestructurar el código, añadir límites de requests y reforzar la estabilidad del sistema.
* El dataset final combina datos estructurados (superficie, precios, habitaciones) con metadatos adicionales (amenities, ubicación, servicios cercanos).

---

## Resultado final

genera un archivo CSV con la siguiente estructura:

| comuna | titulo | precio_uf | m2_totales | m2_construidos | banos | dormitorios | estacionamientos | antiguedad_anos | jardin | piscina | quincho | condominio_cerrado | educacion | comercios | salud | direccion | url |
| ------ | ------ | --------- | ---------- | -------------- | ----- | ----------- | ---------------- | --------------- | ------ | ------- | ------- | ------------------ | --------- | --------- | ----- | --------- | --- |

Estos archivos fueron posteriormente combinados y utilizados para el **análisis exploratorio de datos (EDA)** del proyecto.

---

