import pandas as pd


class ExcelHandler:
    @staticmethod
    def read_excel(filepath):
        try:
            df = pd.read_excel(
                filepath,
                dtype={"FT_CODIGOPRODUCTO": str}
            )

            # Validar columnas requeridas
            required_cols = {"FT_CODIGOPRODUCTO", "NO_FABRICADOS"}
            if not required_cols.issubset(df.columns):
                raise ValueError(
                    f"El Excel debe contener las columnas: {', '.join(required_cols)}"
                )

            return df

        except Exception as e:
            raise Exception(f"Error al leer el archivo Excel: {e}")

    @staticmethod
    def validate_data(df):
        # Validar que no haya valores nulos
        if df["FT_CODIGOPRODUCTO"].isnull().any():
            return False

        if df["NO_FABRICADOS"].isnull().any():
            return False

        # Validar que NO_FABRICADOS sea numérico positivo
        if (df["NO_FABRICADOS"] <= 0).any():
            return False

        return True