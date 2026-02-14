# 📖 Diccionario de Datos HR - Data Lake

## 🎯 Propósito
Este diccionario centraliza la definición de todos los campos utilizados en el Data Lake de RR.HH., asegurando consistencia y comprensión compartida entre equipos.

---

## 📊 Tablas Core

### 1. Employee Master (Maestro de Empleados)

| Campo | Tipo | Longitud | Nulos | Descripción | Capa | Ejemplo |
|-------|------|----------|-------|-------------|------|---------|
| `employee_id` | INTEGER | - | NO | Identificador único del empleado (autoincrementable) | Todas | 10234 |
| `dni` | VARCHAR | 8 | NO | Documento Nacional de Identidad (Perú) | Staging, Raw | "12345678" |
| `nombre_completo` | VARCHAR | 150 | NO | Nombre y apellidos completos | Staging, Raw | "Juan Carlos Pérez García" |
| `fecha_nacimiento` | DATE | - | NO | Fecha de nacimiento | Raw+ | 1990-05-15 |
| `edad` | INTEGER | - | SÍ | Edad calculada (años cumplidos) | Master | 35 |
| `genero` | CHAR | 1 | NO | M=Masculino, F=Femenino, O=Otro | Raw+ | "M" |
| `estado_civil` | VARCHAR | 20 | SÍ | Soltero, Casado, Divorciado, Viudo | Raw+ | "Casado" |
| `num_hijos` | INTEGER | - | SÍ | Número de hijos declarados | Raw+ | 2 |
| `email_corporativo` | VARCHAR | 100 | NO | Correo electrónico de la empresa | Raw+ | "jperez@empresa.com" |
| `telefono_movil` | VARCHAR | 15 | SÍ | Número de contacto | Raw+ | "+51987654321" |

---

### 2. Employment Details (Detalles Laborales)

| Campo | Tipo | Longitud | Nulos | Descripción | Capa | Ejemplo |
|-------|------|----------|-------|-------------|------|---------|
| `employee_id` | INTEGER | - | NO | FK a Employee Master | Todas | 10234 |
| `fecha_ingreso` | DATE | - | NO | Fecha de contratación | Todas | 2022-03-01 |
| `fecha_egreso` | DATE | - | SÍ | Fecha de salida (NULL si activo) | Raw+ | NULL |
| `estado_laboral` | VARCHAR | 20 | NO | Activo, Inactivo, Suspendido | Raw+ | "Activo" |
| `tipo_contrato` | VARCHAR | 30 | NO | Plazo Fijo, Indeterminado, Prácticas | Raw+ | "Indeterminado" |
| `departamento_cod` | CHAR | 3 | NO | Código del departamento | Todas | "VEN" |
| `departamento_nombre` | VARCHAR | 50 | NO | Nombre del departamento | Raw+ | "Ventas" |
| `puesto` | VARCHAR | 100 | NO | Título del puesto | Raw+ | "Analista de Ventas" |
| `nivel_jerarquico` | INTEGER | - | NO | 1=Ejecutivo, 2=Gerente, 3=Coordinador, 4=Analista, 5=Asistente | Raw+ | 4 |
| `supervisor_id` | INTEGER | - | SÍ | employee_id del jefe directo | Raw+ | 10189 |
| `ubicacion` | VARCHAR | 50 | NO | Ciudad/Oficina | Raw+ | "Lima - San Isidro" |
| `modalidad_trabajo` | VARCHAR | 20 | NO | Presencial, Remoto, Híbrido | Raw+ | "Híbrido" |
| `antiguedad_dias` | INTEGER | - | SÍ | Días desde fecha_ingreso | Master | 1095 |
| `antiguedad_años` | DECIMAL | 4,2 | SÍ | Años de antigüedad | Master | 3.00 |

---

### 3. Compensation (Compensaciones)

