#ifndef PROCESS_CONTEXT_H
#define PROCESS_CONTEXT_H

#include <string>
#include <map>
#include <vector>

/**
 * Estructura para representar un recurso (Analista, Gerente)
 */
struct Resource {
    std::string name;
    int totalAvailable;
    int currentlyUsed;
    double costPerHour;
    double totalCost;
    double totalTimeUsed; // en minutos
    
    Resource(const std::string& n, int available, double cost) 
        : name(n), totalAvailable(available), currentlyUsed(0), 
          costPerHour(cost), totalCost(0), totalTimeUsed(0) {}
    
    bool isAvailable() const {
        return currentlyUsed < totalAvailable;
    }
    
    void acquire() {
        if (isAvailable()) currentlyUsed++;
    }
    
    void release() {
        if (currentlyUsed > 0) currentlyUsed--;
    }
    
    void addUsage(double minutes) {
        totalTimeUsed += minutes;
        totalCost += (minutes / 60.0) * costPerHour;
    }
    
    double getUtilization() const {
        // Utilización como porcentaje
        return totalAvailable > 0 ? (double)currentlyUsed / totalAvailable * 100.0 : 0;
    }
};

/**
 * Contexto del proceso - recursos, métricas, configuración
 */
class ProcessContext {
private:
    std::map<std::string, Resource> resources;
    double currentSimulationTime;
    
    // Métricas
    int tokensStarted;
    int tokensCompleted;
    std::map<std::string, int> endReasons; // Cuenta por razón de fin
    
public:
    ProcessContext() : currentSimulationTime(0), tokensStarted(0), tokensCompleted(0) {}
    
    // Gestión de recursos
    void addResource(const std::string& name, int quantity, double costPerHour) {
        resources.emplace(name, Resource(name, quantity, costPerHour));
    }
    
    Resource* getResource(const std::string& name) {
        auto it = resources.find(name);
        return (it != resources.end()) ? &it->second : nullptr;
    }
    
    // Tiempo de simulación
    double getCurrentTime() const { return currentSimulationTime; }
    void setCurrentTime(double time) { currentSimulationTime = time; }
    
    // Métricas
    void tokenStarted() { tokensStarted++; }
    void tokenCompleted(const std::string& reason) { 
        tokensCompleted++; 
        endReasons[reason]++;
    }
    
    int getTokensStarted() const { return tokensStarted; }
    int getTokensCompleted() const { return tokensCompleted; }
    const std::map<std::string, int>& getEndReasons() const { return endReasons; }
    
    // Reporte de recursos
    void printResourceReport() const {
        std::cout << "\n=== REPORTE DE RECURSOS ===\n";
        for (const auto& [name, resource] : resources) {
            std::cout << "\nRecurso: " << name << "\n";
            std::cout << "  Disponibles: " << resource.totalAvailable << "\n";
            std::cout << "  Tiempo usado: " << resource.totalTimeUsed / 60.0 << " horas\n";
            std::cout << "  Costo total: $" << resource.totalCost << "\n";
            std::cout << "  Utilización promedio: " << resource.getUtilization() << "%\n";
        }
    }
    
    void printMetricsReport() const {
        std::cout << "\n=== MÉTRICAS DEL PROCESO ===\n";
        std::cout << "Candidatos iniciados: " << tokensStarted << "\n";
        std::cout << "Candidatos completados: " << tokensCompleted << "\n";
        std::cout << "\nResultados por razón:\n";
        for (const auto& [reason, count] : endReasons) {
            double percentage = (double)count / tokensCompleted * 100.0;
            std::cout << "  " << reason << ": " << count 
                     << " (" << percentage << "%)\n";
        }
    }
};

#endif // PROCESS_CONTEXT_H
