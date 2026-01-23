# Sistema de Fabricación

Sistema automatizado para gestión de inventario y fabricación con conexión a base de datos DBISAM.

## Requisitos

- Python 3.8+
- Driver DBISAM 4 ODBC instalado
- Windows (para DBISAM)

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar base de datos en `config/settings.py`

## Uso
```bash
python src/main.py
```

## Características

- Carga de archivos Excel con productos a fabricar
- Validación de stock de materias primas
- Actualización automática de inventario
- Consola de logs en tiempo real
- Interfaz gráfica intuitiva

## Estructura del Excel

El archivo Excel debe contener las columnas:
- `FT_CODIGOPRODUCTO`: Código del producto
- `NO_FABRICADOS`: Cantidad a fabricar