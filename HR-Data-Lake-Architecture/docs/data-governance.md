# 🛡️ Data Governance Framework - HR Data Lake

## 🎯 Objetivos del Governance

El framework de Data Governance establece políticas y procesos para garantizar:

1. **Calidad**: Datos precisos, completos y consistentes
2. **Seguridad**: Protección de información sensible (PII)
3. **Cumplimiento**: Adherencia a normativas (LGPD, GDPR equivalente)
4. **Trazabilidad**: Auditoría completa del linaje de datos
5. **Accesibilidad**: Datos disponibles para usuarios autorizados

---

## 📊 Dimensiones de Calidad de Datos

### 1. Completitud (Completeness)

**Definición**: % de registros con valores en campos obligatorios

**Métricas**:
```sql
-- % de registros con campos obligatorios completos
SELECT 
    (COUNT(*) FILTER (WHERE employee_id IS NOT NULL 
                        AND nombre_completo IS NOT NULL
                        AND departamento_cod IS NOT NULL)) * 100.0 / COUNT(*) 
    AS completeness_pct
FROM raw.employee_master;
```

**Umbrales**:
- ✅ **Aceptable**: ≥ 98%
- ⚠️ **Alerta**: 95-98%
- ❌ **Crítico**: < 95%

**Acción correctiva**: Rechazar lote de ingesta si < 95%

---

### 2. Unicidad (Uniqueness)

**Definición**: Cada entidad debe tener un identificador único sin duplicados

**Validación**:
```sql
-- Detectar DNIs duplicados
SELECT dni, COUNT(*) as duplicados
FROM raw.employee_master
GROUP BY dni
HAVING COUNT(*) > 1;
```

**Regla**: `employee_id` y `dni` deben ser **únicos** por registro

**Acción correctiva**: Cuarentena de registros duplicados → Revisión manual

---

### 3. Consistencia (Consistency)

**Definición**: Datos coherentes entre sí y alineados con reglas de negocio

**Validaciones**:

**Fechas lógicas**:
```sql
-- Validar que fecha_egreso > fecha_ingreso
SELECT employee_id, fecha_ingreso, fecha_egreso
FROM raw.employment_details
WHERE fecha_egreso IS NOT NULL 
  AND fecha_egreso < fecha_ingreso;
```

**Rangos salariales**:
```sql
-- Validar salario dentro de rango legal peruano
SELECT employee_id, salario_bruto
FROM raw.compensation
WHERE salario_bruto < 1025  -- Sueldo mínimo Perú 2026
   OR salario_bruto > 100000;  -- Outlier sospechoso
```

**Códigos maestros**:
```sql
-- Validar que departamento_cod exista en catálogo
SELECT e.employee_id, e.departamento_cod
FROM raw.employment_details e
LEFT JOIN master.departamentos_catalogo d ON e.departamento_cod = d.codigo
WHERE d.codigo IS NULL;
```

**Acción correctiva**: Alerta automática a Data Steward

---

### 4. Precisión (Accuracy)

**Definición**: Datos reflejan la realidad correctamente

**Validaciones**:

**Formato DNI peruano**:
```python
import re

def validar_dni(dni):
    """DNI debe ser 8 dígitos numéricos"""
    pattern = r'^\d{8}$'
    return bool(re.match(pattern, str(dni)))

# Aplicar en ETL
df_validated = df_raw[df_raw['dni'].apply(validar_dni)]
```

**Edad razonable**:
```sql
SELECT employee_id, fecha_nacimiento, 
       DATEDIFF(CURRENT_DATE, fecha_nacimiento)/365 AS edad
FROM raw.employee_master
WHERE edad < 18 OR edad > 70;
```

**Acción correctiva**: Rechazar registros inválidos → Log de errores

---

### 5. Actualidad (Timeliness)

**Definición**: Datos disponibles cuando se necesitan

**SLA del Pipeline**:
| Fuente | Frecuencia | Latencia Máxima | Horario |
|--------|-----------|-----------------|---------|
| Nóminas (SAP) | Mensual | 24 horas | Día 1 del mes |
| Asistencias (ADP) | Diaria | 6 horas | 6 AM |
| Evaluaciones | Semestral | 48 horas | Fin de período |

**Monitoreo**:
```python
# Airflow DAG con alertas
if (datetime.now() - last_update_time).hours > SLA_HOURS:
    send_alert_to_slack(f"⚠️ Data delayed: {source_name}")
```

---

