import pyodbc
from config.settings import DB_CONFIG

class DatabaseConnection:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            connection_string = (
                f"DRIVER={{{DB_CONFIG['driver']}}};"
                f"ConnectionType={DB_CONFIG['connection_type']};"
                f"CatalogName={DB_CONFIG['catalog']};"
                f"DatabaseName={DB_CONFIG['database']};"
                f"UserName={DB_CONFIG['username']};"
                f"Password={DB_CONFIG['password']};"
            )

            self.conn = pyodbc.connect(connection_string)
            return self.conn

        except pyodbc.Error as e:
            raise Exception(f"Error al conectar a la base de datos: {e}")

    def close(self, conn=None):
        connection = conn or self.conn
        if connection:
            try:
                connection.close()
            except Exception as e:
                print(f"Error al cerrar conexión: {e}")

    def get_cursor(self):
        if not self.conn:
            self.connect()
        return self.conn.cursor()