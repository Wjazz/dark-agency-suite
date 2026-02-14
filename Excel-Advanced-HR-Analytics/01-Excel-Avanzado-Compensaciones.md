# 📊 Excel Avanzado para Compensaciones y HR Analytics

## Introducción

Este módulo cubre las funcionalidades avanzadas de Excel necesarias para trabajar en Compensaciones y People Analytics. Sodimac pide "Excel intermedio-avanzado", que incluye:

- Tablas dinámicas avanzadas
- Fórmulas complejas (BUSCARV, ÍNDICE/COINCIDIR, SUMAR.SI.CONJUNTO)
- Modelado financiero
- Automatización con Macros (VBA básico)
- Power Query (ETL básico)
- Dashboards interactivos

## Nivel 1: Funciones Esenciales para Compensaciones

### 1. BUSCARV / VLOOKUP
**Uso:** Buscar datos de otras tablas (ej: midpoint de banda salarial)

```excel
=BUSCARV(valor_buscado; tabla; columna; [coincidencia_exacta])
```

**Ejemplo:**
```excel
=BUSCARV(B2; Bandas_Salariales!A:C; 3; FALSO)
```
Busca el salario en la tabla de bandas y devuelve el valor de la columna 3.

**Limitación:** Solo busca hacia la derecha.

### 2. ÍNDICE + COINCIDIR (INDEX + MATCH)
**Uso:** Más flexible que BUSCARV, puede buscar en cualquier dirección.

```excel
=ÍNDICE(rango_devolver; COINCIDIR(valor_buscar; rango_buscar; 0))
```

**Ejemplo - Buscar midpoint:**
```excel
=ÍNDICE(Bandas!C:C; COINCIDIR(A2; Bandas!A:A; 0))
```

**Ejemplo - Buscar con dos criterios:**
```excel
=ÍNDICE(Salarios!D:D; 
        COINCIDIR(1; 
                  (Salarios!A:A=A2)*(Salarios!B:B=B2); 
                  0))
```
*(Fórmula matricial: Ctrl+Shift+Enter)*

### 3. SUMAR.SI.CONJUNTO / SUMIFS
**Uso:** Sumar con múltiples criterios.

```excel
=SUMAR.SI.CONJUNTO(rango_suma; rango_criterio1; criterio1; rango_criterio2; criterio2; ...)
```

**Ejemplo - Masa salarial por departamento:**
```excel
=SUMAR.SI.CONJUNTO(Salarios!D:D; 
                    Empleados!C:C; "Ventas"; 
                    Empleados!E:E; "Activo")
```

### 4. SI.ERROR / IFERROR
**Uso:** Manejar errores en fórmulas.

```excel
=SI.ERROR(fórmula; valor_si_error)
```

**Ejemplo:**
```excel
=SI.ERROR(BUSCARV(A2; Mercado!A:C; 3; FALSO); "No disponible")
```

### 5. Fórmulas para Compa-Ratio

```excel
=REDONDEAR((Salario_Actual / Midpoint) * 100; 2)
```

**Con clasificación:**
```excel
=SI(Compa_Ratio<80; "Muy bajo";
   SI(Compa_Ratio<90; "Bajo";
      SI(Compa_Ratio<=110; "En línea";
         SI(Compa_Ratio<=120; "Alto"; "Muy alto"))))
```

### 6. Fórmulas para Range Penetration

```excel
=REDONDEAR(((Salario - Mínimo) / (Máximo - Mínimo)) * 100; 2)
```

**Con cuartiles:**
```excel
=SI(Range_Penetration<25; "Q1";
   SI(Range_Penetration<50; "Q2";
      SI(Range_Penetration<75; "Q3"; "Q4")))
```

## Nivel 2: Tablas Dinámicas Avanzadas

### Caso: Análisis de Compensación por Departamento

**Datos necesarios:**
- Empleados (ID, Nombre, Departamento, Puesto, Banda)
- Salarios (ID, Salario Actual, Fecha)
- Bandas (Banda, Midpoint, Mínimo, Máximo)

**Tabla dinámica:**

