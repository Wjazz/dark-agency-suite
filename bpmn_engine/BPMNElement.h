#ifndef BPMN_ELEMENT_H
#define BPMN_ELEMENT_H

#include <string>
#include <vector>
#include <memory>
#include <iostream>

// Forward declarations
class Token;
class ProcessContext;

/**
 * Clase base abstracta para todos los elementos BPMN
 * Usa polimorfismo para permitir diferentes tipos de nodos
 */
class BPMNElement {
protected:
    std::string id;
    std::string name;
    std::vector<BPMNElement*> outgoing; // Flujos de salida
    
public:
    BPMNElement(const std::string& id, const std::string& name) 
        : id(id), name(name) {}
    
    virtual ~BPMNElement() = default;
    
    // Método virtual puro - cada elemento define cómo se ejecuta
    virtual void execute(Token& token, ProcessContext& context) = 0;
    
    // Conectar este elemento con el siguiente
    void connectTo(BPMNElement* next) {
        outgoing.push_back(next);
    }
    
    // Getters
    std::string getId() const { return id; }
    std::string getName() const { return name; }
    const std::vector<BPMNElement*>& getOutgoing() const { return outgoing; }
    
    // Método virtual para obtener tipo (útil para debugging)
    virtual std::string getType() const = 0;
};

#endif // BPMN_ELEMENT_H
