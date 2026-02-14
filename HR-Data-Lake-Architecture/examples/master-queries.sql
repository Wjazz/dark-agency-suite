-- ============================================
-- CONSULTAS SQL PARA MASTER LAYER
-- Ejemplos de queries analíticos sobre datos Parquet
-- ============================================

-- ============================================
-- 1. ANÁLISIS DE HEADCOUNT POR DEPARTAMENTO
-- ============================================
-- Muestra la distribución actual de empleados activos por departamento

SELECT 
    departamento_nombre,
    COUNT(*) as headcount,
    ROUND(AVG(salario_bruto), 2) as salario_promedio,
    ROUND(AVG(antiguedad_años), 2) as antiguedad_promedio_años
FROM master.employee_metrics
WHERE estado_laboral = 'Activo'
GROUP BY departamento_nombre
ORDER BY headcount DESC;

-- Resultado esperado:
-- departamento_nombre | headcount | salario_promedio | antiguedad_promedio_años
-- Ventas             | 145       | 5800.00          | 2.5
-- TI                 | 89        | 7200.00          | 3.2
-- Finanzas           | 62        | 6500.00          | 4.1


-- ============================================
-- 2. EMPLEADOS EN RIESGO DE ROTACIÓN (TOP 20)
-- ============================================
-- Identifica empleados con mayor probabilidad de renuncia

SELECT 
    employee_id,
    nombre_completo,
    departamento_nombre,
    puesto,
    turnover_risk_score,
    flight_risk_category,
    ratio_salario_mercado,
    performance_rating
FROM master.employee_metrics
WHERE estado_laboral = 'Activo'
  AND turnover_risk_score > 0.7  -- Alto riesgo
ORDER BY turnover_risk_score DESC
LIMIT 20;

-- ⚠️ Acción: Intervenir con planes de retención


-- ============================================
-- 3. TENDENCIA DE ROTACIÓN MENSUAL (ÚLTIMOS 12 MESES)
-- ============================================
-- Calcula la tasa de rotación mes a mes

WITH monthly_stats AS (
    SELECT 
        DATE_TRUNC('month', snapshot_date) as mes,
        COUNT(CASE WHEN estado_laboral = 'Activo' THEN 1 END) as headcount_fin,
        COUNT(CASE WHEN fecha_egreso IS NOT NULL 
                   AND DATE_TRUNC('month', fecha_egreso) = DATE_TRUNC('month', snapshot_date) 
              THEN 1 END) as salidas
    FROM master.headcount_history
    WHERE snapshot_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY DATE_TRUNC('month', snapshot_date)
)
SELECT 
    mes,
    headcount_fin,
    salidas,
    ROUND((salidas * 100.0 / headcount_fin), 2) as turnover_rate_pct
FROM monthly_stats
ORDER BY mes DESC;


-- ============================================
-- 4. ANÁLISIS DE EQUIDAD SALARIAL (GENDER PAY GAP)
-- ============================================
-- Compara salarios promedio entre géneros para detectar inequidades

SELECT 
    puesto,
    genero,
    COUNT(*) as num_empleados,
    ROUND(AVG(salario_bruto), 2) as salario_promedio,
    ROUND(MIN(salario_bruto), 2) as salario_min,
    ROUND(MAX(salario_bruto), 2) as salario_max
FROM master.employee_metrics
WHERE estado_laboral = 'Activo'
  AND puesto IN ('Analista de Ventas', 'Desarrollador Senior', 'Gerente de Operaciones')
GROUP BY puesto, genero
ORDER BY puesto, genero;

-- Cálculo de brecha salarial:
WITH salary_by_gender AS (
    SELECT 
        puesto,
        AVG(CASE WHEN genero = 'M' THEN salario_bruto END) as salario_masculino,
        AVG(CASE WHEN genero = 'F' THEN salario_bruto END) as salario_femenino
    FROM master.employee_metrics
    WHERE estado_laboral = 'Activo'
    GROUP BY puesto
)
SELECT 
    puesto,
    ROUND(salario_masculino, 2) as salario_masculino,
    ROUND(salario_femenino, 2) as salario_femenino,
    ROUND(((salario_masculino - salario_femenino) / salario_masculino * 100), 2) as brecha_pct
FROM salary_by_gender
WHERE salario_masculino IS NOT NULL AND salario_femenino IS NOT NULL
ORDER BY brecha_pct DESC;


-- ============================================
-- 5. TIME TO HIRE POR DEPARTAMENTO
-- ============================================
-- Mide la eficiencia del proceso de reclutamiento

SELECT 
    departamento_nombre,
    AVG(time_to_hire_days) as promedio_dias,
    MIN(time_to_hire_days) as min_dias,
    MAX(time_to_hire_days) as max_dias,
    COUNT(*) as contrataciones_ultimo_año
