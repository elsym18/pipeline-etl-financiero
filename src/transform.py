# src/transform.py
"""
Módulo de transformación y limpieza de datos.
Separa registros válidos de rechazados según las reglas de calidad.
"""

import pandas as pd
from datetime import datetime
from src.quality import (
    MONEDAS_VALIDAS,
    MONTO_MINIMO,
    MONTO_MAXIMO,
    FECHA_MAXIMA,
    COLUMNAS_CRITICAS,
)


def marcar_invalidos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marca cada fila con las razones por las que falla QA.
    Agrega columna 'motivos_rechazo' (lista separada por ;).
    """
    df = df.copy()
    df["motivos_rechazo"] = ""

    # 1. Nulos en columnas críticas
    for col in COLUMNAS_CRITICAS:
        mask = df[col].isna()
        df.loc[mask, "motivos_rechazo"] += f"NULO:{col};"

    # 2. Duplicados por id_transaccion
    duplicados_mask = df.duplicated(subset=["id_transaccion"], keep=False)
    df.loc[duplicados_mask, "motivos_rechazo"] += "DUPLICADO:id_transaccion;"

    # 3. Moneda inválida
    mask_moneda = ~df["moneda"].isin(MONEDAS_VALIDAS)
    df.loc[mask_moneda, "motivos_rechazo"] += "MONEDA_INVALIDA;"

    # 4. Monto fuera de rango
    df_monto = pd.to_numeric(df["monto"], errors="coerce")
    mask_monto_min = df_monto < MONTO_MINIMO
    mask_monto_max = df_monto > MONTO_MAXIMO
    df.loc[mask_monto_min, "motivos_rechazo"] += "MONTO_MENOR_MINIMO;"
    df.loc[mask_monto_max, "motivos_rechazo"] += "MONTO_MAYOR_MAXIMO;"

    # 5. Fecha inválida o futura
    df_fechas = pd.to_datetime(df["fecha"], errors="coerce")
    mask_fecha_invalida = df_fechas.isna()
    mask_fecha_futura = df_fechas > FECHA_MAXIMA
    df.loc[mask_fecha_invalida, "motivos_rechazo"] += "FECHA_INVALIDA;"
    df.loc[mask_fecha_futura, "motivos_rechazo"] += "FECHA_FUTURA;"

    # Limpiar punto y coma final
    df["motivos_rechazo"] = df["motivos_rechazo"].str.rstrip(";")

    return df


def separar_validos_y_rechazados(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Separa el DataFrame en dos: registros válidos y rechazados.
    Los rechazados conservan la columna 'motivos_rechazo'.
    """
    df_marcado = marcar_invalidos(df)

    mask_validos = df_marcado["motivos_rechazo"] == ""
    df_validos = df_marcado[mask_validos].drop(columns=["motivos_rechazo"]).copy()
    df_rechazados = df_marcado[~mask_validos].copy()

    return df_validos, df_rechazados


def limpiar_validos(df_validos: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza tipos de datos en los registros válidos.
    """
    df = df_validos.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["monto"] = pd.to_numeric(df["monto"])
    df["sucursal"] = df["sucursal"].str.strip().str.upper()
    df["moneda"] = df["moneda"].str.strip().str.upper()
    df["estado"] = df["estado"].str.strip().str.upper()
    return df


def transformar(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Pipeline de transformación completo."""
    print("\n🔄 Transformando datos...")
    df_validos, df_rechazados = separar_validos_y_rechazados(df)
    df_validos = limpiar_validos(df_validos)

    print(f"   ✅ Registros válidos: {len(df_validos)}")
    print(f"   ❌ Registros rechazados: {len(df_rechazados)}")

    return df_validos, df_rechazados


if __name__ == "__main__":
    from src.extract import extraer_datos
    df = extraer_datos()
    validos, rechazados = transformar(df)
    print("\n--- VÁLIDOS (primeros 5) ---")
    print(validos.head())
    print("\n--- RECHAZADOS (primeros 5) ---")
    print(rechazados[["id_transaccion", "motivos_rechazo"]].head())