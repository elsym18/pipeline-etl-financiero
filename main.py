# main.py
"""
Pipeline ETL Financiero - Orquestador principal.
Fases: extract → quality → transform → load → report
"""

from src.extract import extraer_datos
from src.quality import ejecutar_validaciones, mostrar_reporte
from src.transform import transformar
from src.load import cargar_a_sqlite, verificar_carga
from src.report import generar_reportes


def run_pipeline():
    print("=" * 60)
    print("🚀 PIPELINE ETL FINANCIERO - INICIANDO")
    print("=" * 60)

    # 1. EXTRACT
    print("\n[1/5] EXTRACCIÓN DE DATOS")
    df = extraer_datos(forzar_regeneracion=True)

    # 2. QUALITY
    print("\n[2/5] VALIDACIÓN DE CALIDAD")
    reporte = ejecutar_validaciones(df)
    mostrar_reporte(reporte)

    # 3. TRANSFORM
    print("\n[3/5] TRANSFORMACIÓN")
    df_validos, df_rechazados = transformar(df)

    # 4. LOAD
    print("\n[4/5] CARGA A SQLITE")
    cargar_a_sqlite(df_validos, df_rechazados)

    # 5. REPORT
    print("\n[5/5] GENERACIÓN DE REPORTES")
    generar_reportes(reporte)

    # Verificación final
    verificar_carga()

    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETADO")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()