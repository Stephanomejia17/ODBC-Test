import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.dirname(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, 'Empre001', 'Data')

DB_CONFIG = {
    'driver': 'DBISAM 4 ODBC Driver',
    'connection_type': 'Local',
    'catalog': DATA_PATH,
    'database': DATA_PATH,
    'username': 'admin',
    'password': ''
}

APP_CONFIG = {
    'window_title': 'Sistema de troquelado',
    'window_width': 1000,
    'window_height': 800,
}

DEPOSITO_ID = 1

if not getattr(sys, 'frozen', False):
    print(f"🔍 DEBUG - Rutas configuradas:")
    print(f"   BASE_DIR: {BASE_DIR}")
    print(f"   DATA_PATH: {DATA_PATH}")
    print(f"   Existe DATA_PATH: {os.path.exists(DATA_PATH)}")