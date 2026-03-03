# DarkAgencyDetector

**Motor de Inferencia basado en Modelo Bifactor S-1**

Un sistema que **predice** comportamiento organizacional usando la teoría de Dark Agency.

## 🚀 Quick Start

```bash
cd ~/proyectos/dark-agency-detector

# Compilar y generar GIF
make gif

# O paso a paso:
make            # Compilar
make run        # Ejecutar con visualización
python3 scripts/make_gif.py   # Generar GIF
```

## 🧠 El Modelo

El Bifactor S-1 extrae dos factores latentes de la Tétrada Oscura:

| Factor | Componentes | Predicción |
|--------|-------------|------------|
| **G** | Psicopatía + Sadismo | CWB-I (daño interpersonal) |
| **S_Agency** | Narcisismo + Maquiavelismo - G | EIB (innovación) |

## 🎨 Clasificación de Agentes

| Color | Tipo | Perfil | Comportamiento |
|-------|------|--------|----------------|
| 🔵 Cyan | Dark Innovator | Alto S_Agency, Bajo G | Transgrede para innovar |
| 🟡 Amarillo | Maverick at Risk | Alto ambos | Transición, necesita intervención |
| 🔴 Rojo | Toxic | Alto G | Destruye sin propósito |
| ⚪ Azul | Normal | Bajo ambos | Sigue reglas |

## 📊 Output

- **GIF animado**: `output/dark_agency_simulation.gif`
- **Estadísticas**: `output/results.csv`
- **Validación de hipótesis**: Correlaciones H1a-c en terminal

## 📁 Estructura

```
dark-agency-detector/
├── src/
│   ├── main.cpp              # Punto de entrada
│   ├── bifactor_model.hpp    # 🧠 Modelo Bifactor S-1
│   ├── agent.hpp             # Agentes con decisión
│   ├── frame_exporter.hpp    # Exporta PPM para GIF
│   └── ...
├── scripts/
│   └── make_gif.py           # Genera GIF animado
├── frames/                   # Frames PPM
├── output/                   # Resultados
└── Makefile
```

## 💬 El Pitch

> *"Los puntos cian son los Dark Innovators. Rompen burocracia pero llegan a las metas, mientras los rojos destruyen sin avanzar. Mi tesis demostró que la rebeldía calculada es rentabilidad. Y lo programé en C++ para demostrarlo matemáticamente."*

---

**Basado en**: "Dark Agency in Institutional Voids: Intrapreneurial Innovation and Bureaucratic Rule-Breaking"
