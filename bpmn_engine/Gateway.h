#ifndef GATEWAY_H
#define GATEWAY_H

#include "BPMNElement.h"
#include "Token.h"
#include "ProcessContext.h"
#include <functional>
#include <random>
#include <iostream>
#include <string>
#include <vector>

/**
 * Gateway Exclusivo (XOR) - Solo una salida se ejecuta
 * Motor de Reglas de Negocio: Evalúa condiciones en orden (if-else if pattern)
 */
class ExclusiveGateway : public BPMNElement {
private:
    /**
     * Estructura que representa una regla de negocio
     * Similar a una regla visual en Kissflow, pero en código
     */
    struct Rule {
        std::string name;                            // Nombre descriptivo de la regla
        std::function<bool(const Token&)> condition; // Lambda que evalúa el Token
        BPMNElement* nextNode;                       // Nodo destino si la condición es true
    };
    
    std::vector<Rule> rules;        // Lista de reglas a evaluar en orden
    BPMNElement* defaultFlow;       // Camino "else" si ninguna regla se cumple

public:
    /**
     * Constructor: Ya no necesita probabilidad, usa reglas explícitas
     */
    ExclusiveGateway(const std::string& id, const std::string& name) 
        : BPMNElement(id, name), defaultFlow(nullptr) {}
    
    /**
     * Agregar una regla de negocio (como configurar una regla en Kissflow)
     * 
     * @param ruleName Nombre descriptivo de la regla (ej. "Shadow Agent Detected")
     * @param target Nodo BPMN al que ir si la condición es verdadera
     * @param condition Lambda que evalúa el Token y devuelve bool
     * 
     * Ejemplo:
     *   gateway->addPath("Salario Alto", nodoGerencia, [](const Token& t) {
     *       return std::stod(t.getData("salaryExpectation")) > 8000.0;
     *   });
     */
    void addPath(const std::string& ruleName, 
                 BPMNElement* target, 
                 std::function<bool(const Token&)> condition) {
        // Validar función
        if (!condition) {
            std::cerr << "[ERROR] Condición nula en regla '" << ruleName 
                      << "' del gateway '" << name << "'\n";
            return;
        }
        
        // Validar nodo destino
        if (!target) {
            std::cerr << "[ERROR] Nodo destino nulo en regla '" << ruleName 
                      << "' del gateway '" << name << "'\n";
            return;
        }
        
        // Agregar regla
        rules.push_back({ruleName, condition, target});
        
        // Mantener el grafo de conexiones (para navegación)
        connectTo(target);
    }
    
    /**
     * Establecer el camino por defecto (ELSE)
     * Se ejecuta si ninguna regla se cumple
     * 
     * @param target Nodo BPMN para el camino por defecto
     */
    void setDefaultPath(BPMNElement* target) {
        if (!target) {
            std::cerr << "[ERROR] Nodo por defecto nulo en gateway '" << name << "'\n";
            return;
        }
        
        defaultFlow = target;
        connectTo(target);
    }
    
    /**
     * Ejecutar el gateway: Evalúa las reglas en orden (if-else if-else)
     * 
     * Flujo de evaluación:
     * 1. Por cada regla, evaluar condición con el Token
     * 2. Si una condición es true, ejecutar ese camino y terminar
     * 3. Si ninguna es true, tomar el camino por defecto
     * 4. Si no hay camino por defecto, reportar error
     */
    void execute(Token& token, ProcessContext& context) override {
        // Evaluar reglas en orden (patrón if-else if)
        for (const auto& rule : rules) {
            // Aquí es donde el motor "mira" dentro del Token
            if (rule.condition(token)) {
                std::cout << "  [XOR] Gateway [" << name << "]: " 
                          << rule.name << "\n";
                
                // Ejecutar el camino correspondiente
                rule.nextNode->execute(token, context);
                return; // Importante: solo un camino se ejecuta (XOR)
            }
        }
        
        // Si ninguna regla se cumplió, tomar camino por defecto
        if (defaultFlow) {
            std::cout << "  [XOR] Gateway [" << name << "]: (Default Path)\n";
            defaultFlow->execute(token, context);
            return;
        }
        
        // Error: Token atrapado sin salida
        std::cerr << "[ERROR] Token #" << token.getCandidateId() 
                  << " sin salida válida en Gateway '" << name << "'\n";
        std::cerr << "  Sugerencia: Agrega un setDefaultPath() para manejar casos no contemplados\n";
    }
    
    std::string getType() const override { return "ExclusiveGateway"; }
};

/**
 * Gateway Paralelo (AND) - Todas las salidas se ejecutan simultáneamente
 */
class ParallelGateway : public BPMNElement {
private:
    bool isDivergence; // true = divide, false = merge
    
public:
    ParallelGateway(const std::string& id, const std::string& name, bool diverge = true) 
        : BPMNElement(id, name), isDivergence(diverge) {}
    
    void execute(Token& token, ProcessContext& context) override {
        if (isDivergence) {
            std::cout << "  [AND+] Gateway Paralelo [" << name << "]: Dividiendo en " 
                     << outgoing.size() << " ramas\n";
            // Ejecutar todas las salidas en paralelo
            for (auto* next : outgoing) {
                // En una simulación real, crearíamos tokens separados
                // Por simplicidad, ejecutamos secuencialmente
                next->execute(token, context);
            }
        } else {
            std::cout << "  [AND] Gateway Paralelo [" << name << "]: Sincronizando ramas\n";
            // En convergencia, esperamos a que lleguen todos los tokens
            // Por simplicidad, continuamos con el siguiente
            if (!outgoing.empty()) {
                outgoing[0]->execute(token, context);
            }
        }
    }
    
    std::string getType() const override { return "ParallelGateway"; }
};

#endif // GATEWAY_H
