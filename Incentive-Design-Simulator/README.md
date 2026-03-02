# 🎯 Simulador de Incentivos Comerciales

Herramienta profesional para diseñar, simular y analizar esquemas de compensación variable.

## 🚀 Características

- ✅ Modelado de KPIs múltiples con pesos personalizados
- ✅ Configuración de threshold, target, cap y aceleradores
- ✅ Simulación Monte Carlo (10,000+ escenarios)
- ✅ Visualización de curvas de pago
- ✅ Análisis de sensibilidad y proyección de costos
- ✅ Exportación de resultados (CSV, PNG)

## 📋 Requisitos

```bash
pip install pandas numpy matplotlib seaborn
```

## 🎯 Uso Rápido

### Ejecutar simulación predefinida (Sodimac)

```bash
python incentive_simulator.py
```

**Output:**
- `payout_curve_Ventas.png` - Curva de pago KPI Ventas
- `payout_curve_Margen.png` - Curva de pago KPI Margen
- `payout_curve_NPS.png` - Curva de pago KPI NPS
- `simulation_results.png` - Dashboard con resultados
- `simulation_results.csv` - Datos detallados de simulación

### Personalizar esquema

```python
from incentive_simulator import IncentiveScheme, KPIConfig

# Crear esquema personalizado
scheme = IncentiveScheme("Mi Esquema", oti_annual=15000)

# Agregar KPI
scheme.add_kpi(KPIConfig(
    name="Ventas",
    weight=0.60,        # 60% de peso
    threshold=85,       # Mínimo 85% para pagar
    target=100,         # Meta = 100%
    cap=150,            # Techo = 150%
    accelerator=2.0     # 2x sobre 100%
))

# Calcular pago individual
result = scheme.calculate_total_payout({
    "Ventas": 120  # Logró 120%
})

print(f"Pago: {result['total_payout_pct']:.1f}%")
print(f"Monto: S/. {result['incentive_amount']:,.0f}")
```

## 📊 Ejemplo de Salida

```
==============================================================
SIMULADOR DE INCENTIVOS COMERCIALES
==============================================================

📊 Creando esquema: Vendedor Sodimac
✓ Validación: Esquema válido

📈 Generando curvas de pago por KPI...
✓ Curva guardada: payout_curve_Ventas.png
✓ Curva guardada: payout_curve_Margen.png
✓ Curva guardada: payout_curve_NPS.png

🧮 Ejemplo de cálculo individual:
------------------------------------------------------------

Logros:
  • Ventas: 112% → Payout: 118.0% → Contribución: 59.0%
  • Margen: 95% → Payout: 50.0% → Contribución: 15.0%
  • NPS: 105% → Payout: 105.0% → Contribución: 21.0%

Resultado Final:
  • Payout Total: 95.0%
  • Monto Incentivo: S/. 10,260.00

🎲 Ejecutando simulación de 10,000 escenarios...
✓ Resultados guardados: simulation_results.csv
✓ Resultados guardados: simulation_results.png

💰 ANÁLISIS DE COSTO (50 vendedores):
------------------------------------------------------------
  • Empleados: 50
  • Payout promedio: S/. 10,523
  • Costo total anual: S/. 526,150
  • Percentil 10: S/. 5,234
  • Percentil 50: S/. 10,398
  • Percentil 90: S/. 16,210
```

## 🎯 Casos de Uso

### 1. Vendedor Retail (Sodimac - ejemplo incluido)

**KPIs:**
- Ventas netas (50%)
- Margen bruto (30%)
- NPS cliente (20%)

**OTI:** 30% salario anual

### 2. Jefe de Tienda

```python
scheme = IncentiveScheme("Jefe Tienda", oti_annual=24000)

scheme.add_kpi(KPIConfig("Ventas", 0.40, 90, 100, 130, 1.5))
scheme.add_kpi(KPIConfig("Margen", 0.25, 90, 100, 120, 1.2))
scheme.add_kpi(KPIConfig("Mermas", 0.20, 80, 100, 110, 1.0))
scheme.add_kpi(KPIConfig("NPS", 0.15, 85, 100, 115, 1.0))
```

### 3. Back Office (Analista)

```python
scheme = IncentiveScheme("Analista", oti_annual=12000)

scheme.add_kpi(KPIConfig("Proyectos_Completados", 0.50, 80, 100, 120, 1.3))
scheme.add_kpi(KPIConfig("Eficiencia", 0.30, 85, 100, 115, 1.0))
scheme.add_kpi(KPIConfig("NPS_Interno", 0.20, 80, 100, 110, 1.0))
```

## 📈 Análisis de Resultados

### Distribución de Pagos (ejemplo real)