## 🔐 Seguridad y Privacidad

### Clasificación de Datos

| Nivel | Descripción | Ejemplos | Protección |
|-------|-------------|----------|-----------|
| **Público** | Sin riesgo si se expone | Nombre departamento | Ninguna |
| **Interno** | Solo empleados | Métricas agregadas | Autenticación |
| **Confidencial** | Acceso restringido | Salario individual | Roles específicos |
| **Crítico (PII)** | Datos personales | DNI, dirección | Encriptación |

### Encriptación de PII

**Campos sensibles**:
- `dni`
- `telefono_movil`
- `direccion_domicilio`
- `cuenta_bancaria`

**Implementación**:
```python
from cryptography.fernet import Fernet

# Generar clave (almacenar en Azure Key Vault)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encriptar al escribir en Raw Layer
df_raw['dni_encrypted'] = df_raw['dni'].apply(
    lambda x: cipher.encrypt(str(x).encode())
)

# Guardar solo versión encriptada
df_raw.drop(columns=['dni']).write.parquet('/raw/employee_master/')
```

**Desencriptación**: Solo usuarios con rol `HR_ADMIN`

---

### Control de Acceso (RBAC)

**Roles definidos**:

| Rol | Staging | Raw | Master | Descripción |
|-----|---------|-----|--------|-------------|
| `DATA_ENGINEER` | RW | RW | RW | Control total del pipeline |
| `HR_ANALYST` | - | R | R | Análisis de datos anonimizados |
| `HR_ADMIN` | - | R (incl. PII) | R (incl. PII) | Acceso a datos sensibles |
| `BI_DEVELOPER` | - | - | R | Solo capa Master para dashboards |
| `MANAGER` | - | - | R (filtered) | Solo su departamento |

**Implementación (Azure)**:
```json
{
  "role": "HR_ANALYST",
  "permissions": [
    {
      "path": "/raw/*",
      "actions": ["read"],
      "conditions": {
        "exclude_columns": ["dni_encrypted", "cuenta_bancaria"]
      }
    }
  ]
}
```

---

## 📋 Linaje de Datos (Data Lineage)

### Trazabilidad End-to-End

**Objetivo**: Responder "¿De dónde viene este dato?"

**Herramienta**: Apache Atlas / AWS Glue Data Catalog

**Ejemplo de linaje**:
```
Campo: turnover_risk_score (Master Layer)

Origen:
└─ master.employee_metrics.turnover_risk_score
   └─ Calculado por: etl_raw_to_master.py (línea 45)
      └─ Inputs:
         ├─ raw.compensation.salario_bruto
         │  └─ staging/nominas/2026-02-04/export_sap.csv (columna: SALARIO_BRUTO)
         │     └─ SAP SuccessFactors (API export 2026-02-04 10:35 AM)
         │
         ├─ raw.engagement.satisfaction_score
         │  └─ staging/encuestas/2025-12-15/clima_laboral.json (campo: satisfaction)
         │     └─ Sistema encuestas internas (aplicado 2025-12-15)
         │
         └─ raw.attendance.faltas_mes
            └─ staging/asistencias/2026-02-04/marcaciones_adp.csv (agregado)
               └─ ADP Workforce Now (daily sync)

Última modificación: 2026-02-04 12:15 PM (job_id: etl_20260204_001)
```

---

### Versionado de Transformaciones

**Control de versiones del código ETL**:
```bash
# Git commit obligatorio antes de ejecutar
git log --oneline etl_raw_to_master.py

a1b2c3d (2026-02-04) Agregado cálculo de turnover_risk_score
d4e5f6g (2026-01-15) Fix: filtro de empleados activos
```

**Metadatos en Master Layer**:
```python
# Agregar columnas de auditoría
df_master['_created_at'] = current_timestamp()
df_master['_etl_version'] = git_commit_hash
df_master['_source_file'] = input_file_name()
```

---

## 📐 Estándares de Datos

### Convenciones de Nomenclatura

**Tablas**:
- Singular, snake_case: `employee_master`, `compensation`
- Prefijo por capa: `staging_`, `raw_`, `master_`

**Columnas**:
- snake_case: `employee_id`, `fecha_ingreso`
- Sufijos:
  - `_id`: Identificadores
  - `_cod`: Códigos categóricos
  - `_pct`: Porcentajes
  - `_score`: Scores calculados

**Fechas**:
- Formato: `YYYY-MM-DD` (ISO 8601)
- Nombres: `fecha_[evento]` (ej: `fecha_contratacion`)