1. **Filas:** Departamento, Banda
2. **Valores:** 
   - Suma de Salario Actual
   - Promedio de Compa-Ratio
   - Cuenta de Empleados
3. **Filtros:** Fecha (último período), Estado (Activo)

**Campos calculados:**
```excel
='Salario Promedio' / 'Midpoint Promedio'
```

### Segmentaciones (Slicers)

**Uso:** Filtros interactivos visuales.

1. Clic en tabla dinámica
2. Insertar → Segmentación de datos
3. Seleccionar campos: Departamento, Banda, Año

**Estilo profesional:**
- Configura 3+ columnas
- Aplica estilo corporativo
- Conecta a múltiples tablas dinámicas

## Nivel 3: Modelado de Incentivos

### Template: Calculadora de Incentivos

**Estructura:**

#### Hoja 1: Configuración
```
| KPI         | Peso | Threshold | Target | Cap | Acelerador |
|-------------|------|-----------|--------|-----|------------|
| Ventas      | 50%  | 85%       | 100%   | 130%| 1.5        |
| Margen      | 30%  | 90%       | 100%   | 120%| 1.2        |
| NPS         | 20%  | 80%       | 100%   | 110%| 1.0        |
```

#### Hoja 2: Cálculo Individual
```
Empleado: [Nombre]
OTI Anual: S/. [10,800]

| KPI    | Logro | Pago % | Peso | Contribución |
|--------|-------|--------|------|--------------|
| Ventas | 112%  | =FÓRMULA| 50% | =...        |
| ...    |       |        |      |              |
```

**Fórmula de pago:**
```excel
=SI(Logro<Threshold; 0;
   SI(Logro<=Target; 
      ((Logro-Threshold)/(Target-Threshold))*100;
      MÍNIMO(100+(Logro-Target)*Acelerador; 
             ((Cap-Threshold)/(Target-Threshold))*100)))
```

#### Hoja 3: Simulación de Escenarios

**Tabla de datos (Data Table):**

1. Crear tabla con escenarios de logro (85%, 90%, 95%, ..., 130%)
2. Datos → Análisis Y si → Tabla de datos
3. Variable fila: Celda de logro

**Resultado:**
```
| Logro Ventas | Pago Total | Monto S/. |
|--------------|------------|-----------|
| 85%          | 25%        | 2,700     |
| 90%          | 45%        | 4,860     |
| ...          | ...        | ...       |
```

### Gráfico de Tornado (Análisis de Sensibilidad)

**Uso:** Identificar qué KPI tiene mayor impacto.

1. Variar cada KPI ±20% manteniendo otros constantes
2. Calcular cambio en pago total
3. Graficar barras horizontales

## Nivel 4: Power Query (ETL Básico)

### Caso: Consolidar múltiples archivos de nómina

**Escenario:** Tienes 12 archivos Excel (uno por mes) con la misma estructura.

**Proceso:**

1. **Datos → Obtener datos → Desde carpeta**
2. Seleccionar carpeta con archivos
3. **Combinar y transformar**

**Transformaciones comunes:**

```powerquery
// Filtrar solo archivos .xlsx
= Table.SelectRows(Source, each Text.EndsWith([Name], ".xlsx"))

// Agregar columna de mes desde nombre archivo
= Table.AddColumn(#"Previous Step", "Mes", each Text.BetweenDelimiters([Name], "Nomina_", ".xlsx"))

// Limpiar salarios (eliminar símbolos)
= Table.TransformColumns(#"Previous Step", {{"Salario", each Number.From(Text.Remove(_, {"S/.", ",", " "})), type number}})

// Filtrar empleados activos
= Table.SelectRows(#"Previous Step", each [Estado] = "Activo")
```

**Resultado:** Tabla consolidada de 12 meses lista para análisis.

### Caso: Calcular Compa-Ratio automáticamente