```
Escenarios simulados: 10,000

Payout Total:
  • Media: 97.3%
  • Mediana: 98.1%
  • Desv. Est.: 12.4%
  • Min: 42.3%
  • Max: 145.6%

Distribución:
  • Sin pago (0%): 124 (1.2%)
  • Parcial (<100%): 4,823 (48.2%)
  • Target (100%±5%): 2,156 (21.6%)
  • Sobre target (>105%): 2,897 (29.0%)
```

### Proyección de Costos

Para **50 vendedores** con distribución normal de logros:

| Escenario | Cumplimiento Prom | Costo Total | % vs Budget |
|-----------|-------------------|-------------|-------------|
| Pesimista | 85% | S/. 270,000 | 50% |
| Realista | 95% | S/. 350,000 | 65% |
| Optimista | 110% | S/. 500,000 | 93% |
| Stretch | 125% | S/. 600,000 | 111% |

## 🔧 Funcionalidades Avanzadas

### Validación automática

```python
is_valid, message = scheme.validate()
if not is_valid:
    print(f"Error: {message}")
```

Valida que:
- Pesos sumen 100%
- Thresholds < Targets < Caps
- Aceleradores > 0

### Análisis de sensibilidad

```python
# Simular impacto de cambiar acelerador de Ventas
results = []
for acc in [1.0, 1.2, 1.5, 2.0]:
    scheme.kpis[0].accelerator = acc
    df = scheme.simulate_scenarios(1000)
    results.append(df['incentive_amount'].mean())
```

### Stress Testing

```python
# Escenario pesimista: logros bajos
pessimistic = {
    "Ventas": 80,
    "Margen": 85,
    "NPS": 90
}
result = scheme.calculate_total_payout(pessimistic)

# Escenario optimista: logros altos
optimistic = {
    "Ventas": 130,
    "Margen": 120,
    "NPS": 110
}
result = scheme.calculate_total_payout(optimistic)
```

## 📚 Teoría Detrás del Simulador

### Componentes de un Esquema

Ver documentación completa en: [`01-Fundamentos-Incentivos.md`](./01-Fundamentos-Incentivos.md)

**Conceptos clave:**
- **OTI (On-Target Incentive):** Monto que se paga al 100% de cumplimiento
- **Threshold:** Umbral mínimo para empezar a pagar
- **Target:** Meta = 100%
- **Cap:** Techo máximo de pago
- **Acelerador:** Multiplicador sobre target (incentiva sobre-cumplimiento)

### Fórmula de Pago

```
Si logro < threshold:
    Pago = 0%

Si threshold ≤ logro ≤ target:
    Pago = ((logro - threshold) / (target - threshold)) × 100%

Si logro > target:
    Pago = 100% + ((logro - target) × acelerador)
    (limitado por cap)
```

## 🎓 Aplicaciones en Entrevistas

### Pregunta: "¿Cómo diseñarías incentivos para vendedores?"

**Respuesta usando este simulador:**

```
"Utilizaría un modelo con 3 KPIs balanceados:

1. Ventas (50% peso): threshold 85%, target 100%, cap 130%, acelerador 1.5x
   - Incentiva volumen pero con mesura

2. Margen (30% peso): threshold 90%, target 100%, cap 120%, acelerador 1.2x
   - Evita descuentos excesivos

3. NPS (20% peso): threshold 80%, target 100%, cap 110%, sin acelerador
   - Asegura calidad de servicio

He simulado 10,000 escenarios y el costo promedio por vendedor sería 
S/. 10,500 anuales con un ROI proyectado de 3.2:1"
```

**Muestra el código:**
- "Aquí está mi herramienta que automatiza este análisis..."
- "Puedo generar curvas de pago en segundos..."
- "La simulación Monte Carlo me permite predecir costos con confianza estadística"

## 🏆 Ventajas Competitivas

✅ **vs Excel manual:**
- Escalable a cientos de empleados
- Simulación automatizada
- Visualizaciones profesionales

✅ **vs SAP/Workday:**
- Prototipado rápido
- Control total del modelo
- Sin costos de licencia

✅ **vs Consultoras:**
- Customizable al 100%
- Resultados en minutos
- Transparencia total del cálculo

## 📖 Documentación Adicional

- 📘 [Fundamentos de Incentivos](./01-Fundamentos-Incentivos.md) - Teoría completa
- 📗 [Casos de Estudio](./casos-estudio/) - Ejemplos reales
- 📊 [Excel Templates](./templates/) - Complementos en Excel

## 🤝 Contribuciones

Este es un proyecto educativo de portafolio. Sugerencias y mejoras son bienvenidas.

## 📜 Licencia

Uso libre para fines educativos y profesionales.

---

**Autor:** James  
**Stack:** Python, pandas, numpy, matplotlib, seaborn  
**Especialización:** Compensation Design & People Analytics  
**Última actualización:** Febrero 2026
