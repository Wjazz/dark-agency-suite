#ifndef ACTIVITY_H
#define ACTIVITY_H

#include "BPMNElement.h"
#include "Token.h"
#include "ProcessContext.h"
#include <random>

/**
 * Event - Eventos de inicio y fin
 */
class Event : public BPMNElement {
private:
    bool isStart;
    
public:
    Event(const std::string& id, const std::string& name, bool start) 
        : BPMNElement(id, name), isStart(start) {}
    
    void execute(Token& token, ProcessContext& context) override {
        if (isStart) {
            context.tokenStarted();
            std::cout << "[>>] Candidato #" << token.getCandidateId() 
                     << " inicia proceso en t=" << token.getCurrentTime() << "\n";
            // Continuar con el siguiente elemento
            if (!outgoing.empty()) {
                outgoing[0]->execute(token, context);
            }
        } else {
            context.tokenCompleted(getName());
            token.complete(getName());
            std::cout << "[END] Candidato #" << token.getCandidateId() 
                     << " termina: " << getName() 
                     << " (ciclo: " << token.getCycleTime() << " min)\n";
        }
    }
    
    std::string getType() const override {
        return isStart ? "StartEvent" : "EndEvent";
    }
};

/**
 * Activity - Tarea que consume tiempo y recursos
 */
class Activity : public BPMNElement {
private:
    double processingTime; // en minutos
    std::string resourceName;
    
public:
    Activity(const std::string& id, const std::string& name, 
             double time, const std::string& resource) 
        : BPMNElement(id, name), processingTime(time), resourceName(resource) {}
    
    void execute(Token& token, ProcessContext& context) override {
        // Intentar adquirir recurso
        Resource* resource = context.getResource(resourceName);
        if (!resource) {
            std::cerr << "ERROR: Recurso '" << resourceName << "' no encontrado\n";
            return;
        }
        
        // Simular espera si no hay recursos disponibles
        while (!resource->isAvailable()) {
            // En simulación real, esperaríamos
            // Por ahora, asumimos que siempre hay disponible
            break;
        }
        
        resource->acquire();
        
        // Simular tiempo de procesamiento
        token.advanceTime(processingTime);
        resource->addUsage(processingTime);
        
        std::cout << "  -> [" << name << "] Candidato #" << token.getCandidateId() 
                 << " procesado en " << processingTime << " min"
                 << " por " << resourceName << "\n";
        
        resource->release();
        
        // Continuar con el siguiente elemento
        if (!outgoing.empty()) {
            outgoing[0]->execute(token, context);
        }
    }
    
    std::string getType() const override { return "Activity"; }
    double getProcessingTime() const { return processingTime; }
};

#endif // ACTIVITY_H
