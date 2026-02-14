# 🧠 Tutorial 01: Mapeo Tesis → Código

Este documento explica cómo cada concepto de tu tesis se traduce a entidades ejecutables en el código.

---

## 📊 Tabla de Correspondencias

### Constructos Psicológicos → Variables

| Constructo Tesis | Variable C++ | Tipo | Rango | Descripción |
|-----------------|--------------|------|-------|-------------|
| G (Factor General Antagónico) | `g_factor` | float | 0.0-1.0 | Tendencia a conductas destructivas sin propósito productivo |
| S_Agency (Agencia Oscura) | `s_agency` | float | 0.0-1.0 | Capacidad de transgresión instrumental calculada |
| VEE (Vigilancia Estratégica) | `vigilance` | float | 0.0-1.0 | Habilidad para detectar oportunidades/vulnerabilidades |
| POPS (Percepción Política) | `perceived_politics` | float | 0.0-1.0 | Qué tan politizado percibe el entorno |
| PsyCap (Capital Psicológico) | `psycap` | float | 0.0-1.0 | Recursos internos para sostener riesgos |
| EIB (Intraemprendimiento) | `innovation_score` | int | 0-N | Contador de innovaciones logradas |
| CWB-O (Transgresión Org.) | `cwb_o_count` | int | 0-N | Reglas burocráticas violadas |
| CWB-I (Transgresión Inter.) | `cwb_i_count` | int | 0-N | Daños causados a otros agentes |

### Contexto Institucional → Entorno

| Concepto Tesis | Entidad Código | Implementación |
|----------------|----------------|----------------|
| Vacío Institucional | `Cell::WALL` | Barrera impasable por vía tradicional |
| Burocracia Normal | `Cell::EMPTY` | Espacio transitable (con costo) |
| Meta de Innovación | `Cell::GOAL` | Objetivo que genera `innovation_score` |
| Detección Selectiva | `detection_probability` | Probabilidad de ser "atrapado" al transgredir |

---

## 🎭 Los Tres Perfiles de Agente

### 1. Dark Agent (Alto S_Agency, G moderado)

```cpp
// Definición matemática en código
bool Agent::isDarkAgent() const {
    return s_agency > AGENCY_THRESHOLD &&   // Alta agencia oscura
           g_factor <= s_agency;             // Más estratégico que destructivo
}
```

**Características comportamentales:**
- Escanea el entorno buscando vulnerabilidades
- Calcula riesgo/beneficio antes de actuar
- Rompe reglas *para avanzar* (transgresión instrumental)
- Genera innovación (EIB) mientras acumula CWB-O
- CWB-I bajo (no daña a otros innecesariamente)

**Mapeo a H1a-b:**
```
S_Agency alta → EIB alto ✓ (H1a)
S_Agency alta → CWB-O moderado ✓ (H1b)
S_Agency alta → CWB-I bajo ✓ (H1b)
```

### 2. Agente Tóxico (Alto G)

```cpp
bool Agent::isToxic() const {
    return g_factor > G_THRESHOLD;  // Antagonismo dominante
}
```

**Características comportamentales:**
- No calcula, actúa impulsivamente
- Destruye por placer o frustración
- No avanza hacia metas productivas
- Alto CWB-I (daña a colegas)
- EIB bajo (no innova)

**Mapeo a H1c:**
```
G alto → EIB bajo ✓ (H1c)
G alto → CWB-O moderado ✓ (H1c)
G alto → CWB-I alto ✓ (H1c)
```

### 3. Agente Normal (Burocrático)

```cpp
bool Agent::isNormal() const {
    return s_agency <= AGENCY_THRESHOLD && 
           g_factor <= G_THRESHOLD;
}
```

**Características comportamentales:**
- Sigue las reglas
- Se detiene ante barreras
- Espera permiso para actuar
- CWB-O y CWB-I muy bajos
- EIB bajo (no toma riesgos)

---

## 🔄 El Algoritmo de Decisión

