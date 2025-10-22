#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar cookies de Portal Inmobiliario / Mercado Libre
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time

def test_login():
    opts = Options()
    opts.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(options=opts)
    try:
        print("Abriendo Portal Inmobiliario...")
        driver.get("https://www.portalinmobiliario.com")
        time.sleep(3)
        print("\n" + "="*50)
        print("INSTRUCCIONES PARA LOGIN:")
        print("1. Inicia sesión manualmente en la ventana del navegador")
        print("2. Completa el proceso de login completamente")
        print("3. Cuando veas la página principal, regresa aquí")
        print("4. Presiona ENTER en esta terminal")
        print("="*50 + "\n")
        input("Presiona ENTER después de haber iniciado sesión...")
        cookies = driver.get_cookies()
        with open("ml_cookies.pkl", "wb") as f:
            pickle.dump(cookies, f)
        print("cookies guardadas correctamente en 'ml_cookies.pkl'!")
        print(f"se guardaron {len(cookies)} cookies")
    except Exception as e:
        print(f"error: {e}")
    finally:
        driver.quit()
        

if __name__ == "__main__":
    test_login()
