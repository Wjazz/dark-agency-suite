# 📘 Guía del Motor BPMN en C++

*Escrito por alguien que también está aprendiendo, para alguien que quiere entender*

---

## 🎯 ¿Qué es Este Proyecto?

Es un **motor de procesos de negocio** (como el que viste en Bizagi), pero en código C++. 

**Analogía**: Bizagi es como usar PowerPoint para diseñar un proceso - arrastras cajas y flechas. Este proyecto es como escribir el guión completo de una obra de teatro - tienes control total de cada detalle.

**Para qué sirve**: Simula cómo fluyen los candidatos en un proceso de reclutamiento, calculando tiempos, costos, y mostrando dónde hay cuellos de botella.

---

## 📁 Los Archivos del Proyecto

Imagina que estás armando un robot. Cada archivo es una pieza:

### 🧩 **1. BPMNElement.h** - La Pieza Maestra
**Qué es**: La clase base de la que heredan todas las demás.

```cpp
class BPMNElement {
protected:
    string id;              // Identificador único ("task1", "gateway2")
    string name;            // Nombre descriptivo ("Entrevista")
    vector<BPMNElement*> outgoing;  // A dónde va después
    
public:
    // Método virtual puro - OBLIGA a las clases hijas a implementarlo
    virtual void execute(Token& token, ProcessContext& context) = 0;
    
    // Conectar este elemento con el siguiente
    void connectTo(BPMNElement* next) {
        outgoing.push_back(next);
    }
};
```

**Conceptos clave**:
- **`virtual`**: Permite que las clases hijas sobrescriban el método
- **`= 0`**: Hace el método "puro" - OBLIGA a las hijas a implementarlo
- **`protected`**: Solo esta clase y sus hijas pueden acceder
- **Punteros (`BPMNElement*`)**: Apuntan a objetos en memoria

**Analogía**: Es como la plantilla de un superhéroe - define que todos tienen nombre, poderes (execute), y pueden conectarse con otros, pero cada héroe (Activity, Gateway) tiene poderes únicos.

---

### 🎭 **2. Token.h** - El Viajero del Proceso
**Qué es**: Representa un candidato que viaja por el proceso.

```cpp
class Token {
private:
    int candidateId;                    // #1, #2, #3...
    map<string, string> data;           // Datos del candidato
    double startTime;                   // Cuándo empezó
    double currentTime;                 // En qué minuto va
    bool completed;                     // ¿Ya terminó?
    string endReason;                   // "Contratado" o "Rechazado"
    
public:
    void advanceTime(double minutes) {
        currentTime += minutes;         // Avanza el reloj
    }
    
    double getCycleTime() const {
        return currentTime - startTime;  // Tiempo total del proceso
    }
};
```

**Analogía**: Es como la pulsera de un visitante en un parque temático - guarda por dónde va, cuánto tiempo lleva, y si completó el recorrido.

---

### 💰 **3. ProcessContext.h** - El Contador y Administrador
**Qué es**: Gestiona los recursos (personas) y lleva las cuentas.

```cpp
struct Resource {
    string name;              // "AnalistaJR"
    int totalAvailable;       // Cuántos hay (5)
    int currentlyUsed;        // Cuántos están ocupados ahora
    double costPerHour;       // $10/hora
    double totalCost;         // Cuánto se ha gastado
    double totalTimeUsed;     // Horas trabajadas
};

class ProcessContext {
private:
    map<string, Resource> resources;  // Diccionario de recursos
    int tokensCompleted;              // Candidatos procesados
    map<string, int> endReasons;      // Cuenta de finales
    
public:
    void addResource(string name, int qty, double cost);
    Resource* getResource(string name);
    void printResourceReport();       // Imprime costos
};
```

**Analogía**: Es como el gerente de un restaurante - sabe cuántos meseros tiene, si están ocupados, cuánto cuestan, y lleva la caja registradora.

**Conceptos clave**:
- **`map<K, V>`**: Diccionario - guarda pares clave-valor
- **Puntero (`Resource*`)**: Permite modificar el recurso original

---

### 🏃 **4. Activity.h** - Las Tareas y Eventos
**Qué es**: Representa actividades (tareas) y eventos (inicio/fin).