**Moneda**:
- Siempre incluir columna `moneda` (PEN, USD)
- Decimales: 2 dígitos (ej: `5500.00`)

---

## 🔍 Monitoreo y Alertas

### Dashboard de Calidad de Datos

**Métricas en tiempo real** (Power BI):

| Métrica | Umbral | Valor Actual | Estado |
|---------|--------|--------------|--------|
| Completeness | ≥98% | 99.2% | ✅ |
| Registros duplicados | 0 | 0 | ✅ |
| Latencia pipeline (hrs) | ≤6 | 4.5 | ✅ |
| Errores ETL (última corrida) | 0 | 3 | ⚠️ |

### Alertas Automáticas

**Configuración (Airflow)**:
```python
def data_quality_check(**context):
    df = spark.read.parquet('/raw/employee_master/')
    
    # Check 1: Completeness
    completeness = df.filter(df.employee_id.isNotNull()).count() / df.count()
    if completeness < 0.98:
        raise AirflowException(f"❌ Completeness {completeness:.2%} < 98%")
    
    # Check 2: Duplicates
    duplicates = df.groupBy('employee_id').count().filter('count > 1').count()
    if duplicates > 0:
        raise AirflowException(f"❌ {duplicates} duplicate employee_ids found")
    
    # Check 3: Invalid salaries
    invalid_salaries = df.filter((df.salario_bruto < 1025) | (df.salario_bruto > 100000)).count()
    if invalid_salaries > 0:
        send_slack_alert(f"⚠️ {invalid_salaries} salaries out of range")

# DAG task
quality_check = PythonOperator(
    task_id='data_quality_check',
    python_callable=data_quality_check,
    trigger_rule='all_success'
)
```

**Canales de notificación**:
- 🔴 Crítico → Email a Data Engineer + Jira ticket
- 🟡 Alerta → Slack #data-quality
- 🟢 Info → Log interno

---

## 👥 Roles y Responsabilidades

| Rol | Responsable | Responsabilidades |
|-----|------------|------------------|
| **Data Owner** | Gerente de RRHH | Aprueba políticas de acceso y uso de datos |
| **Data Steward** | Analista Senior RRHH | Valida calidad, resuelve inconsistencias |
| **Data Engineer** | Equipo TI | Implementa pipelines, mantiene infraestructura |
| **Data Custodian** | Administrador de Sistemas | Gestiona backups, seguridad física |
| **Data Consumer** | Analistas/Gerentes | Consume datos para análisis y decisiones |

---

## 📅 Ciclo de Revisión

**Periodicidad de auditorías**:

| Actividad | Frecuencia | Responsable |
|-----------|-----------|-------------|
| Revisión de calidad de datos | Diaria | Data Engineer |
| Actualización de diccionario | Trimestral | Data Steward |
| Auditoría de accesos | Mensual | InfoSec |
| Certificación de cumplimiento | Anual | Legal + RRHH |

---

## 📄 Cumplimiento Normativo

### Legislación Aplicable (Perú)

**Ley de Protección de Datos Personales (Ley N° 29733)**:
- ✅ Consentimiento para uso de datos personales
- ✅ Derecho al olvido (eliminar datos de empleados que lo soliciten)
- ✅ Retención máxima: 5 años post-egreso

**Implementación**:
```python
# Script de anonimización para ex-empleados (> 5 años)
def anonymize_old_records():
    cutoff_date = datetime.now() - timedelta(days=5*365)
    
    df = spark.read.parquet('/raw/employee_master/')
    df_anonymized = df.filter(df.fecha_egreso < cutoff_date) \
        .withColumn('nombre_completo', lit('ANONIMIZADO')) \
        .withColumn('dni', lit('00000000')) \
        .withColumn('email_corporativo', lit('redacted@empresa.com'))
    
    df_anonymized.write.mode('overwrite').parquet('/raw/employee_master_anon/')
```

---

## 🔗 Referencias

- [ISO 8000: Data Quality](https://www.iso.org/standard/50798.html)
- [DAMA-DMBOK: Data Governance](https://www.dama.org/cpages/body-of-knowledge)
- [Ley N° 29733 (Protección de Datos Personales - Perú)](https://www.gob.pe/institucion/minjus/normas-legales/241865-29733)

---

**Versión**: 1.0  
**Autor**: James Lalupu  
**Última actualización**: 2026-02-04
