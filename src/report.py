# src/report.py
"""
Módulo de generación de reportes.
Guarda el reporte de calidad en CSV y HTML.
"""

import os
from datetime import datetime
import pandas as pd

REPORTS_DIR = "data/quality_reports"


def _estilos_html() -> str:
    return """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }
        h1 { color: #38bdf8; }
        table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
        th, td { border: 1px solid #334155; padding: 0.6rem; text-align: left; }
        th { background: #1e293b; color: #38bdf8; }
        tr:nth-child(even) { background: #1e293b; }
        .ok { color: #22c55e; font-weight: bold; }
        .falla { color: #ef4444; font-weight: bold; }
        .resumen { margin-top: 1.5rem; padding: 1rem; background: #1e293b; border-left: 4px solid #38bdf8; }
    </style>
    """


def guardar_reporte_csv(reporte: pd.DataFrame) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{REPORTS_DIR}/reporte_calidad_{timestamp}.csv"
    reporte.to_csv(path, index=False)
    print(f"   📄 Reporte CSV: {path}")
    return path


def guardar_reporte_html(reporte: pd.DataFrame) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{REPORTS_DIR}/reporte_calidad_{timestamp}.html"

    total = len(reporte)
    fallas = (reporte["estado"] == "FALLA").sum()
    ok = total - fallas

    filas = ""
    for _, row in reporte.iterrows():
        clase = "ok" if row["estado"] == "OK" else "falla"
        filas += f"""
        <tr>
            <td>{row['regla']}</td>
            <td>{row['descripcion']}</td>
            <td>{row['registros_afectados']}</td>
            <td class="{clase}">{row['estado']}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Calidad de Datos</title>
        {_estilos_html()}
    </head>
    <body>
        <h1>📊 Reporte de Calidad de Datos</h1>
        <p>Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <table>
            <thead>
                <tr>
                    <th>Regla</th>
                    <th>Descripción</th>
                    <th>Registros afectados</th>
                    <th>Estado</th>
                </tr>
            </thead>
            <tbody>{filas}</tbody>
        </table>
        <div class="resumen">
            <strong>Resumen:</strong> {ok}/{total} reglas OK | {fallas} con fallas
        </div>
    </body>
    </html>
    """

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"   🌐 Reporte HTML: {path}")
    return path


def generar_reportes(reporte: pd.DataFrame) -> None:
    print("\n📝 Generando reportes...")
    guardar_reporte_csv(reporte)
    guardar_reporte_html(reporte)