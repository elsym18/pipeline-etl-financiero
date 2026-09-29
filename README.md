# 💰 Pipeline ETL Financiero con Calidad de Datos

Pipeline ETL (Extract → Transform → Load) para procesar transacciones financieras, aplicar reglas de calidad de datos estilo Hammurabi, separar registros válidos de rechazados y generar reportes automáticos en CSV y HTML.

Inspirado en experiencia real en banca, finanzas públicas y QA de datos.

---

##  Características

- ✅ **Extract:** generación/carga de transacciones financieras simuladas
- ✅ **Quality:** 10 reglas de validación (nulos, duplicados, dominios, rangos, fechas)
- ✅ **Transform:** separación de registros válidos y rechazados con motivo
- ✅ **Load:** carga a SQLite en tablas separadas
- ✅ **Report:** reportes automáticos en CSV y HTML con diseño profesional
- ✅ **Tests:** 15 tests automatizados con Pytest
- ✅ **Docker:** entorno reproducible con Docker Compose

---

## 🏗️ Arquitectura

```
EXTRACT  ->  QUALITY  ->  TRANSFORM  ->  LOAD  ->  REPORT
   |           |            |            |         |
CSV crudo   10 reglas    Validos vs   SQLite   CSV + HTML
1020 rows   de calidad   Rechazados   2 tablas
```

---

##  Tecnologías

| Categoría | Tecnología |
|-----------|-----------|
| Lenguaje | Python 3.11 |
| Datos | Pandas, NumPy |
| Base de datos | SQLite |
| Testing | Pytest |
| Contenedores | Docker, Docker Compose |
| Reportes | HTML5, CSS3, CSV |

---

##  Estructura del proyecto

```
pipeline-etl-financiero/
├── data/
│   ├── raw/
│   ├── processed/
│   └── quality_reports/
├── db/
│   └── finanzas.db
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── quality.py
│   ├── transform.py
│   ├── load.py
│   └── report.py
├── tests/
│   ├── __init__.py
│   └── test_quality.py
├── Dockerfile
├── docker-compose.yml
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

##  Cómo ejecutarlo

### Requisitos

- Docker Desktop instalado y corriendo
- Git (opcional, para clonar)

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/pipeline-etl-financiero.git
cd pipeline-etl-financiero
```

### 2. Construir la imagen Docker

```bash
docker compose build
```

### 3. Ejecutar el pipeline

```bash
docker compose up
```

Los datos, la base y los reportes se generarán automáticamente en `data/` y `db/`.

### 4. Ejecutar los tests

```bash
docker compose run --rm etl-financiero pytest
```

Resultado esperado: **15 tests passed** 

---

##  Reglas de calidad implementadas

| # | Regla | Descripción |
|---|-------|-------------|
| 1 | NO_NULOS::id_transaccion | El ID de transacción no debe ser nulo |
| 2 | NO_NULOS::fecha | La fecha no debe ser nula |
| 3 | NO_NULOS::monto | El monto no debe ser nulo |
| 4 | NO_NULOS::cliente_id | El ID de cliente no debe ser nulo |
| 5 | UNICIDAD::id_transaccion | El ID de transacción debe ser único |
| 6 | DOMINIO::moneda | Moneda debe ser ARS, USD o EUR |
| 7 | RANGO::monto_positivo | Monto debe ser mayor o igual a 0.01 |
| 8 | RANGO::monto_maximo | Monto no debe exceder 1.000.000 |
| 9 | FORMATO::fecha | Fecha debe tener formato YYYY-MM-DD |
| 10 | RANGO::fecha_no_futura | Fecha no debe superar 2025-12-31 |

---

##  Ejemplo de salida

```
[1/5] EXTRACCION DE DATOS
Generando dataset simulado...
Dataset guardado (1020 registros)

[2/5] VALIDACION DE CALIDAD
Resumen: 4/10 reglas OK | 6 con fallas

[3/5] TRANSFORMACION
   Registros validos: 903
   Registros rechazados: 117

[4/5] CARGA A SQLITE
   Tabla 'transacciones_limpias': 903 registros
   Tabla 'transacciones_rechazadas': 117 registros

[5/5] GENERACION DE REPORTES
   Reporte CSV generado
   Reporte HTML generado

PIPELINE COMPLETADO
```

---

##  Tests

El proyecto incluye 15 tests automatizados:

- **Extract (2):** columnas esperadas, dataset no vacío
- **Quality (5):** detección de nulos, duplicados, monedas inválidas, montos negativos y fechas futuras
- **Transform (5):** separación correcta, sin nulos, sin duplicados, montos positivos, monedas válidas
- **Rechazados (2):** motivo presente, registros rechazados no vacíos

```bash
docker compose run --rm etl-financiero pytest
```

Resultado esperado:

```
15 passed in 0.69s
```

---

##  Motivación

Este proyecto fue creado como parte de un portafolio profesional para demostrar habilidades en:

- **Ingeniería de Datos:** ETL, calidad, pipelines
- **QA / Data Quality:** reglas de validación automatizadas
- **Finanzas:** transacciones, montos, compliance
- **DevOps:** Docker, entornos reproducibles

---

##  Roadmap

- [x] Pipeline ETL básico
- [x] Reglas de calidad de datos
- [x] Tests automatizados con Pytest
- [x] Dockerización
- [ ] Dashboard interactivo con Streamlit
- [ ] Scheduler tipo Control-M
- [ ] Integración con AWS S3
- [ ] Conexión a Power BI

---

##  Autora

Elsy Molina

- LinkedIn: Elsy Molina (https://www.linkedin.com/in/elsymolina/)
- GitHub: @elsym18 (https://github.com/elsym18)

---

##  Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
