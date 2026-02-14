# 🎯 Diseño de Incentivos y Pagos Variables

## Introducción

Los **incentivos** son compensaciones variables vinculadas al logro de objetivos específicos, diseñados para alinear comportamientos con resultados de negocio.

## Tipos de Incentivos

### 1. Por Frecuencia
- **Corto Plazo**: Mensuales, trimestrales, anuales
- **Largo Plazo**: Plurianuales (2-5 años)

### 2. Por Población
- **Comerciales**: Ventas, cobranzas, captación
- **Operativos**: Productividad, calidad, seguridad
- **Back-Office**: Proyectos, eficiencia, NPS

### 3. Por Estructura
- **Bonos**: Monto fijo al logro de meta
- **Comisiones**: % de venta o resultado
- **Mixtos**: Salario + comisión/bono

## KPIs Comunes por Área

### Comercial (Ventas)
| KPI | Fórmula | Peso Típico |
|-----|---------|-------------|
| Ventas netas | Ingresos - devoluciones | 40-60% |
| Margen | (Precio venta - costo) / Precio | 20-30% |
| Nuevos clientes | # clientes nuevos periodo | 10-20% |
| NPS | Promotores - Detractores | 5-10% |
| Cobranzas | % facturas cobradas < 30 días | 10-15% |

### Operaciones (Retail/Logística)
| KPI | Fórmula | Peso Típico |
|-----|---------|-------------|
| Productividad | Unidades / hora-hombre | 30-40% |
| Mermas | (Stock inicial + compras - ventas - stock final) / ventas × 100 | 20-30% |
| Rotación inventario | Costo de ventas / Inventario promedio | 15-20% |
| Incidentes seguridad | # accidentes / # empleados × 100 | 10-15% |
| Cumplimiento entregas | Entregas a tiempo / Total entregas × 100 | 15-25% |

### Back-Office (Soporte)
| KPI | Fórmula | Peso Típico |
|-----|---------|-------------|
| Proyectos completados | # proyectos finalizados / # proyectos planeados | 30-40% |
| Eficiencia procesos | Tiempo actual / Tiempo estándar × 100 | 20-30% |
| NPS interno | Satisfacción clientes internos | 15-25% |
| Errores | # errores / # transacciones × 100 | 10-20% |
| Cumplimiento plazos | Tareas a tiempo / Total tareas × 100 | 20-30% |

## Componentes de un Esquema de Incentivos

### 1. Población Elegible
**Criterios:**
- Rol (comercial, gerencial, todos)
- Nivel (ejecutivo, gerencial, profesional)
- Antigüedad (ej: > 3 meses)
- Tipo contrato (indefinido, full-time)

### 2. Incentivo Target (On-Target Incentive - OTI)

**Definición:** Monto que se paga al 100% de cumplimiento de metas.

**Expresión:**
- Como % del salario base (ej: 20% del salario anual)
- Como monto fijo (ej: S/. 5,000 anuales)
- Como múltiplos del salario mensual (ej: 2 salarios)

**Ejemplo:**
```
Salario anual: S/. 72,000 (S/. 6,000 × 12)
OTI: 25% del salario anual
OTI = 72,000 × 0.25 = S/. 18,000 anuales
```

### 3. Threshold (Umbral Mínimo)

**Definición:** Cumplimiento mínimo para empezar a pagar incentivo.

**Típico:** 80-90% de la meta

**Ejemplo:**
```
Si cumplimiento < 80%: Pago = 0
Si cumplimiento ≥ 80%: Inicia pago proporcional
```

### 4. Target (Meta)

**Definición:** Nivel de desempeño esperado (100%).

**Cálculo:**
- Histórico + crecimiento
- Benchmark de mercado
- Capacidad instalada

**Ejemplo (Ventas):**
```
Ventas año anterior: S/. 10M
Crecimiento esperado: 15%
Meta = 10M × 1.15 = S/. 11.5M
```

### 5. Cap (Techo)

**Definición:** Cumplimiento máximo que se paga.

**Típico:** 120-150% de la meta

**Razones para cap:**
- Controlar costo
- Evitar incentivos a prácticas riesgosas
- Limitar beneficios por factores externos

### 6. Aceleradores

**Definición:** Pago > 1:1 por sobre-cumplimiento.

**Ejemplo:**
```
80-100%: Pago 1:1
100-120%: Pago 1.5:1 (acelerador)
> 120%: Cap

Si logras 110%:
- Primeros 100 puntos: 100 × 1 = 100
- Siguientes 10 puntos: 10 × 1.5 = 15
- Total pago: 115% del OTI
```

### 7. Multiplicadores

**Definición:** Factor que ajusta el pago basado en cumplimiento de meta secundaria.

**Ejemplo:**
```
KPI Principal: Ventas (70% weight)
KPI Secundario: NPS (30% weight)

Si Ventas = 100% y NPS = 120%:
Pago = OTI × (0.70 × 100% + 0.30 × 120%)
     = OTI × (70% + 36%)
     = OTI × 106%
```

## Curvas de Pago

### Curva Lineal
```
Pago % = (Cumplimiento % - Threshold %) / (100% - Threshold %) × 100%
```

**Ejemplo:**
```
Threshold: 80%
Cumplimiento: 90%

Pago = (90 - 80) / (100 - 80) × 100 = 50%
```

### Curva con Acelerador
```
If cumplimiento ≤ 100%:
    Pago = cumplimiento

If 100% < cumplimiento ≤ cap:
    Pago = 100 + (cumplimiento - 100) × acelerador
```