FROM master.recruitment_metrics
WHERE fecha_contratacion >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY departamento_nombre
ORDER BY promedio_dias DESC;

-- 🎯 Meta: Reducir TTH a < 30 días en todos los departamentos


-- ============================================
-- 6. EMPLEADOS CON BAJO DESEMPEÑO Y ALTO SALARIO
-- ============================================
-- Detecta posibles casos de compensación no alineada con resultados

SELECT 
    e.employee_id,
    e.nombre_completo,
    e.departamento_nombre,
    e.salario_bruto,
    e.performance_rating,
    e.ratio_salario_mercado
FROM master.employee_metrics e
WHERE e.estado_laboral = 'Activo'
  AND e.performance_rating < 3.0  -- Bajo desempeño
  AND e.ratio_salario_mercado > 1.05  -- Gana 5% más que mercado
ORDER BY e.salario_bruto DESC;


-- ============================================
-- 7. PROYECCIÓN DE VACANTES (PRÓXIMOS 90 DÍAS)
-- ============================================
-- Predice cuántos empleados podrían renunciar según modelo ML

SELECT 
    departamento_nombre,
    COUNT(*) as empleados_en_riesgo,
    ROUND(AVG(probabilidad_renuncia_90d), 3) as prob_promedio,
    ROUND(SUM(probabilidad_renuncia_90d), 0) as vacantes_esperadas
FROM master.employee_metrics
WHERE estado_laboral = 'Activo'
  AND probabilidad_renuncia_90d > 0.5
GROUP BY departamento_nombre
ORDER BY vacantes_esperadas DESC;

-- 📊 Uso: Planificar reclutamiento proactivo


-- ============================================
-- 8. ANÁLISIS DE PROMOCIONES INTERNAS
-- ============================================
-- Identifica empleados listos para promoción

SELECT 
    e.employee_id,
    e.nombre_completo,
    e.departamento_nombre,
    e.puesto,
    e.antiguedad_años,
    e.performance_rating,
    e.dias_ultima_promocion / 365 as años_sin_promocion
FROM master.employee_metrics e
WHERE e.estado_laboral = 'Activo'
  AND e.performance_rating >= 4.0  -- Alto desempeño
  AND e.antiguedad_años >= 2.0
  AND (e.dias_ultima_promocion IS NULL OR e.dias_ultima_promocion > 730)  -- >2 años sin promo
ORDER BY e.performance_rating DESC, e.antiguedad_años DESC
LIMIT 50;


-- ============================================
-- 9. DISTRIBUCIÓN DE ANTIGÜEDAD (HISTOGRAMA)
-- ============================================
-- Analiza la distribución de experiencia en la empresa

SELECT 
    CASE 
        WHEN antiguedad_años < 1 THEN '< 1 año'
        WHEN antiguedad_años BETWEEN 1 AND 2 THEN '1-2 años'
        WHEN antiguedad_años BETWEEN 2 AND 5 THEN '2-5 años'
        WHEN antiguedad_años BETWEEN 5 AND 10 THEN '5-10 años'
        ELSE '> 10 años'
    END as rango_antiguedad,
    COUNT(*) as num_empleados,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as porcentaje
FROM master.employee_metrics
WHERE estado_laboral = 'Activo'
GROUP BY rango_antiguedad
ORDER BY MIN(antiguedad_años);


-- ============================================
-- 10. SCORE DE ENGAGEMENT POR EQUIPO
-- ============================================
-- Identifica equipos con bajo clima laboral

SELECT 
    e.supervisor_id,
    s.nombre_completo as supervisor,
    COUNT(e.employee_id) as tamaño_equipo,
    ROUND(AVG(e.satisfaction_score), 2) as satisfaction_promedio,
    ROUND(AVG(e.work_life_balance), 2) as wlb_promedio,
    ROUND(AVG(e.turnover_risk_score), 3) as riesgo_promedio
FROM master.employee_metrics e
JOIN master.employee_metrics s ON e.supervisor_id = s.employee_id
WHERE e.estado_laboral = 'Activo'
  AND e.supervisor_id IS NOT NULL
GROUP BY e.supervisor_id, s.nombre_completo
HAVING COUNT(e.employee_id) >= 5  -- Equipos con al menos 5 personas
ORDER BY satisfaction_promedio ASC
LIMIT 20;

-- ⚠️ Equipos con satisfaction < 3.5 requieren intervención


-- ============================================
-- NOTAS DE USO:
-- - Estas queries asumen tablas Parquet en master layer
-- - Compatible con Spark SQL, Presto, Athena
-- - Para Power BI: Usar DirectQuery o importar resultados
-- ============================================
