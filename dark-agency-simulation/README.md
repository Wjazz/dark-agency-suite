# Dark Agency in Institutional Voids

**Simulación basada en tesis de maestría**

Una simulación visual en C++ que demuestra cómo diferentes perfiles de personalidad navegan entornos organizacionales con vacíos institucionales.

## 🎯 Propósito

Esta simulación **traduce a código ejecutable** las hipótesis centrales de la tesis:

| Hipótesis | Descripción | Variable Dependiente |
|-----------|-------------|---------------------|
| **H1a** | S_Agency → EIB (+) | Innovación |
| **H1b** | S_Agency → CWB-O (+), CWB-I (neutral) | Transgresión selectiva |
| **H1c** | G → CWB (+), EIB (-) | Destrucción sin progreso |

## 🏃 Quick Start

```bash
# Compilar
make

# Ejecutar con visualización
make run

# Ejecutar en modo rápido (solo estadísticas)
make fast
```

## 📁 Estructura

```
dark-agency-simulation/
├── src/
│   ├── main.cpp          # Punto de entrada
│   ├── config.hpp        # Parámetros configurables
│   ├── cell.hpp          # Tipos de celda
│   ├── random.hpp        # Generador aleatorio
│   ├── grid.hpp          # Entorno (grid con muros)
│   ├── agent.hpp         # 🧠 Agentes (lógica central)
│   ├── statistics.hpp    # Métricas y correlaciones
│   └── simulation.hpp    # Orquestador principal
├── docs/
│   ├── 00-conceptos-basicos-cpp.md   # Tutorial C++
│   └── 01-teoria-dark-agency.md      # Mapeo tesis → código
├── data/                 # Configuraciones
├── output/               # Resultados exportados
├── Makefile              # Sistema de compilación
└── README.md
```

## 🧠 Los Tres Perfiles

### 🟢 Dark Agent (D)
- **Rasgos**: Alto S_Agency, G moderado
- **Comportamiento**: Calcula riesgo/beneficio, transgrede instrumentalmente
- **Resultado**: Alto EIB (innovación), CWB-O moderado, CWB-I bajo

### 🔴 Toxic Agent (T)
- **Rasgos**: Alto G
- **Comportamiento**: Destruye sin propósito, daña a colegas
- **Resultado**: Bajo EIB, alto CWB-I

### 🔵 Normal Agent (N)
- **Rasgos**: Bajo S_Agency, bajo G
- **Comportamiento**: Sigue reglas, espera permiso
- **Resultado**: Bajo EIB, bajo CWB

## 📊 Output

La simulación genera:

1. **Visualización en tiempo real** del grid con agentes
2. **Estadísticas por tipo** de agente (EIB, CWB-O, CWB-I)
3. **Validación de hipótesis** con correlaciones calculadas
4. **CSV exportado** para análisis en R/Python

```
═══════════════════════════════════════════════════════════
          VALIDACIÓN DE HIPÓTESIS - DARK AGENCY
═══════════════════════════════════════════════════════════

H1a: S_Agency predice EIB positivamente
     Correlación calculada: r = 0.73
     Hipótesis: CONFIRMADA ✓
```

## 🔧 Requisitos

- **Compilador**: g++ con soporte C++17
- **OS**: Linux (Fedora, Ubuntu) o WSL

```bash
# Fedora
sudo dnf install gcc-c++ make

# Ubuntu/Debian
sudo apt install g++ make
```

## 📚 Documentación

Ver carpeta `docs/` para:
- Tutorial de C++ adaptado al proyecto
- Mapeo detallado de constructos tesis → código

## 💬 Narrativa

> *"Mira el código. La mayoría de empresas (el `else`) se detienen ante el muro. Mis 'Dark Agents' (`if s_agency > 0.7`) son los únicos que cruzan. El código demuestra que sin ellos, la empresa se estanca. Matemáticamente, la rebeldía instrumentalmente calculada es rentabilidad."*

---

**Autor**: James  
**Tesis**: Dark Agency in Institutional Voids: Intrapreneurial Innovation and Bureaucratic Rule-Breaking in Service Organizations