**Ejemplo:**
```
Cumplimiento: 110%
Acelerador: 1.5x sobre 100%

Pago = 100 + (110 - 100) × 1.5
     = 100 + 15
     = 115%
```

## Diseño de Esquema: Ejemplo Completo

### Caso: Vendedor de Retail (Sodimac)

**Población:** Vendedores de tienda  
**OTI:** 30% del salario anual  
**Frecuencia:** Trimestral  
**KPIs:**

| KPI | Peso | Threshold | Target | Cap |
|-----|------|-----------|--------|-----|
| Ventas netas | 50% | 85% | 100% | 130% |
| Margen promedio | 30% | 90% | 100% | 120% |
| NPS tienda | 20% | 80% | 100% | 110% |

**Aceleradores:**
- Ventas: 1.5x sobre 100%
- Margen: 1.2x sobre 100%
- NPS: Lineal

### Cálculo Práctico

**Datos empleado:**
- Salario anual: S/. 36,000
- OTI anual: 36,000 × 30% = S/. 10,800
- OTI trimestral: 10,800 / 4 = S/. 2,700

**Resultados Q1:**
- Ventas: 112% (sobre 100% → acelerador)
- Margen: 95% (entre threshold y target)
- NPS: 105%

**Cálculo por KPI:**

1. **Ventas (50% peso):**
```
85-100%: Lineal
100-130%: Acelerador 1.5x

Cumplimiento: 112%
Hasta 100: 100
De 100 a 112: (112-100) × 1.5 = 18
Total: 118%

Contribución = 118% × 50% = 59%
```

2. **Margen (30% peso):**
```
Threshold: 90%
Cumplimiento: 95%

Pago = (95 - 90) / (100 - 90) × 100 = 50%

Contribución = 50% × 30% = 15%
```

3. **NPS (20% peso):**
```
Cumplimiento: 105%
Pago: 105% (lineal)

Contribución = 105% × 20% = 21%
```

**Total:**
```
Pago % = 59% + 15% + 21% = 95%

Incentivo Q1 = 2,700 × 0.95 = S/. 2,565
```

## Simulación What-If Analysis

### Herramienta en Excel

**Objetivo:** Predecir costos en diferentes escenarios.

**Variables de entrada:**
- # vendedores
- Distribución de cumplimiento
- OTI promedio

**Variables de salida:**
- Costo total incentivos
- % vs presupuesto
- ROI (incremento ventas / costo incentivo)

### Ejemplo de Simulación

**Escenario 1: Conservador**
```
50 vendedores
Distribución:
- 20% bajo threshold (no paga)
- 50% entre 85-100% (pago parcial promedio 60%)
- 25% entre 100-120% (pago promedio 110%)
- 5% en cap 130% (pago 145%)

OTI promedio: S/. 10,800

Costo:
= 50 × 10,800 × (0.20×0 + 0.50×0.60 + 0.25×1.10 + 0.05×1.45)
= 50 × 10,800 × (0 + 0.30 + 0.275 + 0.0725)
= 50 × 10,800 × 0.6475
= S/. 349,650
```

**Presupuesto por escenario:**

| Escenario | Cumplimiento Prom | Costo Total | % vs Budget |
|-----------|-------------------|-------------|-------------|
| Pesimista | 85% | S/. 270,000 | 50% |
| Realista | 95% | S/. 350,000 | 65% |
| Optimista | 110% | S/. 500,000 | 93% |
| Stretch | 125% | S/. 600,000 | 111% |

## Control de Fraude y Errores

### Cláusulas de Ajuste

**1. Calidad (Quality Gate):**
```
If errores_críticos > threshold:
    Incentivo final = Incentivo calculado × 0
```

**2. Clawback:**
```
Si después del pago se descubre fraude:
    Empresa puede recuperar incentivo pagado
```

**3. Proration:**
```
If meses_trabajados < periodo_completo:
    Incentivo = Incentivo calculado × (meses_trabajados / meses_totales)
```

### Ejemplo Proration
```
Incentivo anual calculado: S/. 10,000
Empleado renunció en mes 8:

Incentivo prorrateado = 10,000 × (8/12) = S/. 6,667
```

## Indicadores de Salud del Esquema

### 1. Costo vs Productividad
```
ROI = (Incremento Ventas - Costo Incentivos) / Costo Incentivos
```

**Target:** ROI > 3:1

### 2. Distribución de Pago
**Ideal:**
- < 10% no cumple threshold
- 20-30% en threshold-target
- 40-50% en target
- 10-20% sobre target
- < 5% en cap

### 3. Predictibilidad
```
Varianza = Desviación Estándar (Pagos) / Promedio Pagos
```

**Target:** Varianza < 30%

## 📊 Ejercicio Práctico

**Diseña un esquema de incentivos para:**

**Rol:** Jefe de Tienda (Sodimac)  
**Salario:** S/. 5,000 mensuales  
**OTI sugerido:** 40% anual  

**KPIs propuestos:**
- Ventas tienda
- Margen bruto
- Mermas
- NPS
- Rotación personal

**Responde:**
1. ¿Qué peso le darías a cada KPI?
2. ¿Qué threshold/target/cap usarías?
3. ¿Aplicarías aceleradores? ¿En cuál KPI?
4. Calcula el costo anual si tienes 50 jefes de tienda con cumplimiento promedio de 105%

**Respuestas al final del módulo →**