```powerquery
// Combinar tabla Empleados con Bandas
= Table.NestedJoin(Empleados, {"Banda"}, Bandas, {"Banda_ID"}, "Bandas", JoinKind.LeftOuter)

// Expandir columna Midpoint
= Table.ExpandTableColumn(#"Previous Step", "Bandas", {"Midpoint"}, {"Midpoint"})

// Calcular Compa-Ratio
= Table.AddColumn(#"Previous Step", "Compa_Ratio", each [Salario_Actual] / [Midpoint] * 100)

// Clasificar
= Table.AddColumn(#"Previous Step", "Clasificación", 
    each if [Compa_Ratio] < 80 then "Muy bajo"
         else if [Compa_Ratio] < 90 then "Bajo"
         else if [Compa_Ratio] <= 110 then "En línea"
         else if [Compa_Ratio] <= 120 then "Alto"
         else "Muy alto")
```

## Nivel 5: Macros y VBA (Automatización Básica)

### Macro 1: Actualizar todos los datos

```vba
Sub ActualizarTodo()
    ' Actualizar conexiones de Power Query
    ActiveWorkbook.RefreshAll
    
    ' Esperar a que termine
    Application.Wait (Now + TimeValue("0:00:05"))
    
    ' Actualizar tablas dinámicas
    Dim pt As PivotTable
    For Each pt In ActiveSheet.PivotTables
        pt.RefreshTable
    Next pt
    
    MsgBox "Datos actualizados correctamente", vbInformation
End Sub
```

### Macro 2: Exportar reporte a PDF

```vba
Sub ExportarReporte()
    Dim rutaPDF As String
    Dim nombreArchivo As String
    
    ' Crear nombre con fecha
    nombreArchivo = "Reporte_Compensacion_" & Format(Date, "yyyy-mm-dd") & ".pdf"
    rutaPDF = ThisWorkbook.Path & "\" & nombreArchivo
    
    ' Exportar hoja activa
    ActiveSheet.ExportAsFixedFormat _
        Type:=xlTypePDF, _
        Filename:=rutaPDF, _
        Quality:=xlQualityStandard, _
        OpenAfterPublish:=True
        
    MsgBox "Reporte exportado: " & nombreArchivo, vbInformation
End Sub
```

### Macro 3: Enviar por correo automáticamente

```vba
Sub EnviarReporte()
    Dim OutlookApp As Object
    Dim Mail As Object
    
    Set OutlookApp = CreateObject("Outlook.Application")
    Set Mail = OutlookApp.CreateItem(0)
    
    With Mail
        .To = "gerente@empresa.com"
        .CC = "rrhh@empresa.com"
        .Subject = "Reporte Mensual de Compensaciones - " & Format(Date, "mmmm yyyy")
        .Body = "Adjunto el reporte actualizado de compensaciones." & vbCrLf & vbCrLf & _
                "Saludos," & vbCrLf & "Equipo de People Analytics"
        .Attachments.Add ThisWorkbook.Path & "\Reporte_Compensacion_" & Format(Date, "yyyy-mm-dd") & ".pdf"
        .Display  ' Cambiar a .Send para enviar automáticamente
    End With
    
    Set Mail = Nothing
    Set OutlookApp = Nothing
End Sub
```

## Nivel 6: Dashboard Interactivo

### Componentes de un Dashboard Profesional

**Layout típico:**

```
┌─────────────────────────────────────────────┐
│   KPIs Principales (Cards)                  │
│  ┌────────┐ ┌────────┐ ┌────────┐          │
│  │Headcount│Masa Sal.│Compa-R. │          │
│  └────────┘ └────────┘ └────────┘          │
├─────────────────────────────────────────────┤
│  Filtros (Slicers)                          │
│  □ Departamento  □ Banda  □ Año            │
├──────────────────┬──────────────────────────┤
│                  │                          │
│  Gráfico Combo:  │  Tabla Top/Bottom:      │
│  Masa salarial + │  - Top 10 salarios      │
│  Compa-ratio     │  - Bottom 10 salarios   │
│                  │                          │
├──────────────────┴──────────────────────────┤
│  Análisis de Distribución                   │
│  Histograma: Empleados por Compa-Ratio     │
└─────────────────────────────────────────────┘
```

### Fórmulas para KPI Cards

