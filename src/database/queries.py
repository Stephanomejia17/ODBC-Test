from config.settings import DEPOSITO_ID
from datetime import datetime
import random


class DatabaseQueries:
    @staticmethod
    def get_producto_existencia(cursor, codigo_producto):
        query = f"""
            SELECT FT_EXISTENCIA
            FROM SinvDep
            WHERE FT_CODIGOPRODUCTO = '{codigo_producto}'
            AND FT_CODIGODEPOSITO = {DEPOSITO_ID}
        """
        cursor.execute(query)
        return cursor.fetchone()

    @staticmethod
    def get_materias_primas(cursor, codigo_producto):
        query = f"""
            SELECT e.FEN_CODEPARTE AS FED_PRODUCTO, 
                   e.FEN_CANTIDAD AS FED_CANTIDAD, 
                   s.FT_EXISTENCIA
            FROM SEnsambles e
            JOIN SinvDep s 
              ON s.FT_CODIGOPRODUCTO = e.FEN_CODEPARTE
             AND s.FT_CODIGODEPOSITO = {DEPOSITO_ID}
            WHERE e.FEN_CODIGO = '{codigo_producto}'
              AND e.FEN_CODEPARTE <> '$$$$$$$$$'
        """
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_siguiente_documento(cursor, tabla, campo_documento):
        query = f"""
            SELECT MAX({campo_documento}) AS MAX_DOC
            FROM {tabla}
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if result and result.MAX_DOC:
            return str(int(result.MAX_DOC) + 1).zfill(8)
        return "00000001"

    @staticmethod
    def get_costo_producto(cursor, codigo_producto, deposito_id):
        query = f"""
            SELECT FT_INVENTARIOINICIALBS, FT_INVENTARIOINICIALUND
            FROM SinvDep
            WHERE FT_CODIGOPRODUCTO = '{codigo_producto}'
            AND FT_CODIGODEPOSITO = {deposito_id}
        """
        cursor.execute(query)
        r = cursor.fetchone()
        if r and r.FT_INVENTARIOINICIALUND:
            return r.FT_INVENTARIOINICIALBS / r.FT_INVENTARIOINICIALUND
        return 0.0

    @staticmethod
    def get_deposito_destino(cursor):
        cursor.execute("SELECT DEPOSITO_ENSAMBLEDESTINO FROM SSistema")
        r = cursor.fetchone()
        if r and r.DEPOSITO_ENSAMBLEDESTINO:
            dep = int(str(r.DEPOSITO_ENSAMBLEDESTINO).strip())
            if dep == DEPOSITO_ID:
                raise Exception("Depósito origen y destino no pueden ser iguales")
            return dep
        return 2 if DEPOSITO_ID != 2 else 1

    @staticmethod
    def procesar_ensamble_completo(cursor, codigo_producto, cantidad_fabricar):
        fecha = datetime.now().strftime('%Y-%m-%d')
        fecha_sys = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hora = datetime.now().strftime('%H:%M:%S')

        deposito_destino = DatabaseQueries.get_deposito_destino(cursor)

        doc_ensamble = DatabaseQueries.get_siguiente_documento(
            cursor, 'SEnsamblesOrden', 'FEO_DOCUMENTO'
        )
        doc_operacion = DatabaseQueries.get_siguiente_documento(
            cursor, 'SOperacionInv', 'FTI_DOCUMENTO'
        )

        materias = DatabaseQueries.get_materias_primas(cursor, codigo_producto)
        serial = random.randint(100000000, 999999999)

        for mp in materias:
            consumo = cantidad_fabricar * mp.FED_CANTIDAD
            costo = DatabaseQueries.get_costo_producto(cursor, mp.FED_PRODUCTO, DEPOSITO_ID)

            cursor.execute(f"""
                INSERT INTO SDetalleInv (
                    FDI_TIPOOPERACION, FDI_CODIGO, FDI_LINEA, FDI_DOCUMENTO,
                    FDI_DOCUMENTOORIGEN, FDI_CLASIFICACION, FDI_STATUS, FDI_VISIBLE,
                    FDI_COSTO, FDI_CANTIDAD, FDI_DEPOSITOSOURCE, FDI_DEPOSITOTARGET,
                    FDI_DECIMALES, FDI_DECIMALESPEN, FDI_SERIALNUMBER,
                    FDI_USASERIALES, FDI_USADEPOSITOS, FDI_COSTOOPERACION,
                    FDI_MONEDA, FDI_FACTORCAMBIO, FDI_UNDDESCARGA,
                    FDI_UNDCAPACIDAD, FDI_UNDDETALLADA, FDI_FECHAOPERACION,
                    FDI_USER
                ) VALUES (
                    1, '{mp.FED_PRODUCTO}', 0, '{doc_operacion}', '{doc_ensamble}',
                    1, 1, 1, {costo}, {consumo},
                    {DEPOSITO_ID}, {deposito_destino},
                    1, 1, {serial}, 0, 1, {costo},
                    1, 1, 1, 1, 0, '{fecha}', 1
                )
            """)

        for mp in materias:
            consumo = cantidad_fabricar * mp.FED_CANTIDAD
            costo = DatabaseQueries.get_costo_producto(cursor, mp.FED_PRODUCTO, DEPOSITO_ID)

            cursor.execute(f"""
                INSERT INTO SEnsamblesDetalle (
                    FED_DOCUMENTO, FED_PRODUCTO, FED_CODEPRINCIPAL,
                    FED_CANTIDAD, FED_CANTIDADDESCARGA, FED_COSTOUNITARIO,
                    FED_ORIGENAUTO, FED_FACTORPRESENTA, FED_CANTIDADCIERRE,
                    FED_ESPRESENTA, FED_TIPOOFERTA, FED_RANDOMOPERACION,
                    FED_EXISTENCIA, FED_EXISTENCIADETALLE, FED_FECHAEMISION,
                    FED_STATUS
                ) VALUES (
                    '{doc_ensamble}', '{mp.FED_PRODUCTO}', '{codigo_producto}',
                    {consumo}, 1, {costo}, 0, 1, 0, 0, 0,
                    {serial}, {mp.FT_EXISTENCIA}, 0, '{fecha}', 4
                )
            """)

        cursor.execute("""
            UPDATE SSistema
            SET NO_TRANSFERENCIAS = NO_TRANSFERENCIAS + 1,
                NO_ORDENENSAMBLE = NO_ORDENENSAMBLE + 1
        """)

        for mp in materias:
            consumo = cantidad_fabricar * mp.FED_CANTIDAD

            cursor.execute(f"""
                UPDATE SinvDep
                SET FT_EXISTENCIA = FT_EXISTENCIA - {consumo}
                WHERE FT_CODIGOPRODUCTO = '{mp.FED_PRODUCTO}'
                AND FT_CODIGODEPOSITO = {DEPOSITO_ID}
            """)

            cursor.execute(f"""
                UPDATE SinvDep
                SET FT_EXISTENCIA = FT_EXISTENCIA + {consumo}
                WHERE FT_CODIGOPRODUCTO = '{mp.FED_PRODUCTO}'
                AND FT_CODIGODEPOSITO = {deposito_destino}
            """)

        # ⚠️ CORRECCIÓN PRINCIPAL: Incluir TODOS los campos que A2 requiere
        cursor.execute(f"""
            INSERT INTO SEnsamblesOrden (
                FEO_DOCUMENTO, FEO_CODEPRODUCTO, FEO_CANTIDADORDEN,
                FEO_FECHAEMISION, FEO_FECHAENTREGA, FEO_HORAEMISION,
                FEO_STATUS, FEO_USUARIO, FEO_COMPUTERNAME,
                FEO_CLASIFICACODE, FEO_CANTIDADCIERRE,
                FEO_COSTOINICIAL, FEO_COSTOFINAL,
                FEO_OTROCOSTO1, FEO_OTROCOSTO1PORCENT,
                FEO_OTROCOSTO2, FEO_OTROCOSTO2PORCENT,
                FEO_OTROCOSTO3, FEO_OTROCOSTO3PORCENT,
                FEO_OTROCOSTOCIERRE1, FEO_OTROCOSTOCIERRE1PORCENT,
                FEO_OTROCOSTOCIERRE2, FEO_OTROCOSTOCIERRE2PORCENT,
                FEO_OTROCOSTOCIERRE3, FEO_OTROCOSTOCIERRE3PORCENT,
                FEO_NOITEMSINICIO, FEO_NOITEMSFINAL
            ) VALUES (
                '{doc_ensamble}', '{codigo_producto}', {cantidad_fabricar},
                '{fecha}', '1899-12-30', '{hora}', 
                4, 'MASTER', 'PYTHON',
                1, 0,
                0, 0,
                0, 0,
                0, 0,
                0, 0,
                0, 0,
                0, 0,
                0, 0,
                0, 0
            )
        """)

        cursor.execute(f"""
            INSERT INTO SOperacionInv (
                FTI_DOCUMENTO, FTI_TIPO, FTI_STATUS, FTI_FECHAEMISION
            ) VALUES (
                '{doc_operacion}', 1, 1, '{fecha_sys}'
            )
        """)

        return doc_ensamble