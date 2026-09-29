# tests/test_quality.py
"""
Tests automatizados del pipeline ETL Financiero.
Verifica reglas de calidad, transformación y carga.
"""

import pandas as pd
import pytest

from src.extract import generar_dataset_simulado
from src.quality import (
    MONEDAS_VALIDAS,
    MONTO_MINIMO,
    FECHA_MAXIMA,
    COLUMNAS_CRITICAS,
    validar_nulos,
    validar_duplicados,
    validar_moneda,
    validar_montos,
    validar_fechas,
)
from src.transform import transformar


# =========================================================
# FIXTURES (datos de prueba reutilizables)
# =========================================================

@pytest.fixture
def df_crudo():
    """Dataset simulado con errores intencionales."""
    return generar_dataset_simulado(n_registros=200, seed=42)


@pytest.fixture
def df_transformado(df_crudo):
    """Dataset ya transformado (válidos, rechazados)."""
    return transformar(df_crudo)


# =========================================================
# TESTS DEL EXTRACT
# =========================================================

def test_dataset_tiene_columnas_esperadas(df_crudo):
    """El dataset debe tener todas las columnas esperadas."""
    columnas_esperadas = {
        "id_transaccion", "fecha", "sucursal", "tipo_operacion",
        "moneda", "monto", "cliente_id", "estado"
    }
    assert columnas_esperadas.issubset(set(df_crudo.columns))


def test_dataset_no_esta_vacio(df_crudo):
    """El dataset debe tener registros."""
    assert len(df_crudo) > 0


# =========================================================
# TESTS DE REGLAS DE CALIDAD (detectan errores correctamente)
# =========================================================

def test_validar_nulos_detecta_nulos(df_crudo):
    """La validación de nulos debe detectar nulos en columnas críticas."""
    reporte = validar_nulos(df_crudo)
    # Debe haber al menos una regla con FALLA (monto o cliente_id tienen nulos)
    assert (reporte["estado"] == "FALLA").any()


def test_validar_duplicados_detecta(df_crudo):
    """La validación de duplicados debe detectar duplicados."""
    reporte = validar_duplicados(df_crudo)
    assert reporte.iloc[0]["estado"] == "FALLA"
    assert reporte.iloc[0]["registros_afectados"] > 0


def test_validar_moneda_detecta_invalidas(df_crudo):
    """La validación de moneda debe detectar valores fuera del catálogo."""
    reporte = validar_moneda(df_crudo)
    assert reporte.iloc[0]["estado"] == "FALLA"


def test_validar_montos_detecta_negativos(df_crudo):
    """La validación de montos debe detectar montos negativos."""
    reporte = validar_montos(df_crudo)
    regla_positivo = reporte[reporte["regla"] == "RANGO::monto_positivo"]
    assert regla_positivo.iloc[0]["estado"] == "FALLA"


def test_validar_fechas_detecta_futuras(df_crudo):
    """La validación de fechas debe detectar fechas futuras."""
    reporte = validar_fechas(df_crudo)
    regla_futura = reporte[reporte["regla"] == "RANGO::fecha_no_futura"]
    assert regla_futura.iloc[0]["estado"] == "FALLA"


# =========================================================
# TESTS DE TRANSFORMACIÓN (datos limpios están OK)
# =========================================================

def test_transformar_separa_validos_y_rechazados(df_crudo, df_transformado):
    """La transformación debe separar en válidos y rechazados sin perder registros."""
    df_validos, df_rechazados = df_transformado
    total_original = len(df_crudo)
    total_transformado = len(df_validos) + len(df_rechazados)
    assert total_transformado == total_original, (
        f"Se perdieron registros: original={total_original}, "
        f"transformado={total_transformado}"
    )


def test_validos_no_tienen_nulos(df_transformado):
    """Después de transformar, los válidos no deben tener nulos en columnas críticas."""
    df_validos, _ = df_transformado
    for col in COLUMNAS_CRITICAS:
        assert df_validos[col].isna().sum() == 0, f"Hay nulos en {col}"


def test_validos_no_tienen_duplicados(df_transformado):
    """Después de transformar, los válidos no deben tener duplicados."""
    df_validos, _ = df_transformado
    assert df_validos["id_transaccion"].duplicated().sum() == 0


def test_validos_tienen_montos_positivos(df_transformado):
    """Después de transformar, todos los montos deben ser positivos."""
    df_validos, _ = df_transformado
    assert (df_validos["monto"] >= MONTO_MINIMO).all()


def test_validos_tienen_monedas_validas(df_transformado):
    """Después de transformar, todas las monedas deben ser válidas."""
    df_validos, _ = df_transformado
    assert df_validos["moneda"].isin(MONEDAS_VALIDAS).all()


def test_validos_tienen_fechas_no_futuras(df_transformado):
    """Después de transformar, las fechas no deben superar el límite."""
    df_validos, _ = df_transformado
    fechas = pd.to_datetime(df_validos["fecha"])
    assert (fechas <= FECHA_MAXIMA).all()


def test_rechazados_tienen_motivo(df_transformado):
    """Todos los registros rechazados deben tener un motivo."""
    _, df_rechazados = df_transformado
    assert (df_rechazados["motivos_rechazo"].str.len() > 0).all()


def test_rechazados_no_estan_vacios(df_transformado):
    """Debe haber registros rechazados (porque inyectamos errores)."""
    _, df_rechazados = df_transformado
    assert len(df_rechazados) > 0