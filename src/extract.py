# src/extract.py
"""
Módulo de extracción de datos financieros.
Simula la extracción de un sistema bancario generando un CSV con errores intencionales.
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

RAW_PATH = "data/raw/transacciones_financieras.csv"


def generar_dataset_simulado(n_registros: int = 1000, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)

    sucursales = ["GCBA-001", "GCBA-002", "BBVA-100", "BBVA-200", "ARAMARK-01"]
    tipos = ["DEBITO", "CREDITO", "TRANSFERENCIA", "PAGO"]
    monedas = ["ARS", "USD", "EUR"]

    registros = []
    fecha_base = datetime(2024, 1, 1)

    for i in range(1, n_registros + 1):
        registros.append({
            "id_transaccion": f"TX-{i:06d}",
            "fecha": (fecha_base + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "sucursal": random.choice(sucursales),
            "tipo_operacion": random.choice(tipos),
            "moneda": random.choice(monedas),
            "monto": round(random.uniform(100, 50000), 2),
            "cliente_id": f"CLI-{random.randint(1000, 9999)}",
            "estado": random.choice(["APROBADA", "RECHAZADA", "PENDIENTE"]),
        })

    df = pd.DataFrame(registros)

    df.loc[df.sample(frac=0.02, random_state=seed).index, "monto"] = -1500.00
    df.loc[df.sample(frac=0.03, random_state=seed + 1).index, "cliente_id"] = None
    df.loc[df.sample(frac=0.015, random_state=seed + 2).index, "monto"] = None
    df = pd.concat([df, df.sample(20, random_state=seed + 3)], ignore_index=True)
    df.loc[df.sample(10, random_state=seed + 4).index, "moneda"] = "XXX"
    df.loc[df.sample(5, random_state=seed + 5).index, "fecha"] = "2030-12-31"

    return df


def extraer_datos(forzar_regeneracion: bool = False) -> pd.DataFrame:
    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

    if not os.path.exists(RAW_PATH) or forzar_regeneracion:
        print("📥 Generando dataset simulado...")
        df = generar_dataset_simulado()
        df.to_csv(RAW_PATH, index=False)
        print(f"✅ Dataset guardado en {RAW_PATH} ({len(df)} registros)")
    else:
        print(f"📂 Cargando dataset existente desde {RAW_PATH}")
        df = pd.read_csv(RAW_PATH)

    return df


if __name__ == "__main__":
    df = extraer_datos(forzar_regeneracion=True)
    print(df.head())
    print(f"\nTotal registros: {len(df)}")
    print(f"Columnas: {list(df.columns)}")