**Headcount:**
```excel
=CONTAR.SI.CONJUNTO(Empleados!E:E; "Activo"; Empleados!C:C; Filtro_Depto)
```

**Masa Salarial:**
```excel
=SUMAR.SI.CONJUNTO(Salarios!D:D; Empleados!C:C; Filtro_Depto; Empleados!E:E; "Activo")
```

**Compa-Ratio Promedio:**
```excel
=PROMEDIO.SI.CONJUNTO(Analisis!F:F; Empleados!C:C; Filtro_Depto; Empleados!E:E; "Activo")
```

### Formatos condicionales avanzados

**Barra de datos con punto medio:**

1. Seleccionar rango de Compa-Ratios
2. Formato condicional → Barras de datos → Más reglas
3. Configurar:
   - Mínimo: 80
   - Punto medio: 100 (amarillo)
   - Máximo: 120
   - Colores: Rojo → Amarillo → Verde

**Iconos según cuartil:**

```excel
Regla 1: Si Range_Penetration >= 75  → ⬆ (Verde)
Regla 2: Si Range_Penetration >= 50  → → (Amarillo)
Regla 3: Si Range_Penetration >= 25  → ↘ (Naranja)
Regla 4: Si Range_Penetration < 25   → ⬇ (Rojo)
```

## Ejercicios Prácticos

### Ejercicio 1: Calculadora de Merit Increase

**Crea un archivo Excel con:**

1. Hoja "Empleados" con datos:
   - ID, Nombre, Salario, Performance (1-5), Compa-Ratio, Cuartil
2. Hoja "Merit Matrix":
   ```
   | Performance | Q1  | Q2  | Q3  | Q4  |
   |-------------|-----|-----|-----|-----|
   | 5 - Exceeds | 10% | 8%  | 6%  | 4%  |
   | 4 - Meets+  | 7%  | 6%  | 5%  | 3%  |
   | 3 - Meets   | 5%  | 4%  | 3%  | 2%  |
   | 2 - Needs   | 2%  | 1%  | 0%  | 0%  |
   | 1 - Under   | 0%  | 0%  | 0%  | 0%  |
   ```
3. Usar ÍNDICE + COINCIDIR para asignar % a cada empleado
4. Calcular nuevo salario
5. Calcular budget total necesario

### Ejercicio 2: Dashboard de Equidad Salarial

**Componentes:**

1. Gráfico de dispersión: Salario vs Antigüedad (por género)
2. Tabla dinámica: Salario promedio por Puesto y Género
3. Indicador: % Brecha salarial
4. Filtros por Departamento y Nivel

### Ejercicio 3: Simulador de Incentivos

**Replica el modelo de Sodimac:**

- 3 KPIs: Ventas (50%), Margen (30%), NPS (20%)
- Thresholds, targets, caps y aceleradores
- Tabla de simulación de escenarios
- Gráfico de curva de pago
- Cálculo de costo total para 50 vendedores

## Recursos Adicionales

### Templates Descargables
*(En este repositorio encontrarás)*

1. `Template_Calculadora_Bandas_Salariales.xlsx`
2. `Template_Merit_Matrix.xlsx`
3. `Template_Simulador_Incentivos.xlsx`
4. `Template_Dashboard_Compensacion.xlsx`

### Atajos de Teclado Esenciales

| Atajo | Función |
|-------|---------|
| Ctrl+T | Crear tabla |
| Alt+N+V | Crear tabla dinámica |
| Ctrl+Shift+L | Activar filtros |
| F4 | Fijar referencia ($) |
| Ctrl+; | Insertar fecha actual |
| Alt+= | Autosuma |
| Ctrl+Shift+Enter | Fórmula matricial |

### Funciones Avanzadas para Explorar

- `SUMAR.SI.CONJUNTO()`
- `PROMEDIO.SI.CONJUNTO()`
- `CONTAR.SI.CONJUNTO()`
- `ÍNDICE() + COINCIDIR()`
- `DESREF()` - Para rangos dinámicos
- `JERARQUIA.MEDIA()` - Para ranking
- `PERCENTIL.INC()` - Para análisis de mercado
