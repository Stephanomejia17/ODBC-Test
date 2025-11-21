import pyodbc

try:
    conn = pyodbc.connect(
        r"DRIVER={DBISAM 4 ODBC Driver};"
        r"ConnectionType=Local;"
        r"CatalogName=C:\Users\steph\OneDrive\Documentos\a2SoftwareFE - copia\a2SoftwareFE - copia\a2SoftwareFE - copia\Empre001\Data;"
        r"DatabaseName=C:\Users\steph\OneDrive\Documentos\a2SoftwareFE - copia\a2SoftwareFE - copia\a2SoftwareFE - copia\Empre001\Data;"
        r"UserName=admin;"
        r"Password=;"
    )

    cur = conn.cursor()
    unidades = int(input("Ingrese las unidades a agregar: "))
    cur.execute("SELECT * FROM SinvDep WHERE FT_CODIGOPRODUCTO = '19833673'")
    cur.execute(f"UPDATE SinvDep SET FT_EXISTENCIA = FT_EXISTENCIA + {unidades} WHERE FT_CODIGOPRODUCTO = '19833673'")
    cur.execute("SELECT * FROM SinvDep WHERE FT_CODIGOPRODUCTO = '19833673'")

    rows = cur.fetchall()
    print("Registros:", len(rows))
    for i, r in enumerate(rows):
        print(i, ". ", r)

except Exception as e:
    print("error:", e)

finally:
    try: conn.close()
    except: pass
