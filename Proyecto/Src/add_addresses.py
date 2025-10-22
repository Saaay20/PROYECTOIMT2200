#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para AÑADIR DIRECCIONES usando el motor del scraper principal.
- Utiliza Selenium para cargar la página y la sesión.
- Utiliza BeautifulSoup para analizar el HTML y extraer la dirección.
- Guarda el progreso en un archivo CSV.
"""

import pandas as pd
import time
import random
import os
import argparse
from tqdm import tqdm
import pickle

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup

class AddressScraper:
    def __init__(self, cookies_path: str, headless=True):
        self.cookies_path = cookies_path
        opts = webdriver.ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=opts)
            self.load_cookies()
        except WebDriverException as e:
            raise SystemExit(f"no se pudo iniciar ChromeDriver: {e}")

    def load_cookies(self):
        if not self.cookies_path or not os.path.exists(self.cookies_path):
            print("ADVERTENCIA: No se encontró el archivo de cookies.")
            return
        
        self.driver.get("https://www.portalinmobiliario.com")
        time.sleep(1)
        with open(self.cookies_path, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        print("Cookies cargadas. Refrescando sesión...")
        self.driver.refresh()
        time.sleep(2)

    def get_address_from_url(self, url: str) -> str | None:
      
        try:
            self.driver.get(url)
            
            WebDriverWait(self.driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            time.sleep(1) 
            
            # Pasa el HTML renderizado a beautifulsoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Ubicación
            location_header = soup.find('h2', string=lambda text: text and 'Ubicación' in text)
            if location_header:
                location_div = location_header.find_next_sibling('div')
                if location_div:
                    address_p = location_div.find('p')
                    if address_p and address_p.text:
                        return address_p.text.strip()

            # Direccion sobre el precio
            subtitle = soup.find('div', class_='ui-pdp-location__subtitle')
            if subtitle and subtitle.text:
                return subtitle.text.strip()

            # Ruta 
            breadcrumb = soup.find('nav', class_='ui-pdp-breadcrumb')
            if breadcrumb:
                parts = [a.text for a in breadcrumb.find_all('a')]
                if len(parts) > 1:
                    return " > ".join(parts[-3:])
            
            return None # Si falla

        except TimeoutException:
            print(f"la pagina tardo demasiado en cargar: {url}")
            return None
        except Exception as e:
            print(f"error grave procesando {url}: {e}")
            return None

    def close(self):
        try: self.driver.quit()
        except Exception: pass

def main():
    ap = argparse.ArgumentParser(description="Añadir direcciones a un CSV (versión BeautifulSoup).")
    ap.add_argument("--input", default="Dataset_viviendas.csv", help="Ruta al CSV de entrada.")
    ap.add_argument("--output", default="Dataset_viviendas_con_direccion.csv", help="Ruta para guardar el nuevo CSV.")
    ap.add_argument("--cookies", default="ml_cookies.pkl", help="Ruta al archivo de cookies.")
    args = ap.parse_args()

    try:
        df = pd.read_csv(args.input)
    except FileNotFoundError:
        raise SystemExit(f" No se encontró el archivo de entrada: {args.input}")

    progreso_file = args.output.replace('.csv', '_progress.csv')
    direcciones = []
    
    if os.path.exists(progreso_file):
        df_progreso = pd.read_csv(progreso_file)
        # Convertimos la columna de direcciones a una lista, manejando posibles NaN
        direcciones = df_progreso['direccion'].astype(str).where(df_progreso['direccion'].notna(), None).tolist()
        print(f"Reanudando proceso. Ya se han procesado {len(direcciones)} URLs.")

    urls_a_procesar = df['url'][len(direcciones):]
    if urls_a_procesar.empty:
        
        return

    scraper = AddressScraper(cookies_path=args.cookies, headless=False)
    try:
       
        with open(progreso_file, 'a', encoding='utf-8', newline='') as f_progreso:
            
            if not direcciones:
                f_progreso.write('url,direccion\n')

            for url in tqdm(urls_a_procesar, desc="Extrayendo direcciones"):
                direccion = scraper.get_address_from_url(url)
                
                print(f"-> URL: {url} | Dirección: {direccion}")
                
                direcciones.append(direccion)
                
                
                direccion_csv = f'"{direccion}"' if direccion else '""'
                f_progreso.write(f'"{url}",{direccion_csv}\n')

                time.sleep(random.uniform(1, 2))

    finally:
        scraper.close()
        

    if len(direcciones) == len(df):
        df['direccion'] = direcciones
        df.to_csv(args.output, index=False)
        print("\n" + "="*50)
        print(f"completado archivo guardado en: '{args.output}'")
        print("="*50)
    else:
        print("ERROR")

if __name__ == "__main__":
    main()