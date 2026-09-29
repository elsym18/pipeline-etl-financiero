# src/quality.py
"""
Módulo de calidad de datos.
Aplica reglas de validación tipo Hammurabi / Data Quality.
"""

import pandas as pd
from datetime import datetime
from tabulate import tabulate


MONEDAS_VALIDAS = {"ARS", "USD", "EUR"}
MONTO_MINIMO = 0.01
MONTO_MAXIMO = 1_000_000
FECHA_MAXIMA = datetime(2025, 12, 31)
COLUMNAS_CRITICAS = ["id_transaccion", "fecha", "monto", "cliente_id"]


def validar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    resultados = []
    for col in COLUMNAS_CRITICAS:
        nulos = df[col].isna().sum()
        resultados.append({
            "regla": f"NO_NULOS::{col}",
            "descripcion": f"La columna '{col}' no debe tener nulos",
            "registros_afectados": int(nulos),
            "estado": "OK" if nulos == 0 else "FALLA",
        })
    return pd.DataFrame(resultados)


def validar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    duplicados = df.duplicated(subset=["id_transaccion"], keep=False).sum()
    return pd.DataFrame([{
        "regla": "UNICIDAD::id_transaccion",
        "descripcion": "El id_transaccion debe ser único",
        "registros_afectados": int(duplicados),
        "estado": "OK" if duplicados == 0 else "FALLA",
    }])


def validar_moneda(df: pd.DataFrame) -> pd.DataFrame:
    invalidas = (~df["moneda"].isin(MONEDAS_VALIDAS)).sum()
    return pd.DataFrame([{
        "regla": "DOMINIO::moneda",
        "descripcion": f"Moneda debe ser una de {MONEDAS_VALIDAS}",
        "registros_afectados": int(invalidas),
        "estado": "OK" if invalidas == 0 else "FALLA",
    }])


def validar_montos(df: pd.DataFrame) -> pd.DataFrame:
    negativos = (df["monto"] < MONTO_MINIMO).sum()
    excedidos = (df["monto"] > MONTO_MAXIMO).sum()
    return pd.DataFrame([
        {
            "regla": "RANGO::monto_positivo",
            "descripcion": f"Monto debe ser >= {MONTO_MINIMO}",
            "registros_afectados": int(negativos),
            "estado": "OK" if negativos == 0 else "FALLA",
        },
        {
            "regla": "RANGO::monto_maximo",
            "descripcion": f"Monto no debe exceder {MONTO_MAXIMO}",
            "registros_afectados": int(excedidos),
            "estado": "OK" if excedidos == 0 else "FALLA",
        },
    ])


def validar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    df_fechas = pd.to_datetime(df["fecha"], errors="coerce")
    invalidas = (df_fechas.isna()).sum()
    futuras = (df_fechas > FECHA_MAXIMA).sum()
    return pd.DataFrame([
        {
            "regla": "FORMATO::fecha",
            "descripcion": "La fecha debe tener formato válido YYYY-MM-DD",
            "registros_afectados": int(invalidas),
            "estado": "OK" if invalidas == 0 else "FALLA",
        },
        {
            "regla": "RANGO::fecha_no_futura",
            "descripcion": f"La fecha no debe superar {FECHA_MAXIMA.date()}",
            "registros_afectados": int(futuras),
            "estado": "OK" if futuras == 0 else "FALLA",
        },
    ])


def ejecutar_validaciones(df: pd.DataFrame) -> pd.DataFrame:
    print("\n🔍 Ejecutando validaciones de calidad de datos...\n")
    reportes = [
        validar_nulos(df),
        validar_duplicados(df),
        validar_moneda(df),
        validar_montos(df),
        validar_fechas(df),
    ]
    return pd.concat(reportes, ignore_index=True)


def mostrar_reporte(reporte: pd.DataFrame) -> None:
    print(tabulate(reporte, headers="keys", tablefmt="grid", showindex=False))
    total = len(reporte)
    fallas = (reporte["estado"] == "FALLA").sum()
    print(f"\n📊 Resumen: {total - fallas}/{total} reglas OK | {fallas} con fallas")


if __name__ == "__main__":
    from src.extract import extraer_datos
    df = extraer_datos()
    reporte = ejecutar_validaciones(df)
    mostrar_reporte(reporte)