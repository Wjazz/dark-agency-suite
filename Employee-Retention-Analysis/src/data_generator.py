"""
Generador de Dataset Sintético para Análisis de Rotación de Personal
======================================================================
Script para crear datos ficticios de empleados con variables predictivas
de rotación (turnover).

Autor: James Lalupu
Fecha: 2026-02-04
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuración de semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

# Configuración del dataset
N_EMPLOYEES = 1000  # Número de empleados a generar

print(f"🔄 Generando dataset de {N_EMPLOYEES} empleados...")

# ============================================
# 1. DATOS BÁSICOS
# ============================================

employee_ids = range(10000, 10000 + N_EMPLOYEES)

# Nombres ficticios (combinaciones aleatorias)
nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Patricia', 'Roberto', 'Carmen',
           'Jorge', 'Laura', 'Pedro', 'Rosa', 'Miguel', 'Elena', 'José', 'Sofía']
apellidos = ['García', 'Rodríguez', 'Martínez', 'López', 'Pérez', 'González', 'Sánchez',
             'Torres', 'Ramírez', 'Flores', 'Vargas', 'Castillo', 'Mendoza', 'Quispe']

nombres_completos = [f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}" 
                     for _ in range(N_EMPLOYEES)]

# Edad (distribución normal centrada en 32 años)
edades = np.random.normal(32, 8, N_EMPLOYEES).astype(int)
edades = np.clip(edades, 22, 65)  # Rango razonable

# Género (55% M, 45% F para reflejar desbalance típico)
generos = np.random.choice(['M', 'F'], N_EMPLOYEES, p=[0.55, 0.45])

# Estado civil
estado_civil = np.random.choice(['Soltero', 'Casado', 'Divorciado', 'Viudo'], 
                                N_EMPLOYEES, p=[0.35, 0.50, 0.12, 0.03])

# Número de hijos (relacionado con estado civil)
num_hijos = []
for ec in estado_civil:
    if ec == 'Soltero':
        hijos = np.random.choice([0, 1], p=[0.85, 0.15])
    elif ec == 'Casado':
        hijos = np.random.choice([0, 1, 2, 3], p=[0.15, 0.30, 0.40, 0.15])
    else:
        hijos = np.random.choice([0, 1, 2], p=[0.40, 0.40, 0.20])
    num_hijos.append(hijos)

# ============================================
# 2. DATOS LABORALES
# ============================================

# Departamentos (distribución realista)
departamentos = np.random.choice(
    ['Ventas', 'TI', 'Finanzas', 'RRHH', 'Operaciones', 'Marketing'],
    N_EMPLOYEES,
    p=[0.30, 0.20, 0.15, 0.10, 0.15, 0.10]
)

# Puestos por departamento
puestos = []
for dept in departamentos:
    if dept == 'Ventas':
        puesto = np.random.choice(['Ejecutivo de Ventas', 'Coordinador', 'Gerente'], p=[0.70, 0.20, 0.10])
    elif dept == 'TI':
        puesto = np.random.choice(['Desarrollador', 'Analista de Sistemas', 'Gerente TI'], p=[0.60, 0.30, 0.10])
    elif dept == 'Finanzas':
        puesto = np.random.choice(['Analista Financiero', 'Contador', 'Gerente'], p=[0.60, 0.30, 0.10])
    elif dept == 'RRHH':
        puesto = np.random.choice(['Asistente RRHH', 'Coordinador', 'Gerente'], p=[0.60, 0.30, 0.10])
    elif dept == 'Operaciones':
        puesto = np.random.choice(['Operario', 'Supervisor', 'Gerente'], p=[0.70, 0.20, 0.10])
    else:  # Marketing
        puesto = np.random.choice(['Especialista Marketing', 'Coordinador', 'Gerente'], p=[0.65, 0.25, 0.10])
    puestos.append(puesto)

# Fecha de ingreso (últimos 10 años con más peso en últimos 3 años)
fecha_actual = datetime(2026, 2, 4)
dias_atras = np.random.exponential(scale=800, size=N_EMPLOYEES).astype(int)
dias_atras = np.clip(dias_atras, 30, 3650)  # Mín 1 mes, máx 10 años
fechas_ingreso = [fecha_actual - timedelta(days=int(d)) for d in dias_atras]

# Antigüedad en años
antiguedad_años = [(fecha_actual - fi).days / 365.25 for fi in fechas_ingreso]

# Salario mensual (en soles peruanos, varía por puesto y antigüedad)
salarios = []
for i, puesto in enumerate(puestos):
    if 'Gerente' in puesto:
        base = np.random.uniform(10000, 15000)
    elif 'Coordinador' in puesto or 'Supervisor' in puesto:
        base = np.random.uniform(6000, 9000)
    elif 'Analista' in puesto or 'Desarrollador' in puesto or 'Contador' in puesto:
        base = np.random.uniform(4500, 7000)
    elif 'Especialista' in puesto:
        base = np.random.uniform(5000, 7500)
    else:
        base = np.random.uniform(2500, 5000)
    
    # Ajuste por antigüedad (+3% anual, hasta 30%)
    ajuste_antiguedad = min(antiguedad_años[i] * 0.03, 0.30)
    salario = base * (1 + ajuste_antiguedad)
    
    # Ruido aleatorio ±10%
    salario *= np.random.uniform(0.90, 1.10)
    
    salarios.append(round(salario, 2))

# ============================================
# 3. VARIABLES DE ENGAGEMENT Y DESEMPEÑO
# ============================================

# Satisfaction Score (1-5, distribución normal centrada en 3.5)
satisfaction_scores = np.random.normal(3.5, 0.8, N_EMPLOYEES)
satisfaction_scores = np.clip(satisfaction_scores, 1, 5)

# Performance Rating (1-5, distribución positivamente sesgada)
performance_ratings = np.random.beta(5, 2, N_EMPLOYEES) * 4 + 1
performance_ratings = np.clip(performance_ratings, 1, 5)

# Work-Life Balance (1-5)
work_life_balance = np.random.normal(3.3, 0.9, N_EMPLOYEES)
work_life_balance = np.clip(work_life_balance, 1, 5)

# Horas extra al mes
horas_extra_mes = np.random.exponential(scale=8, size=N_EMPLOYEES)
horas_extra_mes = np.clip(horas_extra_mes, 0, 60)

# Días de ausencia en último año
dias_ausencia_año = np.random.poisson(lam=5, size=N_EMPLOYEES)
dias_ausencia_año = np.clip(dias_ausencia_año, 0, 30)

# ============================================
# 4. VARIABLE TARGET: TURNOVER
# ============================================
# Modelamos la probabilidad de rotación basada en factores realistas

turnover_probs = []
for i in range(N_EMPLOYEES):
    prob = 0.15  # Probabilidad base 15%
    
    # Factor 1: Satisfaction (más importante)
    if satisfaction_scores[i] < 2.5:
        prob += 0.35
    elif satisfaction_scores[i] < 3.5:
        prob += 0.15
    
    # Factor 2: Salario bajo relativo a puesto
    salario_esperado = 6000 if 'Gerente' not in puestos[i] else 12000
    if salarios[i] < salario_esperado * 0.8:
        prob += 0.20
    
    # Factor 3: Work-Life Balance
    if work_life_balance[i] < 2.5:
        prob += 0.15
    
    # Factor 4: Horas extra excesivas
    if horas_extra_mes[i] > 30:
        prob += 0.10
    
    # Factor 5: Antigüedad (efecto U: muy nuevos o muy antiguos tienden a irse)
    if antiguedad_años[i] < 1:
        prob += 0.20  # Newbies no se adaptan
    elif antiguedad_años[i] > 7:
        prob += 0.10  # Buscan nuevos retos
    
    # Factor 6: Performance bajo
    if performance_ratings[i] < 2.5:
        prob += 0.15  # Riesgo de despido o deserción
    
    turnover_probs.append(min(prob, 0.95))  # Cap en 95%

# Generar variable binaria turnover basada en probabilidades
turnover = [1 if np.random.random() < p else 0 for p in turnover_probs]

print(f"✅ Tasa de rotación generada: {sum(turnover)/len(turnover)*100:.2f}%")

# ============================================
# 5. CREAR DATAFRAME
# ============================================

df = pd.DataFrame({
    'employee_id': employee_ids,
    'nombre_completo': nombres_completos,
    'edad': edades,
    'genero': generos,
    'estado_civil': estado_civil,
    'num_hijos': num_hijos,
    'departamento': departamentos,
    'puesto': puestos,
    'fecha_ingreso': [fi.strftime('%Y-%m-%d') for fi in fechas_ingreso],
    'antiguedad_años': [round(a, 2) for a in antiguedad_años],
    'salario_mensual': salarios,
    'satisfaction_score': [round(s, 2) for s in satisfaction_scores],
    'performance_rating': [round(p, 2) for p in performance_ratings],
    'work_life_balance': [round(w, 2) for w in work_life_balance],
    'horas_extra_mes': [round(h, 1) for h in horas_extra_mes],
    'dias_ausencia_año': dias_ausencia_año,
    'turnover': turnover
})

# ============================================
# 6. GUARDAR DATASET
# ============================================

output_path = 'data/employees_synthetic.csv'
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"💾 Dataset guardado en: {output_path}")
print(f"\n📊 Resumen del Dataset:")
print(f"  - Total empleados: {len(df)}")
print(f"  - Empleados activos: {len(df[df.turnover == 0])} ({len(df[df.turnover == 0])/len(df)*100:.1f}%)")
print(f"  - Empleados que renunciaron: {len(df[df.turnover == 1])} ({len(df[df.turnover == 1])/len(df)*100:.1f}%)")
print(f"  - Salario promedio: S/ {df.salario_mensual.mean():.2f}")
print(f"  - Antigüedad promedio: {df['antiguedad_años'].mean():.2f} años")
print(f"\n✅ Dataset generado exitosamente!")
