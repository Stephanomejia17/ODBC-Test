from config.settings import DEPOSITO_ID

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
            SELECT d.FED_PRODUCTO, d.FED_CANTIDAD, s.FT_EXISTENCIA
            FROM SEnsamblesDetalle d
            JOIN SinvDep s
              ON s.FT_CODIGOPRODUCTO = d.FED_PRODUCTO
             AND s.FT_CODIGODEPOSITO = {DEPOSITO_ID}
            WHERE d.FED_CODEPRINCIPAL = '{codigo_producto}'
        """
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def actualizar_producto_terminado(cursor, codigo_producto, cantidad):
        query = f"""
            UPDATE SinvDep
            SET FT_EXISTENCIA = FT_EXISTENCIA + {cantidad}
            WHERE FT_CODIGOPRODUCTO = '{codigo_producto}'
            AND FT_CODIGODEPOSITO = {DEPOSITO_ID}
        """
        cursor.execute(query)

    @staticmethod
    def descontar_materia_prima(cursor, codigo_producto, cantidad):
        query = f"""
            UPDATE SinvDep
            SET FT_EXISTENCIA = FT_EXISTENCIA - {cantidad}
            WHERE FT_CODIGOPRODUCTO = '{codigo_producto}'
            AND FT_CODIGODEPOSITO = {DEPOSITO_ID}
        """
        cursor.execute(query)