| Campo | Tipo | Longitud | Nulos | Descripción | Capa | Ejemplo |
|-------|------|----------|-------|-------------|------|---------|
| `employee_id` | INTEGER | - | NO | FK a Employee Master | Todas | 10234 |
| `periodo` | DATE | - | NO | Mes de la nómina (YYYY-MM-01) | Todas | 2026-02-01 |
| `salario_base` | DECIMAL | 10,2 | NO | Sueldo base mensual (antes de bonos) | Raw+ | 5000.00 |
| `bono_productividad` | DECIMAL | 10,2 | SÍ | Bono variable por cumplimiento de metas | Raw+ | 500.00 |
| `horas_extra` | DECIMAL | 10,2 | SÍ | Pago por horas adicionales | Raw+ | 0.00 |
| `salario_bruto` | DECIMAL | 10,2 | NO | Total antes de descuentos | Raw+ | 5500.00 |
| `descuento_onp_afp` | DECIMAL | 10,2 | NO | Pensión (13% aprox) | Raw+ | 715.00 |
| `descuento_essalud` | DECIMAL | 10,2 | NO | Seguro de salud (9% empleador) | Raw+ | 495.00 |
| `impuesto_renta` | DECIMAL | 10,2 | SÍ | Retención de 5ta categoría | Raw+ | 200.00 |
| `salario_neto` | DECIMAL | 10,2 | NO | Total a depositar | Raw+ | 4585.00 |
| `moneda` | CHAR | 3 | NO | PEN=Soles, USD=Dólares | Raw+ | "PEN" |
| `forma_pago` | VARCHAR | 20 | NO | Depósito Bancario, Efectivo | Raw+ | "Depósito Bancario" |

---

### 4. Attendance (Asistencia y Tiempo)

| Campo | Tipo | Longitud | Nulos | Descripción | Capa | Ejemplo |
|-------|------|----------|-------|-------------|------|---------|
| `employee_id` | INTEGER | - | NO | FK a Employee Master | Todas | 10234 |
| `fecha` | DATE | - | NO | Día de asistencia | Todas | 2026-02-04 |
| `tipo_dia` | VARCHAR | 20 | NO | Laboral, Descanso, Feriado | Raw+ | "Laboral" |
| `hora_entrada` | TIME | - | SÍ | Hora de ingreso registrada | Raw+ | 08:45:00 |
| `hora_salida` | TIME | - | SÍ | Hora de salida registrada | Raw+ | 18:30:00 |
| `horas_trabajadas` | DECIMAL | 4,2 | SÍ | Horas efectivas | Master | 9.75 |
| `tardanza_minutos` | INTEGER | - | SÍ | Minutos de retraso vs horario oficial | Master | 45 |
| `estado_asistencia` | VARCHAR | 20 | NO | Presente, Falta, Licencia, Vacaciones | Raw+ | "Presente" |
| `tipo_ausencia` | VARCHAR | 30 | SÍ | Médica, Personal, Sin goce | Raw+ | NULL |
| `horas_extra_dia` | DECIMAL | 4,2 | SÍ | Horas adicionales trabajadas | Raw+ | 1.75 |

---

### 5. Performance (Evaluación de Desempeño)

| Campo | Tipo | Longitud | Nulos | Descripción | Capa | Ejemplo |
|-------|------|----------|-------|-------------|------|---------|
| `employee_id` | INTEGER | - | NO | FK a Employee Master | Todas | 10234 |
| `periodo_evaluacion` | VARCHAR | 7 | NO | Año-Semestre (YYYY-S1/S2) | Raw+ | "2025-S2" |
| `fecha_evaluacion` | DATE | - | NO | Fecha en que se realizó la evaluación | Raw+ | 2026-01-15 |
| `evaluador_id` | INTEGER | - | NO | employee_id del supervisor que evalúa | Raw+ | 10189 |
| `performance_rating` | DECIMAL | 3,2 | NO | Calificación general (1-5 escala) | Raw+ | 4.25 |
| `competencia_tecnica` | DECIMAL | 3,2 | SÍ | Habilidades técnicas (1-5) | Raw+ | 4.50 |
| `competencia_liderazgo` | DECIMAL | 3,2 | SÍ | Capacidad de liderazgo (1-5) | Raw+ | 3.75 |
| `competencia_trabajo_equipo` | DECIMAL | 3,2 | SÍ | Colaboración (1-5) | Raw+ | 4.00 |
| `cumplimiento_objetivos_pct` | INTEGER | - | SÍ | % de metas alcanzadas | Raw+ | 95 |
| `comentarios_evaluador` | TEXT | - | SÍ | Retroalimentación cualitativa | Raw+ | "Excelente..." |
| `objetivos_siguiente_periodo` | TEXT | - | SÍ | Metas para próximo ciclo | Raw+ | "Certificación..." |

---

### 6. Engagement & Climate (Clima Organizacional)

