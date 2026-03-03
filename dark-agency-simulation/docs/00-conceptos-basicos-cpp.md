# 🎓 Tutorial 00: Conceptos Básicos de C++ para la Simulación

Este tutorial te enseña los fundamentos de C++ que necesitas para entender el código de la simulación Dark Agency.

## 📚 Índice

1. [Estructura de un programa C++](#1-estructura-de-un-programa-c)
2. [Variables y tipos de datos](#2-variables-y-tipos-de-datos)
3. [Clases y objetos (OOP)](#3-clases-y-objetos-oop)
4. [Control de flujo](#4-control-de-flujo)
5. [Vectores y contenedores](#5-vectores-y-contenedores)
6. [Generación de números aleatorios](#6-generación-de-números-aleatorios)

---

## 1. Estructura de un Programa C++

```cpp
#include <iostream>  // Librería para entrada/salida
#include <vector>    // Librería para vectores dinámicos
#include <string>    // Librería para cadenas de texto

using namespace std; // Permite usar cout, cin sin "std::"

int main() {
    // Tu código aquí
    cout << "¡Hola, Mariel!" << endl;
    return 0;  // El programa terminó correctamente
}
```

**Conceptos clave:**
- `#include`: Importa librerías (como `import` en Python)
- `main()`: Punto de entrada del programa
- `cout`: Imprime en pantalla
- `endl`: Salto de línea

---

## 2. Variables y Tipos de Datos

### Tipos fundamentales

```cpp
// Números enteros
int ticks = 0;           // Contador de turnos
int innovation_score = 0; // EIB logrados

// Números decimales (personalidad)
float g_factor = 0.75;   // Factor G (antagonismo)
float s_agency = 0.82;   // Agencia Oscura
float energy = 100.0;    // Energía del agente

// Booleanos
bool is_alive = true;    // ¿El agente sigue activo?
bool reached_goal = false;

// Texto
string agent_type = "Dark Agent";
```

### En nuestra simulación:

| Variable | Tipo | Uso |
|----------|------|-----|
| `g_factor` | `float` | Nivel de antagonismo (0.0 - 1.0) |
| `s_agency` | `float` | Nivel de agencia oscura (0.0 - 1.0) |
| `psycap` | `float` | Capital psicológico (0.0 - 1.0) |
| `x, y` | `int` | Posición en el grid |
| `cwb_o_count` | `int` | Transgresiones organizacionales |

---

## 3. Clases y Objetos (OOP)

Las clases son "planos" para crear objetos. Un `Agent` en nuestra simulación es una clase.

### Definición de una clase

```cpp
class Agent {
private:
    // Atributos (datos internos del agente)
    float g_factor;
    float s_agency;
    float energy;
    int x, y;

public:
    // Constructor (crea un nuevo agente)
    Agent(float g, float s, int startX, int startY) {
        g_factor = g;
        s_agency = s;
        energy = 100.0;
        x = startX;
        y = startY;
    }

    // Métodos (acciones del agente)
    void move(int dx, int dy) {
        x += dx;
        y += dy;
        energy -= 1.0;  // Moverse cuesta energía
    }

    float getAgency() const {
        return s_agency;
    }

    bool isDarkAgent() const {
        return s_agency > 0.7 && g_factor < s_agency;
    }
};
```

### Usando la clase

```cpp
int main() {
    // Crear un Dark Agent
    Agent maria(0.3, 0.85, 0, 0);  // g=0.3, s_agency=0.85

    if (maria.isDarkAgent()) {
        cout << "María es una Dark Agent!" << endl;
        cout << "Su agencia oscura: " << maria.getAgency() << endl;
    }

    return 0;
}
```

---

## 4. Control de Flujo

### Condicionales (el "cerebro" del agente)

```cpp
// Esta es la lógica central de tu tesis en código
void Agent::decide(bool wall_ahead) {
    if (s_agency > 0.7 && g_factor < s_agency) {
        // Dark Agent: transgrede instrumentalmente
        breakRuleAndAdvance();
    }
    else if (g_factor > 0.7) {
        // Tóxico: sabotea sin propósito
        sabotage();
    }
    else {
        // Normal: espera permiso
        wait();
    }
}
```

**Explicación del mapeo tesis → código:**
- `s_agency > 0.7`: Umbral para considerar "alta agencia oscura"
- `g_factor < s_agency`: El agente es más estratégico que tóxico
- `g_factor > 0.7`: Predomina el antagonismo destructivo

### Bucles

```cpp
// El bucle principal de la simulación
for (int tick = 0; tick < MAX_TICKS; tick++) {
    // En cada turno, cada agente toma una decisión
    for (Agent& agent : agents) {
        agent.decide();
    }
    render();  // Mostrar el estado actual
}
```

---

## 5. Vectores y Contenedores

Los vectores son listas dinámicas que pueden crecer.

```cpp
#include <vector>

int main() {
    // Crear una población de agentes
    vector<Agent> population;

    // Agregar agentes
    for (int i = 0; i < 100; i++) {
        float g = randomFloat(0.0, 1.0);
        float s = randomFloat(0.0, 1.0);
        population.push_back(Agent(g, s, i % 10, i / 10));
    }

    // Iterar sobre todos los agentes
    for (Agent& agent : population) {
        agent.decide();
    }

    cout << "Población creada: " << population.size() << " agentes" << endl;
    return 0;
}
```

### El Grid como vector 2D

```cpp
// El tablero es una matriz de celdas
vector<vector<Cell>> grid(HEIGHT, vector<Cell>(WIDTH, Cell::EMPTY));

// Colocar un muro en (5, 3)
grid[3][5] = Cell::WALL;

// Verificar si hay muro adelante
if (grid[agent.y][agent.x + 1] == Cell::WALL) {
    // Hay una barrera burocrática
}
```

---

## 6. Generación de Números Aleatorios

Fundamental para simular la variabilidad de rasgos.

```cpp
#include <random>

class RandomGenerator {
private:
    mt19937 rng;  // Motor de números aleatorios

public:
    RandomGenerator() {
        random_device rd;
        rng.seed(rd());
    }

    // Generar float entre min y max
    float uniform(float min, float max) {
        uniform_real_distribution<float> dist(min, max);
        return dist(rng);
    }

    // Generar entero entre min y max
    int uniformInt(int min, int max) {
        uniform_int_distribution<int> dist(min, max);
        return dist(rng);
    }

    // Simular evento con probabilidad p
    bool chance(float p) {
        return uniform(0.0, 1.0) < p;
    }
};
```

### Uso en la simulación

```cpp
RandomGenerator rng;

// Crear agente con rasgos aleatorios
float g = rng.uniform(0.0, 1.0);
float s = rng.uniform(0.0, 1.0);
Agent newAgent(g, s, 0, 0);

// Simular detección de transgresión (20% probabilidad)
if (rng.chance(0.2)) {
    agent.penalize();
}
```

---

## 🎯 Ejercicio Práctico

Antes de ver el código completo, intenta entender este fragmento:

```cpp
void Agent::executeDecision(Decision d) {
    switch(d) {
        case BREAK_RULE_AND_ADVANCE:
            cwb_o_count++;
            energy -= RULE_BREAKING_COST;
            if (!rng.chance(detection_prob)) {
                move();
                if (reachedGoal()) innovation_score++;
            }
            break;
        case SABOTAGE_NO_ADVANCE:
            cwb_i_count++;
            damageNearbyAgents();
            break;
        case WAIT_FOR_PERMISSION:
            wait_time++;
            break;
    }
}
```

**Pregunta**: ¿Por qué `BREAK_RULE_AND_ADVANCE` incrementa `cwb_o_count` (transgresión organizacional) pero puede llevar a `innovation_score` (EIB)?

**Respuesta**: Porque la Agencia Oscura implica romper reglas burocráticas (CWB-O) como medio para innovar (EIB). Esta es exactamente la hipótesis H1b de tu tesis: S_Agency se asocia positivamente con CWB-O *y* con EIB, porque la transgresión es instrumental, no destructiva.

---

## 📖 Siguiente Tutorial

[01-teoria-dark-agency.md](./01-teoria-dark-agency.md) - Mapeo completo de la tesis a entidades de código

---

**Compilar y ejecutar (Fedora):**

```bash
g++ -std=c++17 -o test test.cpp
./test
```