### Pseudocódigo conceptual (de tu tesis)

```
POR CADA tick de simulación:
    POR CADA agent en población:
        1. agent.scan(entorno)           // VEE
        2. decision = agent.decide()     // Evaluar opciones
        3. agent.execute(decision)       // Actuar
        4. simulation.updateStats()      // Registrar métricas
```

### Implementación C++ del Modelo H1-H3

```cpp
Decision Agent::decide() {
    // Escanear entorno (activación de VEE)
    float opportunity = scanForOpportunities();
    float threat = scanForThreats();
    
    // H3: POPS modera la relación S_Agency → VEE
    float effective_vigilance = vigilance * (1.0 + perceived_politics * 0.5);
    
    // Detectar obstáculo adelante
    Cell ahead = grid->getCell(x + dx, y + dy);
    
    if (ahead == Cell::WALL) {
        // HAY UNA BARRERA BUROCRÁTICA
        
        // ============================================
        // CASO 1: DARK AGENT
        // H1a-b: S_Agency → EIB (+) y CWB-O (+)
        // ============================================
        if (isDarkAgent()) {
            // Calcular riesgo/beneficio
            float benefit = goalDistance() < 5 ? 1.0 : 0.5;
            float risk = detection_probability * (1.0 - psycap);
            
            // H4: PsyCap modera la relación S_Agency → EIB
            if (benefit > risk) {
                return Decision::BREAK_RULE_AND_ADVANCE;
            }
        }
        
        // ============================================
        // CASO 2: AGENTE TÓXICO
        // H1c: G → CWB-I (+), EIB (-)
        // ============================================
        else if (isToxic()) {
            return Decision::SABOTAGE_NO_ADVANCE;
        }
        
        // ============================================
        // CASO 3: AGENTE NORMAL
        // Referencia para contrastar
        // ============================================
        else {
            return Decision::WAIT_FOR_PERMISSION;
        }
    }
    
    // Sin obstáculo: moverse normalmente
    return Decision::MOVE_FORWARD;
}
```

---

## 📈 Mediación: VEE como Mecanismo (H2)

Tu tesis propone que **VEE media** la relación entre S_Agency y EIB:

```
S_Agency → VEE → EIB
```

En código:

```cpp
float Agent::calculateInnovationPotential() {
    // H2: El efecto de S_Agency en EIB está mediado por VEE
    
    // Paso 1: S_Agency activa VEE
    float vee_activation = s_agency * vigilance;
    
    // Paso 2: VEE detecta oportunidades
    float opportunities_found = vee_activation * scanEnvironment();
    
    // Paso 3: Oportunidades llevan a EIB
    return opportunities_found;
}
```

**Interpretación:**
- Un agente puede tener alta S_Agency pero baja VEE → No detecta oportunidades → Bajo EIB
- La VEE "canaliza" la agencia oscura hacia resultados productivos

---

## 🎛️ Moderadores: POPS y PsyCap

### H3: POPS × S_Agency → VEE

```cpp
// POPS activa la expresión de S_Agency en forma de VEE
float Agent::getEffectiveVigilance() {
    // Sin política percibida, la agencia no se activa
    // Con alta política, el escaneo estratégico se intensifica
    float pops_moderation = 1.0 + (perceived_politics * s_agency);
    return vigilance * pops_moderation;
}
```

**Lógica:** En entornos donde "las reglas son letra muerta" (alta POPS), los Dark Agents *activan* su escaneo estratégico. En entornos justos y claros, no necesitan esta capacidad.

### H4: PsyCap × S_Agency → EIB

```cpp
// PsyCap sostiene la transgresión a largo plazo
float Agent::calculateRiskTolerance() {
    // Sin PsyCap, el agente colapsa ante el estrés
    // Con PsyCap, puede sostener riesgos
    return s_agency * psycap;
}

bool Agent::shouldTakeRisk() {
    float tolerance = calculateRiskTolerance();
    return tolerance > RISK_THRESHOLD;
}
```

