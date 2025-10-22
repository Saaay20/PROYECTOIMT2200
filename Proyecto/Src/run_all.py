import subprocess
import os
import time


# Agregar aquí comunas a scrapear.
# Dicc con nombre:url.


COMUNAS_A_SCRAPEAR = [
    {"nombre": "Santiago", "url": "https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana/_DisplayType_LF"},
    {"nombre": "Cerrillos", "url": "https://www.portalinmobiliario.com/venta/departamento/cerrillos-metropolitana/_DisplayType_LF"},
    {"nombre": "Cerro Navia", "url": "https://www.portalinmobiliario.com/venta/departamento/cerro-navia-metropolitana/_DisplayType_LF"},
    {"nombre": "Conchalí", "url": "https://www.portalinmobiliario.com/venta/departamento/conchali-metropolitana/_DisplayType_LF"},
    {"nombre": "El Bosque", "url": "https://www.portalinmobiliario.com/venta/departamento/el-bosque-metropolitana/_DisplayType_LF"},
    {"nombre": "Estación Central", "url": "https://www.portalinmobiliario.com/venta/departamento/estacion-central-metropolitana/_DisplayType_LF"},
    {"nombre": "Huechuraba", "url": "https://www.portalinmobiliario.com/venta/departamento/huechuraba-metropolitana/_DisplayType_LF"},
    {"nombre": "Independencia", "url": "https://www.portalinmobiliario.com/venta/departamento/independencia-metropolitana/_DisplayType_LF"},
    {"nombre": "La Cisterna", "url": "https://www.portalinmobiliario.com/venta/departamento/la-cisterna-metropolitana/_DisplayType_LF"},
    {"nombre": "La Florida", "url": "https://www.portalinmobiliario.com/venta/departamento/la-florida-metropolitana/_DisplayType_LF"},
    {"nombre": "La Granja", "url": "https://www.portalinmobiliario.com/venta/departamento/la-granja-metropolitana/_DisplayType_LF"},
    {"nombre": "La Pintana", "url": "https://www.portalinmobiliario.com/venta/departamento/la-pintana-metropolitana/_DisplayType_LF"},
    {"nombre": "La Reina", "url": "https://www.portalinmobiliario.com/venta/departamento/la-reina-metropolitana/_DisplayType_LF"},
    {"nombre": "Las Condes", "url": "https://www.portalinmobiliario.com/venta/departamento/las-condes-metropolitana/_DisplayType_LF"},
    {"nombre": "Lo Barnechea", "url": "https://www.portalinmobiliario.com/venta/departamento/lo-barnechea-metropolitana/_DisplayType_LF"},
    {"nombre": "Lo Espejo", "url": "https://www.portalinmobiliario.com/venta/departamento/lo-espejo-metropolitana/_DisplayType_LF"},
    {"nombre": "Lo Prado", "url": "https://www.portalinmobiliario.com/venta/departamento/lo-prado-metropolitana/_DisplayType_LF"},
    {"nombre": "Macul", "url": "https://www.portalinmobiliario.com/venta/departamento/macul-metropolitana/_DisplayType_LF"},
    {"nombre": "Maipú", "url": "https://www.portalinmobiliario.com/venta/departamento/maipu-metropolitana/_DisplayType_LF"},
    {"nombre": "Ñuñoa", "url": "https://www.portalinmobiliario.com/venta/departamento/nunoa-metropolitana/_DisplayType_LF"},
    {"nombre": "Pedro Aguirre Cerda", "url": "https://www.portalinmobiliario.com/venta/departamento/pedro-aguirre-cerda-metropolitana/_DisplayType_LF"},
    {"nombre": "Peñalolén", "url": "https://www.portalinmobiliario.com/venta/departamento/penalolen-metropolitana/_DisplayType_LF"},
    {"nombre": "Providencia", "url": "https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana/_DisplayType_LF"},
    {"nombre": "Pudahuel", "url": "https://www.portalinmobiliario.com/venta/departamento/pudahuel-metropolitana/_DisplayType_LF"},
    {"nombre": "Quilicura", "url": "https://www.portalinmobiliario.com/venta/departamento/quilicura-metropolitana/_DisplayType_LF"},
    {"nombre": "Quinta Normal", "url": "https://www.portalinmobiliario.com/venta/departamento/quinta-normal-metropolitana/_DisplayType_LF"},
    {"nombre": "Recoleta", "url": "https://www.portalinmobiliario.com/venta/departamento/recoleta-metropolitana/_DisplayType_LF"},
    {"nombre": "Renca", "url": "https://www.portalinmobiliario.com/venta/departamento/renca-metropolitana/_DisplayType_LF"},
    {"nombre": "San Joaquín", "url": "https://www.portalinmobiliario.com/venta/departamento/san-joaquin-metropolitana/_DisplayType_LF"},
    {"nombre": "San Miguel", "url": "https://www.portalinmobiliario.com/venta/departamento/san-miguel-metropolitana/_DisplayType_LF"},
    {"nombre": "San Ramón", "url": "https://www.portalinmobiliario.com/venta/departamento/san-ramon-metropolitana/_DisplayType_LF"},
    {"nombre": "Vitacura", "url": "https://www.portalinmobiliario.com/venta/departamento/vitacura-metropolitana/_DisplayType_LF"},
    {"nombre": "Colina", "url": "https://www.portalinmobiliario.com/venta/departamento/colina-metropolitana/_DisplayType_LF"},
    {"nombre": "Puente Alto", "url": "https://www.portalinmobiliario.com/venta/departamento/puente-alto-metropolitana/_DisplayType_LF"},
    {"nombre": "San José de Maipo", "url": "https://www.portalinmobiliario.com/venta/departamento/san-jose-de-maipo-metropolitana/_DisplayType_LF"},
]
# propiedades a extraer por cada comuna
MAX_PROPIEDADES_POR_COMUNA = 200

