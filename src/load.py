# src/load.py
"""
Módulo de carga a SQLite.
Guarda registros válidos y rechazados en tablas separadas.
"""

import os
import sqlite3
import pandas as pd

DB_PATH = "db/finanzas.db"


def cargar_a_sqlite(df_validos: pd.DataFrame, df_rechazados: pd.DataFrame) -> None:
    """Carga los DataFrames a SQLite en tablas separadas."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    print(f"\n💾 Cargando datos a {DB_PATH}...")

    with sqlite3.connect(DB_PATH) as conn:
        df_validos.to_sql("transacciones_limpias", conn, if_exists="replace", index=False)
        df_rechazados.to_sql("transacciones_rechazadas", conn, if_exists="replace", index=False)

    print(f"   ✅ Tabla 'transacciones_limpias': {len(df_validos)} registros")
    print(f"   ✅ Tabla 'transacciones_rechazadas': {len(df_rechazados)} registros")


def verificar_carga() -> None:
    """Muestra un resumen de lo que hay en la base."""
    if not os.path.exists(DB_PATH):
        print("⚠️  Base de datos no encontrada.")
        return

    with sqlite3.connect(DB_PATH) as conn:
        query = """
            SELECT 'limpias' AS tabla, COUNT(*) AS total FROM transacciones_limpias
            UNION ALL
            SELECT 'rechazadas', COUNT(*) FROM transacciones_rechazadas
        """
        print("\n📊 Estado de la base de datos:")
        print(pd.read_sql(query, conn).to_string(index=False))


if __name__ == "__main__":
    verificar_carga()