**Lógica:** La Agencia Oscura *quiere* innovar, pero necesita PsyCap para *sostener* la transgresión sin colapsar emocionalmente.

---

## 📊 Perfil de "Desviación Constructiva" (H5 Exploratorio)

Tu tesis explora si existe un perfil identificable:

| Característica | Valor Esperado |
|---------------|----------------|
| S_Agency | Alta (>0.7) |
| G | Moderado (<0.5) |
| EIB | Alto |
| CWB-O | Moderado |
| CWB-I | Bajo |

En código:

```cpp
bool Agent::isConstructiveDeviant() const {
    return s_agency > 0.7 &&
           g_factor < 0.5 &&
           innovation_score > avg_innovation &&
           cwb_o_count > 0 &&        // Sí transgrede
           cwb_i_count < 2;          // Pero no daña a otros
}
```

**Este perfil es la evidencia empírica de tu hipótesis central.**

---

## 🔢 Fórmulas Matemáticas en Código

### Del modelo estructural (sección 2.9 de tu tesis)

```cpp
// VEE = α_0 + α_1*S_A + α_2*POPS + α_3*(S_A × POPS) + ε
float calculateVEE() {
    float alpha_0 = 0.1;   // Intercepto
    float alpha_1 = 0.4;   // Efecto directo de S_Agency
    float alpha_2 = 0.2;   // Efecto directo de POPS
    float alpha_3 = 0.3;   // Interacción S_Agency × POPS
    
    return alpha_0 + 
           alpha_1 * s_agency + 
           alpha_2 * perceived_politics + 
           alpha_3 * s_agency * perceived_politics +
           randomNoise();
}

// EIB = β_0 + β_1*S_A + β_2*G + β_3*VEE + β_4*PsyCap + β_5*(S_A × PsyCap) + ε
float calculateEIB() {
    float beta_0 = 0.0;
    float beta_1 = 0.3;   // S_Agency → EIB (+)
    float beta_2 = -0.2;  // G → EIB (-)
    float beta_3 = 0.4;   // VEE → EIB (+)
    float beta_4 = 0.2;   // PsyCap → EIB (+)
    float beta_5 = 0.15;  // Interacción S_Agency × PsyCap
    
    float vee = calculateVEE();
    
    return beta_0 +
           beta_1 * s_agency +
           beta_2 * g_factor +
           beta_3 * vee +
           beta_4 * psycap +
           beta_5 * s_agency * psycap +
           randomNoise();
}
```

---

## 🎬 Secuencia de Eventos en la Simulación

```
Tick 0: Inicialización
├── Crear grid con muros (vacíos institucionales)
├── Crear población (N=500 agentes con rasgos aleatorios)
└── ~15% Dark Agents, ~10% Tóxicos, ~75% Normales

Tick 1-5000: Bucle principal
├── Por cada agente:
│   ├── scan() → Activar VEE
│   ├── decide() → Elegir acción basada en perfil
│   ├── execute() → Realizar acción
│   └── updateStats() → Registrar EIB, CWB-O, CWB-I
├── Render grid
└── Mostrar estadísticas

Tick Final: Análisis
├── Calcular correlaciones
├── Validar hipótesis H1-H4
└── Identificar perfiles (H5)
```

---

## 📖 Siguiente Tutorial

[02-arquitectura-simulacion.md](./02-arquitectura-simulacion.md) - Diseño detallado de clases y sus interacciones

---

## 💬 Narrativa

> *"Mira este código. `isDarkAgent()` verifica si alguien tiene alta agencia oscura pero G moderado. Cuando encuentra un muro, no se detiene como el empleado promedio ni lo golpea sin sentido como el tóxico. Calcula. Evalúa. Y si el beneficio supera el riesgo, atraviesa. Eso es exactamente lo que mi tesis predice: la transgresión instrumental como motor de innovación. En 5000 ticks de simulación, los Dark Agents acumulan más EIB que cualquier otro perfil. Matemáticamente demostrado."*
