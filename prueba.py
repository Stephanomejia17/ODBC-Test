import pyodbc
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

excel_path = filedialog.askopenfilename(
    title="Seleccione el archivo Excel",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

if not excel_path:
    raise Exception("No se seleccionó ningún archivo Excel")

df = pd.read_excel(excel_path)

required_cols = {"FT_CODIGOPRODUCTO", "NO_FABRICADOS"}
if not required_cols.issubset(df.columns):
    raise Exception("El Excel debe contener las columnas FT_CODIGOPRODUCTO y NO_FABRICADOS")

conn = pyodbc.connect(
    r"DRIVER={DBISAM 4 ODBC Driver};"
    r"ConnectionType=Local;"
    r"CatalogName=C:\Users\steph\OneDrive\Documentos\a2SoftwareFE - copia\a2SoftwareFE - copia\a2SoftwareFE - copia\Empre001\Data;"
    r"DatabaseName=C:\Users\steph\OneDrive\Documentos\a2SoftwareFE - copia\a2SoftwareFE - copia\a2SoftwareFE - copia\Empre001\Data;"
    r"UserName=admin;"
    r"Password=;"
)

cur = conn.cursor()

for idx, row in df.iterrows():
    FT_CODIGOPRODUCTO = str(row["FT_CODIGOPRODUCTO"]).strip()
    NO_FABRICADOS = int(row["NO_FABRICADOS"])

    print("\n===================================")
    print(f"Procesando producto {FT_CODIGOPRODUCTO}")
    print(f"Cantidad a fabricar: {NO_FABRICADOS}")

    try:
        cur.execute(
            f"SELECT FT_EXISTENCIA FROM SinvDep WHERE FT_CODIGOPRODUCTO = '{FT_CODIGOPRODUCTO}'"
        )
        prod_ini = cur.fetchone()
        if not prod_ini:
            raise Exception(
                f"Producto {FT_CODIGOPRODUCTO} no existe en SinvDep"
            )

        cur.execute(
            f"""
            SELECT d.FED_PRODUCTO, d.FED_CANTIDAD, s.FT_EXISTENCIA
            FROM SEnsamblesDetalle d
            JOIN SinvDep s ON s.FT_CODIGOPRODUCTO = d.FED_PRODUCTO
            WHERE d.FED_CODEPRINCIPAL = '{FT_CODIGOPRODUCTO}'
            """
        )

        materias = cur.fetchall()
        if not materias:
            raise Exception(
                f"Producto {FT_CODIGOPRODUCTO} no tiene ensambles"
            )

        for mp in materias:
            consumo_total = int(NO_FABRICADOS * mp.FED_CANTIDAD)
            stock_actual = mp.FT_EXISTENCIA

            if stock_actual - consumo_total <= 0:
                raise Exception(
                    f"STOCK INSUFICIENTE | "
                    f"Producto: {FT_CODIGOPRODUCTO} | "
                    f"Materia prima: {mp.FED_PRODUCTO} | "
                    f"Stock actual: {stock_actual} | "
                    f"Consumo requerido: {consumo_total}"
                )

        cur.execute(
            f"""
            UPDATE SinvDep
            SET FT_EXISTENCIA = FT_EXISTENCIA + {NO_FABRICADOS}
            WHERE FT_CODIGOPRODUCTO = '{FT_CODIGOPRODUCTO}'
            """
        )

        for mp in materias:
            consumo_total = int(NO_FABRICADOS * mp.FED_CANTIDAD)
            cur.execute(
                f"""
                UPDATE SinvDep
                SET FT_EXISTENCIA = FT_EXISTENCIA - {consumo_total}
                WHERE FT_CODIGOPRODUCTO = '{mp.FED_PRODUCTO}'
                """
            )

        conn.commit()
        print("Fabricación aplicada correctamente")

    except Exception as e:
        conn.rollback()
        print("OPERACIÓN CANCELADA PARA ESTE PRODUCTO")
        print(e)
        continue

conn.close()
print("\nProceso finalizado")
