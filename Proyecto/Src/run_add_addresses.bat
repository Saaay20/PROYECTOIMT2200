@echo off
echo =======================================================
echo  AÑADIR DIRECCIONES A CSV USANDO SCRAPER CON SESION
echo =======================================================

REM 
set INPUT_FILE=Dataset_viviendas.csv
set OUTPUT_FILE=Dataset_viviendas_con_direccion.csv
set COOKIES_FILE=ml_cookies.pkl
REM 

echo.
echo  Este script abrira una ventana de Chrome para funcionar.
echo  Es necesario para evitar que el sitio nos bloquee.
echo.
pause

REM generar cookies 
set /p generate_cookies="Necesitas generar/actualizar las cookies de sesion (s/n)? "
if /I "%generate_cookies%"=="s" (
  echo.
  echo      >> Abriendo navegador para login manual...
  py -3.11 test_login.py
)

REM ejecutar el script para extraer direcciones
echo.
echo  >> Iniciando la extraccion de direcciones para el archivo '%INPUT_FILE%'...
echo.
py -3.11 add_addresses.py --input "%INPUT_FILE%" --output "%OUTPUT_FILE%" --cookies "%COOKIES_FILE%"

if errorlevel 1 (
  echo.
  echo  ERROR: El script finalizo con errores.
) else (
  echo.
  echo  PROCESO COMPLETADO: Se guardo el archivo en '%OUTPUT_FILE%'.
)

echo.
pause