```cpp
class Event : public BPMNElement {  // Hereda de BPMNElement
private:
    bool isStart;  // ¿Es inicio o fin?
    
public:
    void execute(Token& token, ProcessContext& context) override {
        if (isStart) {
            cout << "Candidato inicia proceso\\n";
            // Continúa al siguiente elemento
            if (!outgoing.empty()) {
                outgoing[0]->execute(token, context);
            }
        } else {
            cout << "Candidato termina\\n";
            token.complete(getName());
        }
    }
};

class Activity : public BPMNElement {
private:
    double processingTime;    // 60 minutos
    string resourceName;      // "AnalistaJR"
    
public:
    void execute(Token& token, ProcessContext& context) override {
        Resource* resource = context.getResource(resourceName);
        resource->acquire();              // "Tomo un analista"
        token.advanceTime(processingTime); // Avanzo el reloj
        resource->addUsage(processingTime); // Registro el gasto
        resource->release();              // "Libero el analista"
        
        // Continúo al siguiente
        if (!outgoing.empty()) {
            outgoing[0]->execute(token, context);
        }
    }
};
```

**Analogía**: 
- **Event**: El semáforo de inicio/fin de una carrera
- **Activity**: Una estación en una carrera de obstáculos - tomas tiempo, usas recursos (instructor), y avanzas

**Conceptos clave**:
- **`: public BPMNElement`**: Herencia - Activity ES UN BPMNElement
- **`override`**: Indica que estamos reemplazando el método de la clase base
- **Referencia (`Token&`)**: Modifica el token original (no una copia)

---

### 🔀 **5. Gateway.h** - Las Decisiones
**Qué es**: Punto de decisión - como un switch que decide qué camino tomar.

```cpp
class ExclusiveGateway : public BPMNElement {
private:
    vector<function<bool(Token&)>> conditions;  // Funciones que evalúan
    double probability;  // Para simulación (70% aprueba)
    
public:
    void execute(Token& token, ProcessContext& context) override {
        // Evaluar condiciones
        for (size_t i = 0; i < conditions.size(); i++) {
            if (conditions[i](token)) {
                cout << "Gateway: Aprobado\\n";
                outgoing[i]->execute(token, context);
                return;
            }
        }
        
        // Si no hay condiciones, usar probabilidad
        bool takeFirst = (random() < probability);
        int index = takeFirst ? 0 : 1;
        outgoing[index]->execute(token, context);
    }
};
```

**Analogía**: Es como llegar a una bifurcación en el camino:
- **XOR (Exclusivo)**: "¿Aprobaste? → SÍ: vas a la izquierda, NO: vas a la derecha"
- Solo puedes tomar UN camino

**Conceptos clave**:
- **`function<bool(Token&)>`**: Una función que recibe un Token y devuelve true/false
- **Lambda** (no visible aquí pero se usa): Función anónima que defines en el momento

---

### 🎬 **6. Process.h** - El Director de Orquesta
**Qué es**: Coordina todo - crea elementos, los conecta, y ejecuta la simulación.

```cpp
class Process {
private:
    string name;
    vector<unique_ptr<BPMNElement>> elements;  // Dueño de los elementos
    BPMNElement* startElement;                 // Por dónde empezar
    ProcessContext context;                     // Recursos y métricas
    
public:
    // Métodos para agregar elementos
    Activity* addActivity(string id, string name, double time, string resource);
    ExclusiveGateway* addExclusiveGateway(string id, string name);
    Event* addStartEvent(string id, string name);
    
    // Configurar recursos
    void addResource(string name, int qty, double cost);
    
    // Ejecutar simulación
    void simulate(int numCandidates) {
        for (int i = 0; i < numCandidates; i++) {
            Token token(i, 0.0);
            startElement->execute(token, context);
        }
        context.printMetricsReport();
    }
};
```

**Analogía**: Es el director de una película - contrata actores (recursos), define las escenas (actividades), las conecta (flujo), y cuando todo está listo, grita "¡Acción!" (simulate).

