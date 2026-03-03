# Motor BPMN en C++ - Proceso de Reclutamiento

## 🎯 Descripción

Motor BPMN educativo implementado en C++ que simula el proceso de reclutamiento y selección de personal. 
Complementa el trabajo realizado en Bizagi Modeler, demostrando que BPMN puede modelarse tanto gráficamente como en código.

## 🏗️ Arquitectura

### Jerarquía de Clases (Polimorfismo)

```
BPMNElement (base abstracta)
├── Event (StartEvent, EndEvent)
├── Activity (tareas con tiempo y recursos)
└── Gateway
    ├── ExclusiveGateway (XOR - solo una ruta)
    └── ParallelGateway (AND - todas las rutas)
```

### Componentes Principales

- **BPMNElement.h:** Clase base con métodos virtuales
- **Activity.h:** Actividades y eventos
- **Gateway.h:** Compuertas de decisión y paralelismo
- **Process.h:** Orquestador del proceso completo
- **Token.h:** Representa una instancia (candidato) en ejecución
- **ProcessContext.h:** Gestiona recursos, métricas y simulación

## 📊 Proceso Modelado

El proceso implementado incluye:

### Lane RECLUTAMIENTO:
1. Recibir hoja de vida (60 min)
2. Gateway XOR: ¿Cumple requisitos? (85% aprobación)
   - NO → Rechazado
   - SÍ → Continuar

### Lane SELECCIÓN:
3. Ejecutar test de resiliencia (1 min)
4. Evaluar ambición (1 min)
5. Gateway XOR: Primera selección (60% aprobación)
   - NO → Rechazado
   - SÍ → Continuar
6. Entrevistas psicotécnicas (30 min)
7. Evaluación 360 (60 min)
8. Entrevista final (60 min)  
9. Gateway XOR: ¿Aprobó entrevista? (70% aprobación)
   - NO → Gateway ¿Segunda oportunidad?
   - SÍ → Continuar

### Lane BÚSQUEDA/CONTRATACIÓN:
10. Inducción (6 días = 2,520 min)
11. Assessment Center (4 horas = 240 min) - GERENTE
12. Gateway XOR: ¿Aceptó oferta? (90% aprobación)
    - NO → No aceptó oferta
    - SÍ → Continuar
13. Verificación de antecedentes (3 días = 1,260 min) - GERENTE
14. Contratación del agente (30 min)
15. END: Contratado exitosamente

## 💰 Recursos Configurados

- **Analista JR:** 5 personas, $10/hora
- **Gerente Líder:** 5 personas, $50/hora

## 🚀 Compilación y Ejecución

```bash
# Compilar
g++ -std=c++17 main.cpp -o bpmn_sim.exe

# Ejecutar
.\bpmn_sim.exe

# O guardar output en archivo
.\bpmn_sim.exe > resultado.txt
```

## 📈 Métricas Recolectadas

El motor calcula automáticamente:

- ✅ **Tiempo de ciclo promedio** por candidato
- ✅ **Throughput** (candidatos procesados)
- ✅ **Conversion rates** (% que pasa cada etapa)
- ✅ **Costos por rol** (Analista vs Gerente)
- ✅ **Utilización de recursos** (% de uso)
- ✅ **Distribución de rechazos** por fase

## 🎓 Ejemplo de Salida

```
================================================
  SIMULACION: Proceso de Reclutamiento y Selección
  Candidatos: 100
================================================

=== METRICAS DEL PROCESO ===
Candidatos iniciados: 100
Candidatos completados: 100

Resultados por razón:
  Contratado exitosamente: 45 (45%)
  Rechazado - No cumple perfil: 15 (15%)
  Rechazado - No superó evaluaciones: 24 (24%)
  ... (otros finales)

=== REPORTE DE RECURSOS ===

Recurso: AnalistaJR
  Disponibles: 5
  Tiempo usado: 1895.53 horas
  Costo total: $18,955.30
  Utilización promedio: 0%

Recurso: GerenteLider
  Disponibles: 5
  Tiempo usado: 870 horas
  Costo total: $43,500.00
  Utilización promedio: 0%

=== TIEMPO DE CICLO ===
Promedio: 1659.32 minutos (27.66 horas)
 (3.95 días laborables)
```

## 💡 Comparación: Código vs Bizagi

| Aspecto | Bizagi (Gráfico) | Código (C++) |
|---------|------------------|-------------|
| Diseño inicial | ⭐⭐⭐⭐⭐ Rápido y visual | ⭐⭐⭐ Más lento |
| Lógica compleja | ⭐⭐⭐ Limitada | ⭐⭐⭐⭐⭐ Total control |
| Versionar cambios | ⭐⭐ XML complejo | ⭐⭐⭐⭐⭐ Git nativo |
| Testing | ⭐⭐⭐ Simulación visual | ⭐⭐⭐⭐⭐ Unit tests |
| Integración | ⭐⭐⭐ APIs limitadas | ⭐⭐⭐⭐⭐ Total libertad |
| Curva de aprendizaje | ⭐⭐⭐⭐ Fácil | ⭐⭐ Requiere OOP |

## 🎯 Para People Analytics

Este proyecto demuestra:

1. **Modelado de procesos** en 2 paradigmas (visual + código)
2. **Simulación y métricas** automatizadas
3. **Análisis de capacidad** (Theory of Constraints)
4. **Optimización de recursos** (costos, tiempos, throughput)
5. **Programación orientada a objetos** aplicada a procesos de negocio

## 📚 Conceptos Aplicados

- ✅ Polimorfismo (clase base `BPMNElement`)
- ✅ Herencia (Event, Activity, Gateway)
- ✅ Encapsulación (Token, ProcessContext)
- ✅ Punteros y referencias
- ✅ STL (vector, map, unique_ptr)
- ✅ Funciones lambda (para condiciones de gateways)

## 🔄 Próximas Mejoras

- [ ] Implementar simulación con tiempo discreto (event queue)
- [ ] Agregar subprocesos y eventos intermedios
- [ ] Exportar/importar desde BPMN 2.0 XML
- [ ] Dashboard web con métricas en tiempo real
- [ ] Integrar con base de datos para persistencia

## 👤 Autor

Creado como proyecto educativo para demostrar dominio en:
- BPMN (Business Process Model and Notation)
- People Analytics
- Programación Orientada a Objetos en C++
- Simulación de procesos de negocio

---

**Nota:** Este motor replica el diseño del proceso modelado en Bizagi Modeler, 
permitiendo ejecutar simulaciones reproducibles y parametrizables en código.
