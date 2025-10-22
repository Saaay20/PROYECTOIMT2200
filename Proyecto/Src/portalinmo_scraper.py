#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PortalInmobiliario.com – Scraper de CASAS y DEPARTAMENTOS en venta por comuna (RM)

- Extrae: comuna, titulo, precio_uf, m2_totales, m2_construidos, banos,
          dormitorios, antiguedad_anos, estacionamientos, jardin, piscina,
          quincho, condominio_cerrado, educacion, comercios, salud, url
- Maneja muro de login (cookies opcionales con --cookies).
- Reanuda si el CSV ya existe y corta exactamente en --max filas.
- SIN webdriver_manager (usa Selenium Manager).
- Lógica de parsing actualizada con BeautifulSoup para mayor robustez.
- Versión flexible: m2_totales se copia de m2_construidos y dormitorios es opcional.
"""

import re
import os
import time
import random
import argparse
import pickle
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict

import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def parse_number_smart(text: Optional[str]):
    if not text: return None
    s = re.sub(r"[^\d,\.]", "", text.strip())
    if not s: return None
    if '.' in s and ',' in s: s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        parts = s.split(',')
        if len(parts[-1]) <= 2: s = s.replace(',', '.')
        else: s = s.replace(',', '')
    elif '.' in s:
        parts = s.split('.')
        if len(parts) > 2 or (len(parts) == 2 and len(parts[-1]) == 3):
            s = s.replace('.', '')
    try: return float(s)
    except (ValueError, TypeError): return None

def to_int(x):
    if x is None: return None
    try:
        if isinstance(x, str): x = parse_number_smart(x)
        if x is None: return None
        return int(float(x))
    except (ValueError, TypeError): return None

def to_float(x):
    if x is None: return None
    try:
        if isinstance(x, str): return parse_number_smart(x)
        return float(x)
    except (ValueError, TypeError): return None

def _offset_url(url: str, offset: int) -> str:
    import urllib.parse as u
    parsed = u.urlparse(url)
    path = parsed.path
    if "_Desde_" in path:
        path = re.sub(r"_Desde_\d+", f"_Desde_{offset}", path)
    else:
        path = path.rstrip("/") + f"/_Desde_{offset}"
    return parsed._replace(path=path).geturl()

def _normalize_url(href: str) -> str:
    if not href: return ""
    href = href.split("#")[0]
    if href.startswith("/"): return "https://www.portalinmobiliario.com" + href
    return href

def _is_listing_url(href: str) -> bool:
    if not href: return False
    h = href.lower()
    if "portalinmobiliario.com" not in h: return False
    bad = ["_desde_", "/listado/", "/ayuda", "/favoritos", "/ofertas",
           "/tiendas-oficiales", "/perfil/", "/cart/", "/auth.", "/login",
           "/registration", "/buscar", "/search", "/user/"]
    if any(b in h for b in bad): return False
    good = ["/mlc-", "/mco-", "/mcu-", "/p/", "/propiedad/", "/casa-", "/venta-", "/departamento-"]
    return any(g in h for g in good)

def _human_scroll(driver, steps=3):
    h = driver.execute_script("return document.body.scrollHeight")
    for i in range(steps):
        y = int((i+1) * h / (steps+1))
        driver.execute_script(f"window.scrollTo(0,{y});")
        time.sleep(random.uniform(0.6, 1.2))

def _fmt_eta(seconds: float) -> str:
    seconds = max(0, int(seconds))
    m, s = divmod(seconds, 60); h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"



@dataclass
class Casa:
    comuna: Optional[str]
    titulo: Optional[str]
    precio_uf: Optional[float]
    m2_totales: Optional[float]
    m2_construidos: Optional[float]
    banos: Optional[int]
    dormitorios: Optional[int]
    antiguedad_anos: Optional[int]
    estacionamientos: Optional[int]
    jardin: bool
    piscina: bool
    quincho: bool
    condominio_cerrado: bool
    educacion: bool
    comercios: bool
    salud: bool
    url: str

# ---------------------------- scraper ----------------------------

class Scraper:
    def __init__(self, headless=True, wait=20, cookies_path: Optional[str]=None, verbose=True):
        self.wait = wait
        self.cookies_path = cookies_path
        self.verbose = verbose
        opts = Options()
        if headless: opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--lang=es-CL")
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36")
        opts.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        try: self.driver = webdriver.Chrome(options=opts)
        except WebDriverException as e: raise SystemExit(f"No se pudo iniciar ChromeDriver: {e}")
        self.driver.set_page_load_timeout(60)

    def close(self):
        try: self.driver.quit()
        except Exception: pass

    def load_cookies(self, base_url: str):
        if not self.cookies_path or not os.path.exists(self.cookies_path): return
        self.driver.get(base_url)
        time.sleep(2)
        with open(self.cookies_path, "rb") as f: cookies = pickle.load(f)
        for c in cookies:
            c.pop('sameSite', None)
            try: self.driver.add_cookie(c)
            except Exception: pass
        self.driver.refresh()
        time.sleep(2)

    def save_cookies(self):
        if not self.cookies_path: return
        with open(self.cookies_path, "wb") as f: pickle.dump(self.driver.get_cookies(), f)

    def _on_login_wall(self) -> bool:
        try:
            url = (self.driver.current_url or "").lower()
            if "auth.mercadolibre" in url or "login" in url: return True
        except Exception: pass
        try:
            title = (self.driver.title or "").lower()
            if any(x in title for x in ["ingresa", "login", "cuenta"]): return True
        except Exception: pass
        return False

    def collect_listing_urls(self, search_url: str, max_urls: int) -> List[str]:
        urls: List[str] = []
        if self.cookies_path and os.path.exists(self.cookies_path):
            self.load_cookies("https://www.portalinmobiliario.com/")
        offset, page = 1, 1
        while len(urls) < max_urls and offset <= 5000:
            page_url = search_url if offset == 1 else _offset_url(search_url, offset)
            if self.verbose: print(f"[URLs] Página {page} ⇒ {page_url}")
            self.driver.get(page_url)
            time.sleep(random.uniform(2, 3.5))
            if self._on_login_wall():
                print("[LOGIN] Inicia sesión en la ventana y vuelve aquí. ENTER para continuar…")
                input(); self.save_cookies(); self.driver.get(page_url); time.sleep(2)
            for sel in ["button.cookies-banner__accept-button", "button[data-testid='action:understood-button']", ".cookie-consent-banner-opt-out__accept", "#newCookieDisclaimerButton"]:
                try: WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel))).click(); break
                except Exception: pass
            try: WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui-search-results")))
            except TimeoutException: print("[WARNING] Timeout esperando resultados")
            _human_scroll(self.driver, steps=4)
            found = set()
            selectors = ["a[href*='/MLC-']", "a[href*='/p/']", "a[href*='/propiedad/']", "li.ui-search-layout__item a", "a.ui-search-link"]
            for s in selectors:
                for a in self.driver.find_elements(By.CSS_SELECTOR, s):
                    href = _normalize_url(a.get_attribute("href") or "")
                    if _is_listing_url(href): found.add(href)
            before = len(urls)
            for u in found:
                urls.append(u)
                if len(urls) >= max_urls: break
            if self.verbose: print(f"[URLs] Página {page}: +{len(urls)-before} (total {len(urls)}/{max_urls})")
            if len(urls) == before and page > 1: break
            offset += 48; page += 1
        out, seen = [], set()
        for u in urls:
            if u not in seen: out.append(u); seen.add(u)
        if self.verbose: print(f"[URLS FINAL] Total únicas: {len(out)}")
        return out[:max_urls]
    
    def parse_listing(self, url: str, comuna_tag: str) -> Optional[Casa]:
        d = self.driver
        base = d.current_window_handle
        d.execute_script("window.open(arguments[0], '_blank')", url)
        time.sleep(random.uniform(0.7, 1.5))
        d.switch_to.window(d.window_handles[-1])

        try:
            WebDriverWait(d, self.wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        except TimeoutException:
            d.close(); d.switch_to.window(base); return None

        html = d.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        titulo = soup.find("h1", class_="ui-pdp-title")
        titulo = titulo.text.strip() if titulo else None
        
        comuna = comuna_tag
        crumbs = soup.select("nav.ui-pdp-breadcrumb a")
        if crumbs: comuna = crumbs[-1].text.strip()
        
        precio_uf = None
        try:
            price_container = soup.find('div', class_='ui-pdp-price')
            if price_container:
                price_fraction = price_container.find('span', class_='andes-money-amount__fraction')
                currency_symbol = price_container.find('span', class_='andes-money-amount__currency-symbol')
                if price_fraction and currency_symbol and 'UF' in currency_symbol.text:
                    precio_uf = to_float(price_fraction.text.strip())
        except Exception: pass
        
        key_map = {'superficie total': 'm2_totales', 'superficie útil': 'm2_construidos', 'superficie construida': 'm2_construidos', 'dormitorios': 'dormitorios', 'baños': 'banos', 'estacionamientos': 'estacionamientos', 'antigüedad': 'antiguedad_anos', 'jardín': 'jardin', 'piscina': 'piscina', 'quincho': 'quincho'}
        data: Dict[str, any] = {}
        h_principales = soup.find(lambda tag: tag.name in ['h2', 'h3'] and 'principales' in tag.text.lower())
        if h_principales:
            table = h_principales.find_next_sibling("table", class_="andes-table")
            if table:
                for row in table.find_all("tr"):
                    key_el, val_el = row.find("th"), row.find("td")
                    if key_el and val_el:
                        key, val = key_el.text.strip().lower(), val_el.text.strip()
                        if key in key_map:
                            if val.lower() in ['sí', 'si']: data[key_map[key]] = True
                            else: data[key_map[key]] = val

        m2_totales = to_float(data.get('m2_totales'))
        m2_construidos = to_float(data.get('m2_construidos'))
        dormitorios = to_int(data.get('dormitorios'))
        banos = to_int(data.get('banos'))
        estacionamientos = to_int(data.get('estacionamientos'))
        antiguedad_anos = to_int(data.get('antiguedad_anos'))

        if m2_totales is None and m2_construidos is not None:
            m2_totales = m2_construidos

       
        if any(v is None for v in [m2_construidos, banos]):
            d.close(); d.switch_to.window(base); return None
        
        
        if dormitorios is None:
            dormitorios = 1
       

        if antiguedad_anos is None: antiguedad_anos = 0

        html_lower = html.lower()
        jardin = data.get('jardin', 'jardín' in html_lower)
        piscina = data.get('piscina', 'piscina' in html_lower)
        quincho = data.get('quincho', 'quincho' in html_lower)
        condominio_cerrado = 'condominio' in html_lower
        educacion = bool(re.search(r'educaci[óo]n.*?(?:\d+\s*(?:metros|min))', html, re.I | re.S))
        comercios = bool(re.search(r'comercios?.*?(?:\d+\s*(?:metros|min))', html, re.I | re.S))
        salud = bool(re.search(r'salud.*?(?:\d+\s*(?:metros|min))', html, re.I | re.S))

        casa = Casa(comuna=comuna, titulo=titulo, precio_uf=precio_uf, m2_totales=m2_totales,
                    m2_construidos=m2_construidos, banos=banos, dormitorios=dormitorios, antiguedad_anos=antiguedad_anos, 
                    estacionamientos=estacionamientos, jardin=bool(jardin), piscina=bool(piscina),
                    quincho=bool(quincho), condominio_cerrado=bool(condominio_cerrado), educacion=educacion, comercios=comercios, salud=salud, url=url)
        d.close(); d.switch_to.window(base)
        return casa


def main():
    ap = argparse.ArgumentParser(description="Scraper de Casas y Departamentos – PortalInmobiliario")
    ap.add_argument("--search-url", required=True)
    ap.add_argument("--comuna", required=True)
    ap.add_argument("--max", type=int, default=200)
    ap.add_argument("--out", default="propiedades.csv")
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--cookies", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    scraper = Scraper(headless=args.headless, cookies_path=args.cookies, verbose=not args.quiet)
    try:
        t0 = time.time()
        prev = None; seen_urls = set()
        if os.path.exists(args.out):
            try:
                prev = pd.read_csv(args.out)
                if "url" in prev.columns: seen_urls = set(prev["url"].dropna().astype(str))
                print(f"[resume] Ya había {len(prev)} filas en {args.out}")
            except Exception: pass
        if prev is not None and len(prev) >= args.max:
            print(f"[OK] Ya tienes {len(prev)} >= {args.max}."); return
        
        faltan = args.max - (len(prev) if prev is not None else 0)
        print(f"[resume] Faltan {faltan} filas para llegar a {args.max}")

        urls_raw = scraper.collect_listing_urls(args.search_url, max_urls=int(faltan * 2.5))
        urls = [u for u in urls_raw if u not in seen_urls]
        print(f"[resume] URLs nuevas candidatas: {len(urls)}")

        results: List[Casa] = []; per_item_times: List[float] = []
        done_start = 0 if prev is None else len(prev)
        checkpoint = 25

        def flush(rows: List[Casa], final=False):
            nonlocal prev
            if not rows and not final: return
            df_new = pd.DataFrame([asdict(x) for x in rows]) if rows else pd.DataFrame()
            if not df_new.empty:
                for c in ["m2_totales", "m2_construidos", "precio_uf"]:
                    if c in df_new.columns: df_new[c] = pd.to_numeric(df_new[c], errors="coerce")
                for c in ["banos", "dormitorios", "antiguedad_anos", "estacionamientos"]:
                    if c in df_new.columns: df_new[c] = pd.to_numeric(df_new[c], errors="coerce").astype("Int64")
                bool_cols = ["jardin", "piscina", "quincho", "condominio_cerrado", "educacion", "comercios", "salud"]
                for c in bool_cols:
                    if c in df_new.columns: df_new[c] = df_new[c].fillna(False).astype(bool)
                if "comuna" not in df_new.columns: df_new.insert(0, "comuna", args.comuna)
                else: df_new["comuna"] = df_new["comuna"].fillna(args.comuna)

            df_out = df_new if prev is None else pd.concat([prev, df_new], ignore_index=True)
            if "url" in df_out.columns: df_out = df_out.drop_duplicates(subset=["url"], keep="first")
            df_out = df_out.iloc[:args.max]
            tmp = args.out + ".tmp"; df_out.to_csv(tmp, index=False, encoding="utf-8")
            os.replace(tmp, args.out)
            prev = df_out
            if final: print(f"[OK] Guardado {len(df_out)} filas en {args.out} — { _fmt_eta(time.time()-t0) }")
            else: print(f"[checkpoint] Guardadas {len(df_out)} filas")

        for i, u in enumerate(urls, start=1):
            t1 = time.time()
            c = scraper.parse_listing(u, args.comuna)
            per_item_times.append(time.time()-t1)
            if c: results.append(c)

            total_done = done_start + len(results)
            if total_done >= args.max:
                print(f"[{total_done:>3}/{args.max}] Límite alcanzado, finalizando...")
                break
            
            remaining = args.max - total_done
            avg = sum(per_item_times[-10:]) / len(per_item_times[-10:])
            eta = _fmt_eta(remaining * avg)
            title_snip = (c.titulo[:55] + "…") if (c and c.titulo and len(c.titulo) > 55) else (c.titulo if c else "")
            print(f"[{total_done:>3}/{args.max}] ETA {eta} — {title_snip}")

            if len(results) > 0 and (len(results) % checkpoint == 0):
                flush(results); results = []

        flush(results, final=True)
    finally:
        scraper.close()

if __name__ == "__main__":
    main()