# carpeta donde se guardarán los resultados
CARPETA_SALIDA = "..Data/raw"



def correr_scraper():
    # Crear la carpeta de salida si no existe
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)
        print(f"{CARPETA_SALIDA}' creada.")

    total_comunas = len(COMUNAS_A_SCRAPEAR)
    print(f"Iniciando scraping para {total_comunas} comunas.")

   
    if not os.path.exists("ml_cookies.pkl"):
        print("No se encontró el archivo 'ml_cookies.pkl'.")
        print("    py -3.11 test_login.py")
        input("    Presiona ENTER para continuar de todas formas...")

    
    for i, comuna_info in enumerate(COMUNAS_A_SCRAPEAR, 1):
        nombre_comuna = comuna_info["nombre"]
        url_busqueda = comuna_info["url"]

        # Formatear archivo de salida 
        nombre_archivo = nombre_comuna.lower().replace(" ", "_") + ".csv"
        ruta_salida = os.path.join(CARPETA_SALIDA, nombre_archivo)

        print("\n" + "="*60)
        print(f"⏳ ({i}/{total_comunas}) Procesando: {nombre_comuna}")
        print("="*60)

        # Construir el comando para llamar al scraper
        comando = [
            "py", "-3.11",
            ".\\portalinmo_scraper.py",
            "--search-url", url_busqueda,
            "--comuna", nombre_comuna,
            "--max", str(MAX_PROPIEDADES_POR_COMUNA),
            "--out", ruta_salida,
            "--cookies", "ml_cookies.pkl"
        ]

        try:
            # Ejecutar el comando
            subprocess.run(comando, check=True)
            print(f"Éxito para {nombre_comuna}")

        except subprocess.CalledProcessError:
            print(f"ERROR al procesar {nombre_comuna}. Saltando a la siguiente")
        except FileNotFoundError:
            
            break
        
        time.sleep(5)

    print("finalizado para todas las comunas")

if __name__ == "__main__":
    correr_scraper()