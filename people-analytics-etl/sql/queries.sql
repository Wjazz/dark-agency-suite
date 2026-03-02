/* ============================================================================
   REPOSITORIO: Dark Agency Suite (people-analytics-etl)
   MÓDULO: Analytical Queries & Performance Testing
   AUTOR: [Tu Nombre]
   DESCRIPCIÓN: Consultas core para People Analytics, incluyendo cálculo 
                de rotación (turnover), métricas de riesgo y optimización.
   ============================================================================ */

-- ----------------------------------------------------------------------------
-- A. CÁLCULO DE ROTACIÓN MENSUAL (TURNOVER RATE)
-- Objetivo: Calcular la tasa de rotación (%) de los últimos 12 meses.
-- Arquitectura: Utiliza CTEs para crear un snapshot mensual.
-- Prevención de errores: Uso de NULLIF para evitar división por cero.
-- ----------------------------------------------------------------------------
WITH monthly_snapshot AS (
  SELECT
    date_trunc('month', snapshot_date)::date AS month,
    -- Conteo de empleados activos al final del periodo
    COUNT(CASE WHEN estado_laboral = 'Activo' THEN 1 END) AS headcount_end,
    -- Conteo de salidas que ocurrieron en el mismo mes del snapshot
    COUNT(CASE WHEN fecha_egreso IS NOT NULL
               AND date_trunc('month', fecha_egreso) = date_trunc('month', snapshot_date)
          THEN 1 END) AS departures
  FROM master.headcount_history
  WHERE snapshot_date >= (current_date - INTERVAL '12 months')
  GROUP BY 1
)
SELECT
  month,
  headcount_end,
  departures,
  -- Cálculo del porcentaje. numeric cast previene truncamiento entero.
  ROUND( 
    CASE 
        WHEN headcount_end = 0 THEN 0
        ELSE (departures::numeric * 100.0 / NULLIF(headcount_end,0)) 
    END, 2
  ) AS turnover_pct
FROM monthly_snapshot
ORDER BY month DESC;


-- ----------------------------------------------------------------------------
-- B. RANKING DE DEPARTAMENTOS POR TASA DE ROTACIÓN
-- Objetivo: Identificar los departamentos críticos (Top 10) usando Window Functions.
-- Arquitectura: Uso de FILTER en lugar de CASE para mayor legibilidad y 
--               función de ventana RANK() OVER() para clasificación.
-- ----------------------------------------------------------------------------
WITH dept_stats AS (
  SELECT
    departamento_nombre,
    COUNT(*) FILTER (WHERE estado_laboral = 'Activo') AS headcount,
    COUNT(*) FILTER (WHERE fecha_egreso IS NOT NULL
                     AND fecha_egreso >= current_date - INTERVAL '12 months') AS salidas_12m
  FROM master.employee_metrics
  GROUP BY departamento_nombre
)
SELECT
  departamento_nombre,
  headcount,
  salidas_12m,
  ROUND((salidas_12m::numeric / NULLIF(headcount,0) * 100), 2) AS turnover_12m_pct,
  -- Window function para generar el ranking basado en la tasa de salidas
  RANK() OVER (ORDER BY (salidas_12m::numeric / NULLIF(headcount,0)) DESC) AS turnover_rank
FROM dept_stats
ORDER BY turnover_12m_pct DESC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- C. DETECCIÓN DE RIESGO DE FUGA (LEAD INDICATORS)
-- Objetivo: Identificar empleados cuyo "Turnover Risk Score" (psicométrico/comportamental)
--           ha subido durante 2 meses consecutivos.
-- Arquitectura: Uso de la función de ventana LAG() para comparar contra periodos anteriores.
-- ----------------------------------------------------------------------------
WITH recent AS (
  SELECT
    employee_id,
    date_trunc('month', snapshot_date)::date AS month,
    AVG(turnover_risk_score) AS avg_risk
  FROM master.headcount_history
  WHERE snapshot_date >= current_date - INTERVAL '3 months'
  GROUP BY employee_id, 1
),
lagged AS (
  SELECT
    employee_id,
    month,
    avg_risk,
    -- Obtenemos el score del mes inmediato anterior particionado por empleado
    LAG(avg_risk) OVER (PARTITION BY employee_id ORDER BY month) AS prev_risk
  FROM recent
)
SELECT
  employee_id,
  month,
  avg_risk,
  prev_risk
FROM lagged
-- Condición de alerta: Incremento mayor al 5% respecto al mes anterior
WHERE prev_risk IS NOT NULL 
  AND avg_risk > prev_risk 
  AND (avg_risk - prev_risk) > 0.05
ORDER BY employee_id, month;


-- ----------------------------------------------------------------------------
-- D. ESTRATEGIA DE OPTIMIZACIÓN (DEMO PARA ENTREVISTAS)
-- Objetivo: Demostrar comprensión de los planes de ejecución y reducción de costos de I/O.
-- ----------------------------------------------------------------------------

-- 1. Ejecutar esto para mostrar el costo antes de optimizar (Table Scan)
/*
EXPLAIN ANALYZE
SELECT COUNT(*) FROM master.headcount_history 
WHERE snapshot_date >= '2025-01-01' AND estado_laboral='Activo';
*/

-- 2. Creación del Índice Compuesto (Alineado a la cardinalidad y filtros comunes)
CREATE INDEX IF NOT EXISTS idx_headcount_history_date_estado
ON master.headcount_history (snapshot_date, estado_laboral);

-- 3. Ejecutar nuevamente para mostrar el costo después (Index Scan)
/*
EXPLAIN ANALYZE
SELECT COUNT(*) FROM master.headcount_history 
WHERE snapshot_date >= '2025-01-01' AND estado_laboral='Activo';
*/
