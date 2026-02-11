@echo off
REM ============================================================================
REM Script para crear el ejecutable del Sistema de Troquelado
REM (VERSION CORREGIDA v2 - Incluye todos los módulos)
REM ============================================================================

echo.
echo ========================================================================
echo CREANDO EJECUTABLE - SISTEMA DE TROQUELADO
echo ========================================================================
echo.

REM Activar entorno virtual
echo [1/4] Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Instalar PyInstaller si no está instalado
echo.
echo [2/4] Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no encontrado. Instalando...
    pip install pyinstaller
) else (
    echo PyInstaller ya esta instalado
)

REM Limpiar builds anteriores
echo.
echo [3/4] Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist SistemaTroquelado.spec del /q SistemaTroquelado.spec

REM Crear el ejecutable
echo.
echo [4/4] Creando ejecutable...
echo.
pyinstaller ^
    --windowed ^
    --name="SistemaTroquelado" ^
    --add-data="assets;assets" ^
    --paths=src ^
    --paths=src/gui ^
    --paths=src/database ^
    --paths=src/utils ^
    --paths=config ^
    --hidden-import=pyodbc ^
    --hidden-import=openpyxl ^
    --hidden-import=pandas ^
    --hidden-import=PIL ^
    --hidden-import=tkinter ^
    --hidden-import=_tkinter ^
    --hidden-import=gui ^
    --hidden-import=gui.main ^
    --hidden-import=database ^
    --hidden-import=database.connection ^
    --hidden-import=database.queries ^
    --hidden-import=utils ^
    --hidden-import=utils.excel_handler ^
    --hidden-import=utils.console_redirector ^
    --hidden-import=config ^
    --hidden-import=config.settings ^
    --hidden-import=assets.styles.colors ^
    --noconfirm ^
    src/main.py

echo.
echo ========================================================================
echo PROCESO COMPLETADO
echo ========================================================================
echo.
echo El ejecutable esta en: dist\SistemaTroquelado\SistemaTroquelado.exe
echo.
echo INSTRUCCIONES PARA USAR:
echo 1. Copia TODA la carpeta dist\SistemaTroquelado a donde esta A2
echo 2. Asegurate de que exista la carpeta Empre001\Data en el mismo lugar
echo.
echo Estructura esperada:
echo   C:\RutaDeA2\
echo   ├── SistemaTroquelado\
echo   │   ├── SistemaTroquelado.exe
echo   │   └── _internal\ (archivos necesarios)
echo   └── Empre001\
echo       └── Data\
echo           ├── SSistema.dat
echo           ├── SFixed.dat
echo           └── ...
echo.
echo ========================================================================

pause