| Campo | Tipo | Longitud | Nulos | Descripción | Capa | Ejemplo |
|-------|------|----------|-------|-------------|------|---------|
| `employee_id` | INTEGER | - | NO | FK a Employee Master | Todas | 10234 |
| `fecha_encuesta` | DATE | - | NO | Fecha de aplicación | Raw+ | 2025-12-15 |
| `satisfaction_score` | DECIMAL | 3,2 | NO | Satisfacción general (1-5) | Raw+ | 4.2 |
| `work_life_balance` | DECIMAL | 3,2 | SÍ | Balance vida-trabajo (1-5) | Raw+ | 3.8 |
| `oportunidades_crecimiento` | DECIMAL | 3,2 | SÍ | Percepción de desarrollo (1-5) | Raw+ | 4.0 |
| `relacion_con_jefe` | DECIMAL | 3,2 | SÍ | Calidad de supervisión (1-5) | Raw+ | 4.5 |
| `recomendaria_empresa` | INTEGER | - | SÍ | NPS: 0-10 | Raw+ | 8 |
| `intent_renuncia_6m` | BOOLEAN | - | SÍ | ¿Planea renunciar en 6 meses? | Raw+ | FALSE |

---

### 7. Turnover Analytics (Capa Master - KPIs Calculados)

| Campo | Tipo | Longitud | Nulos | Descripción | Capa | Ejemplo |
|-------|------|----------|-------|-------------|------|---------|
| `employee_id` | INTEGER | - | NO | FK a Employee Master | Master | 10234 |
| `snapshot_date` | DATE | - | NO | Fecha del snapshot | Master | 2026-02-04 |
| `turnover_risk_score` | DECIMAL | 4,3 | NO | Score predictivo (0-1) | Master | 0.682 |
| `flight_risk_category` | VARCHAR | 10 | NO | Low, Medium, High | Master | "High" |
| `dias_ultima_promocion` | INTEGER | - | SÍ | Días desde último ascenso | Master | 730 |
| `ratio_salario_mercado` | DECIMAL | 4,3 | SÍ | Salario vs benchmark (1=mercado) | Master | 0.85 |
| `ausentismo_pct_3m` | DECIMAL | 5,2 | SÍ | % días ausente últimos 3 meses | Master | 4.50 |
| `variacion_performance_6m` | DECIMAL | 4,2 | SÍ | Cambio en rating vs 6 meses atrás | Master | -0.25 |
| `probabilidad_renuncia_90d` | DECIMAL | 4,3 | NO | Probabilidad según modelo ML | Master | 0.73 |

---

## 🔑 Catálogos y Códigos

### Departamentos

| Código | Nombre | Tipo | Gerente Responsable |
|--------|--------|------|-------------------|
| VEN | Ventas | Comercial | ID 10010 |
| TI | Tecnología | Soporte | ID 10025 |
| FIN | Finanzas | Administrativo | ID 10003 |
| RRHH | Recursos Humanos | Soporte | ID 10001 |
| OPS | Operaciones | Operativo | ID 10050 |
| MKT | Marketing | Comercial | ID 10015 |

### Estados Laborales

| Código | Descripción | Incluir en Headcount |
|--------|-------------|---------------------|
| ACT | Activo | SÍ |
| INA | Inactivo (renunció/cesado) | NO |
| LIC | Licencia temporal (médica, maternidad) | SÍ |
| SUS | Suspendido (disciplinario) | NO |
| VAC | Vacaciones | SÍ |

---

## 📐 Reglas de Negocio

### Validaciones Críticas

1. **Unicidad de DNI**: No pueden existir dos `employee_id` con el mismo `dni`
2. **Fechas lógicas**: `fecha_ingreso <= fecha_egreso`
3. **Salario mínimo**: `salario_base >= 1025` (sueldo mínimo Perú 2026)
4. **Edad laboral**: `edad BETWEEN 18 AND 70`
5. **Jerarquía**: `supervisor_id` no puede ser igual a `employee_id` (evitar auto-supervisión)

### Cálculos Estándar

**Antigüedad en años**:
```sql
antiguedad_años = DATEDIFF(CURRENT_DATE, fecha_ingreso) / 365.25
```

**Tasa de Rotación (Turnover Rate) Mensual**:
```sql
turnover_rate = (COUNT(salidas_mes) / AVG(headcount_mes)) * 100
```

**Time to Hire**:
```sql
time_to_hire_days = DATEDIFF(fecha_contratacion, fecha_publicacion_vacante)
```

---

## 🔄 Versionado

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-02-04 | Versión inicial del diccionario |

---

## 👤 Mantenedor

**James Lalupu** - People Analytics Specialist  
Última actualización: 2026-02-04
