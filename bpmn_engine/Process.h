#ifndef PROCESS_H
#define PROCESS_H

#include "BPMNElement.h"
#include "Activity.h"
#include "Gateway.h"
#include "Token.h"
#include "ProcessContext.h"
#include <vector>
#include <memory>

/**
 * Process - Orquestador del proceso completo
 */
class Process {
private:
    std::string name;
    std::vector<std::unique_ptr<BPMNElement>> elements;
    BPMNElement* startElement;
    ProcessContext context;
    std::vector<Token> tokens;  // Tokens de la simulación (guardados para export)
    
public:
    Process(const std::string& name) : name(name), startElement(nullptr) {}
    
    // Agregar elementos al proceso
    Event* addStartEvent(const std::string& id, const std::string& name) {
        auto event = std::make_unique<Event>(id, name, true);
        Event* ptr = event.get();
        elements.push_back(std::move(event));
        if (!startElement) startElement = ptr;
        return ptr;
    }
    
    Event* addEndEvent(const std::string& id, const std::string& name) {
        auto event = std::make_unique<Event>(id, name, false);
        Event* ptr = event.get();
        elements.push_back(std::move(event));
        return ptr;
    }
    
    Activity* addActivity(const std::string& id, const std::string& name, 
                         double time, const std::string& resource) {
        auto activity = std::make_unique<Activity>(id, name, time, resource);
        Activity* ptr = activity.get();
        elements.push_back(std::move(activity));
        return ptr;
    }
    
    ExclusiveGateway* addExclusiveGateway(const std::string& id, 
                                          const std::string& name) {
        auto gateway = std::make_unique<ExclusiveGateway>(id, name);
        ExclusiveGateway* ptr = gateway.get();
        elements.push_back(std::move(gateway));
        return ptr;
    }
    
    ParallelGateway* addParallelGateway(const std::string& id, 
                                        const std::string& name, 
                                        bool diverge = true) {
        auto gateway = std::make_unique<ParallelGateway>(id, name, diverge);
        ParallelGateway* ptr = gateway.get();
        elements.push_back(std::move(gateway));
        return ptr;
    }
    
    // Configurar recursos
    void addResource(const std::string& name, int quantity, double costPerHour) {
        context.addResource(name, quantity, costPerHour);
    }
    
    // Ejecutar el proceso con un token
    void executeToken(Token& token) {
        if (startElement) {
            startElement->execute(token, context);
        }
    }
    
    // Simular múltiples candidatos
    void simulate(int numCandidates, double arrivalInterval = 1.0) {
        std::cout << "\n================================================\n";
        std::cout << "  SIMULACION: " << name << std::endl;
        std::cout << "  Candidatos: " << numCandidates << std::endl;
        std::cout << "================================================\n\n";
        
        double currentTime = 0.0;
        tokens.clear();  // Limpiar tokens de simulaciones anteriores
        
        // Crear tokens
        for (int i = 0; i < numCandidates; i++) {
            tokens.emplace_back(i + 1, currentTime);
            currentTime += arrivalInterval;
        }
        
        // Ejecutar cada token
        for (auto& token : tokens) {
            std::cout << "\n--- Candidato #" << token.getCandidateId() << " ---\n";
            executeToken(token);
        }
        
        // Reportes finales
        std::cout << "\n\n";
        context.printMetricsReport();
        context.printResourceReport();
        
        // Calcular tiempo de ciclo promedio
        double totalCycleTime = 0.0;
        int completedCount = 0;
        for (const auto& token : tokens) {
            if (token.isCompleted()) {
                totalCycleTime += token.getCycleTime();
                completedCount++;
            }
        }
        
        if (completedCount > 0) {
            double avgCycleTime = totalCycleTime / completedCount;
            std::cout << "\n=== TIEMPO DE CICLO ===\n";
            std::cout << "Promedio: " << avgCycleTime << " minutos";
            std::cout << " (" << avgCycleTime / 60.0 << " horas)\n";
            std::cout << " (" << avgCycleTime / 420.0 << " días laborables)\n";
        }
    }
    
    ProcessContext& getContext() { return context; }
    const std::vector<Token>& getTokens() const { return tokens; }
};

#endif // PROCESS_H
