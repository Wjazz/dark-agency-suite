# 📘 Fundamentos de Compensaciones

## 1. Bandas Salariales (Salary Bands)

### ¿Qué son?
Las bandas salariales son rangos estructurados de remuneración para cada puesto o nivel organizacional. Permiten gestionar la equidad interna y externa.

### Componentes Clave

#### Midpoint (Punto Medio)
- Representa el valor de mercado del puesto
- Referencia para posicionamiento competitivo
- Se obtiene típicamente del percentil 50 del mercado

```
Midpoint = Percentil 50 del mercado
```

#### Mínimo y Máximo
```
Mínimo = Midpoint × (1 - Range Spread/2)
Máximo = Midpoint × (1 + Range Spread/2)
```

#### Range Spread (Amplitud de Banda)
Porcentaje de diferencia entre mínimo y máximo:

```
Range Spread = (Máximo - Mínimo) / Mínimo × 100
```

**Típicos por nivel:**
- Operativo: 30-40%
- Profesional: 40-50%
- Gerencial: 50-60%
- Ejecutivo: 60-80%

### Ejemplo Práctico

**Puesto:** Analista de Compensaciones  
**Midpoint mercado:** S/. 6,000  
**Range Spread:** 50%

```
Mínimo = 6,000 × (1 - 0.50/2) = S/. 4,500
Máximo = 6,000 × (1 + 0.50/2) = S/. 7,500

Banda salarial: S/. 4,500 - S/. 7,500
```

## 2. Compa-Ratio

### Definición
Indica la posición del salario actual respecto al midpoint de la banda.

### Fórmula
```
Compa-Ratio = Salario Actual / Midpoint × 100
```

### Interpretación
- **< 80%**: Muy por debajo de mercado (riesgo de fuga)
- **80-90%**: Debajo de mercado
- **90-110%**: En línea con mercado ✓
- **110-120%**: Por encima de mercado
- **> 120%**: Muy por encima (riesgo presupuestal)

### Ejemplo
```
Salario actual: S/. 5,400
Midpoint: S/. 6,000

Compa-Ratio = 5,400 / 6,000 × 100 = 90%
```
**Interpretación:** Ligeramente debajo de mercado, candidato para aumento.

## 3. Range Penetration (Posición en la Banda)

### Definición
Indica qué tan cerca está el salario del máximo de la banda.

### Fórmula
```
Range Penetration = (Salario - Mínimo) / (Máximo - Mínimo) × 100
```

### Interpretación
- **0-25%**: Cuartil 1 (nuevo en el rol)
- **25-50%**: Cuartil 2 (en desarrollo)
- **50-75%**: Cuartil 3 (competente)
- **75-100%**: Cuartil 4 (experto/tenured)

### Ejemplo
```
Salario: S/. 5,400
Mínimo: S/. 4,500
Máximo: S/. 7,500

Range Penetration = (5,400 - 4,500) / (7,500 - 4,500) × 100
                  = 900 / 3,000 × 100
                  = 30%
```
**Interpretación:** Cuartil 2, espacio para crecimiento en la banda.

## 4. Merit Matrices (Matrices de Mérito)

### ¿Qué son?
Herramientas para distribuir incrementos salariales basados en:
- **Performance** (eje Y)
- **Posición en la banda** (eje X)

### Estructura Típica

| Performance ↓ / Position → | Q1 (0-25%) | Q2 (25-50%) | Q3 (50-75%) | Q4 (75-100%) |
|---------------------------|------------|-------------|-------------|--------------|
| **Exceeds (5)**           | 8-10%      | 6-8%        | 5-6%        | 3-4%        |
| **Meets + (4)**           | 6-7%       | 5-6%        | 4-5%        | 2-3%        |
| **Meets (3)**             | 4-5%       | 3-4%        | 2-3%        | 0-2%        |
| **Needs Improve (2)**     | 0-2%       | 0-1%        | 0%          | 0%          |
| **Underperform (1)**      | 0%         | 0%          | 0%          | 0%          |

### Lógica
- **Alto performance + baja posición** = Mayor incremento (desarrollar)
- **Alto performance + alta posición** = Menor incremento (ya en techo)
- **Bajo performance** = Mínimo o ningún incremento

## 5. Budget Planning (Planificación Presupuestal)

### Proceso

#### Paso 1: Definir Budget Total
```
Budget Total = Masa Salarial Actual × % Incremento Promedio
```

Ejemplo:
```
Masa salarial: S/. 10,000,000
Incremento promedio mercado: 4.5%

Budget = 10,000,000 × 0.045 = S/. 450,000
```

#### Paso 2: Reservar para Promociones
```
Budget Promociones = Budget Total × % Reserva
Budget Merit = Budget Total - Budget Promociones
```

Ejemplo:
```
Reserva promociones: 20%

Budget Promociones = 450,000 × 0.20 = S/. 90,000
Budget Merit = 450,000 - 90,000 = S/. 360,000
```

#### Paso 3: Distribución por Merit Matrix
1. Clasificar empleados por cuadrante (Performance × Position)
2. Aplicar % según matriz
3. Validar que suma = budget disponible

#### Paso 4: Ajustar si Excede Budget
```
Factor de Ajuste = Budget Disponible / Suma de Incrementos Calculados
```

### Ejemplo Completo

**Equipo de 5 personas:**

| Empleado | Salario | Performance | Position | Incremento % | Incremento S/. |
|----------|---------|-------------|----------|--------------|----------------|
| Ana      | 5,000   | 5           | Q2       | 7%           | 350           |
| Luis     | 6,000   | 4           | Q3       | 4%           | 240           |
| María    | 4,500   | 3           | Q1       | 5%           | 225           |
| Carlos   | 7,000   | 5           | Q4       | 3%           | 210           |
| Elena    | 5,500   | 2           | Q2       | 0%           | 0             |
| **Total**|**28,000**|           |          | **4.38%**    | **1,225**     |

Budget disponible: S/. 1,200  
Total calculado: S/. 1,225  
Exceso: S/. 25

```
Factor = 1,200 / 1,225 = 0.9796

Incrementos ajustados:
Ana: 350 × 0.9796 = 343
Luis: 240 × 0.9796 = 235
...
```

## 6. Equidad Interna vs Externa

### Equidad Interna
**Objetivo:** Consistencia entre puestos similares dentro de la empresa.

**Métricas:**
- Compa-ratio por puesto
- Diferencias por género/antigüedad en mismo rol
- Coherencia de bandas entre niveles

### Equidad Externa
**Objetivo:** Competitividad frente al mercado.

**Métricas:**
- Posicionamiento percentil vs mercado
- Aging de datos (ajuste inflación)
- Brecha vs competitors

## 📊 Ejercicio Práctico

Usa estos datos para practicar:

**Empresa:** Retail SAC  
**Puesto:** Analista de Compensaciones  
**Mercado (Percentil 50):** S/. 6,200  
**Range Spread:** 50%

**Empleados:**
1. Juan - S/. 5,100 - Performance 4 - 2 años antigüedad
2. María - S/. 6,800 - Performance 5 - 5 años antigüedad
3. Pedro - S/. 4,700 - Performance 3 - 1 año antigüedad

**Calcula:**
1. Banda salarial (min-max)
2. Compa-ratio de cada empleado
3. Range penetration de cada empleado
4. Incrementos según merit matrix
5. Budget necesario

**Respuestas al final del módulo →**