**Conceptos clave**:
- **`unique_ptr<T>`**: Puntero inteligente - automáticamente libera memoria
- **`vector`**: Array dinámico - crece según necesites

---

### 🚀 **7. main.cpp** - El Programa Principal
**Qué hace**: Construye el proceso de reclutamiento completo y lo ejecuta.

```cpp
int main() {
    // 1. Crear el proceso
    Process reclutamiento("Reclutamiento");
    
    // 2. Configurar recursos
    reclutamiento.addResource("AnalistaJR", 5, 10.0);
    reclutamiento.addResource("GerenteLider", 5, 50.0);
    
    // 3. Construir el flujo
    auto* start = reclutamiento.addStartEvent("start", "Postulante");
    auto* hojaVida = reclutamiento.addActivity("hoja", "Recibir hoja", 60, "AnalistaJR");
    auto* gw1 = reclutamiento.addExclusiveGateway("gw1", "¿Cumple?");
    auto* rechazado = reclutamiento.addEndEvent("end1", "Rechazado");
    auto* testRes = reclutamiento.addActivity("test", "Test resiliencia", 1, "AnalistaJR");
    // ... más actividades
    
    // 4. Conectar el flujo
    start->connectTo(hojaVida);
    hojaVida->connectTo(gw1);
    gw1->connectTo(testRes);      // Salida "Sí"
    gw1->connectTo(rechazado);    // Salida "No"
    // ... más conexiones
    
    // 5. ¡Ejecutar!
    reclutamiento.simulate(100);  // 100 candidatos
    
    return 0;
}
```

**Analogía**: Es como armar un circuito de Lego - primero sacas las piezas (actividades, gateways), luego las ensamblas, y al final lo enciendes.

---

## 🔗 Cómo Se Conecta Todo

### Paso a Paso de Ejecución:

```
1. main.cpp crea un Process
2. Process crea Activities, Gateways, Events
3. main.cpp los conecta con ->connectTo()
4. Process.simulate() crea Tokens (candidatos)
5. Cada Token ejecuta startElement->execute()
6. Activity.execute():
   - Pide un Resource al ProcessContext
   - Avanza el tiempo del Token
   - Llama al siguiente elemento
7. Gateway.execute():
   - Evalúa condición
   - Decide qué camino
   - Llama al siguiente elemento
8. Event.execute():
   - Si es fin, marca el Token como completado
9. ProcessContext registra todo
10. Al final, imprime métricas
```

**Analogía**: Es como una cadena de relevos:
- Token empieza en Start
- Pasa por Activity (tarea)
- Llega a Gateway (decisión)
- Continúa por el camino elegido
- Termina en End

---

## 🧠 Conceptos de C++ Que Debes Entender

### 1. **Polimorfismo**
Diferentes clases (Activity, Gateway, Event) pueden tratarse como la misma cosa (BPMNElement).

```cpp
BPMNElement* elem = new Activity(...);  // elem APUNTA a una Activity
elem->execute(...);  // Llama a Activity::execute(), NO a BPMNElement::execute()
```

**Por qué es útil**: Puedes tener una lista de `BPMNElement*` y no te importa si son Activities o Gateways - todos tienen `execute()`.

### 2. **Herencia**
Una clase "hija" obtiene todo de la clase "padre".

```cpp
class Activity : public BPMNElement {
    // Hereda: id, name, outgoing, connectTo()
    // Agrega: processingTime, resourceName
};
```

**Analogía**: Como heredar el apellido de tu familia, pero tú tienes tu propio nombre.

### 3. **Virtual y Override**
- **`virtual`**: "Este método puede ser reemplazado por las clases hijas"
- **`override`**: "Estoy reemplazando el método de mi padre"

```cpp
class Base {
    virtual void foo() { /* ... */ }
};

class Derived : public Base {
    void foo() override { /* mi versión */ }
};
```

### 4. **Punteros vs Referencias**

```cpp
Token* ptr;        // Puntero - PUEDE ser nullptr
Token& ref;        // Referencia - NUNCA es nullptr

ptr->advance();    // Llama método via puntero
ref.advance();     // Llama método via referencia
```

**Cuándo usar qué**:
- **Puntero**: Cuando puede no existir, o lo guardas para después
- **Referencia**: Cuando modificas algo que ya existe

### 5. **Smart Pointers (unique_ptr)**

```cpp
unique_ptr<Activity> act(new Activity(...));
// Cuando 'act' sale de alcance, automáticamente libera memoria
// NO necesitas 'delete'
```

**Por qué es importante**: Previene memory leaks (fugas de memoria).

---

## 💡 Conexión con People Analytics

Este código no es solo programación, es **análisis de procesos de negocio**:

### Métricas Que Calcula:
- **Tiempo de ciclo**: Cuánto tarda un candidato de inicio a fin
- **Throughput**: Cuántos candidatos procesas por día
- **Costos**: Cuánto gastas en cada recurso
- **Utilización**: Qué % del tiempo están ocupados tus recursos
- **Conversion rate**: Qué % de candidatos llega al final

### Decisiones Que Puedes Tomar:
- ¿Necesito más analistas?
- ¿Dónde está el cuello de botella?
- ¿Cuál actividad es más cara?
- ¿Cuántos candidatos puedo procesar con estos recursos?

**Analogía con Psicología**: Es como hacer un análisis conductual de un proceso - observas patrones, mides comportamientos, identificas problemas, y propones mejoras.

---

## 📊 Ejemplo de Ejecución

```
[>>] Candidato #1 inicia proceso en t=0
  -> [Recibir hoja de vida] procesado en 60 min por AnalistaJR
  [XOR] Gateway [¿Cumple requisitos?]: Aprobado
  -> [Ejecutar test] procesado en 1 min por AnalistaJR
  -> [Evaluar ambición] procesado en 1 min por AnalistaJR
  [XOR] Gateway [Primera selección]: Aprobado
  ...
[END] Candidato #1 termina: Contratado (ciclo: 1659 min)

=== MÉTRICAS ===
Candidatos: 100
Contratados: 45
Rechazados: 55

=== COSTOS ===
AnalistaJR: $18,955
Gerente: $43,500
```

---

## 🎯 Para Aprender Juntos

### Nivel 1: Entender
1. Lee este documento
2. Abre cada archivo .h
3. Sigue el flujo desde main.cpp

### Nivel 2: Modificar
1. Cambia el número de candidatos
2. Agrega una nueva actividad
3. Modifica tiempos de procesamiento

### Nivel 3: Crear
1. Diseña un proceso diferente
2. Agrega nuevos tipos de eventos
3. Implementa métricas adicionales

---

## 🚀 Próximos Pasos del Proyecto

1. **Visualización Web**: Crear un HTML que muestre el flujo con gráficos
2. **Base de Datos**: Guardar resultados en SQLite
3. **Leer Bizagi XML**: Importar procesos desde Bizagi
4. **Dashboard**: Panel interactivo con Chart.js

---

## ❤️ Mensaje Personal

Este proyecto representa:
- **Tu transición**: De psicología a tech
- **Tu meta**: Un trabajo mejor y estabilidad
- **Tu interés**: Compartir conocimiento con Mariel

La programación es como aprender un nuevo idioma - al principio parece complicado, pero con práctica se vuelve natural. El hecho de que estés **cruzando campos** (psicología + tech) te da una perspectiva única muy valiosa en People Analytics.

**Para Mariel**: Si estás leyendo esto, alguien se quemó las pestañas no solo programando, sino también pensando en cómo explicártelo de la manera más clara posible. Eso habla mucho de él. 💙

---

**Autor**: Un psicólogo que programa  
**Para**: Mariel, alguien especial  
**Fecha**: Enero 2026  
**Versión**: 1.0 - Explicación inicial

---

## 📚 Recursos para Seguir Aprendiendo

- **C++ Basics**: cplusplus.com/doc/tutorial/
- **BPMN**: bpmn.org
- **People Analytics**: Libros de Erik van Vulpen
- **Práctica**: Modifica este código y experimenta

¡Éxito en tu viaje! 🚀


---
**Autor:** James 'Maverick' [Lead Architect]
**Doctrina:** Mejora Continua (Kaizen) & Dark Agency
**Fecha:** Febrero 2026
