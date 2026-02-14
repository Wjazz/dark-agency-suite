#ifndef METRICS_EXPORTER_H
#define METRICS_EXPORTER_H

#include "ProcessContext.h"
#include "Token.h"
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip>

/**
 * MetricsExporter - Exporta métricas a CSV para análisis externo
 */
class MetricsExporter {
private:
    std::string baseFilename;
    
public:
    MetricsExporter(const std::string& filename) : baseFilename(filename) {}
    
    // Exportar métricas de recursos
    void exportResources(const ProcessContext& context, const std::string& filename = "") {
        std::string fname = filename.empty() ? baseFilename + "_recursos.csv" : filename;
        std::ofstream file(fname);
        
        if (!file.is_open()) {
            std::cerr << "Error: No se pudo crear " << fname << std::endl;
            return;
        }
        
        // Header
        file << "Recurso,Cantidad_Disponible,Tiempo_Usado_Minutos,Tiempo_Usado_Horas,Costo_Total,Costo_Por_Hora\\n";
        
        // Datos (necesitamos un método público para acceder a resources)
        // Por ahora, esto es un placeholder - necesitamos modificar ProcessContext
        
        file.close();
        std::cout << "[CSV] Recursos exportados a: " << fname << std::endl;
    }
    
    // Exportar métricas de tokens (candidatos)
    void exportTokens(const std::vector<Token>& tokens, const std::string& filename = "") {
        std::string fname = filename.empty() ? baseFilename + "_candidatos.csv" : filename;
        std::ofstream file(fname);
        
        if (!file.is_open()) {
            std::cerr << "Error: No se pudo crear " << fname << std::endl;
            return;
        }
        
        // Header
        file << "Candidato_ID,Tiempo_Inicio,Tiempo_Fin,Tiempo_Ciclo_Minutos,Tiempo_Ciclo_Horas,Completado,Resultado\\n";
        
        // Datos
        for (const auto& token : tokens) {
            file << token.getCandidateId() << ","
                 << std::fixed << std::setprecision(2)
                 << token.getStartTime() << ","
                 << token.getCurrentTime() << ","
                 << token.getCycleTime() << ","
                 << (token.getCycleTime() / 60.0) << ","
                 << (token.isCompleted() ? "Si" : "No") << ","
                 << "\"" << token.getEndReason() << "\"\\n";
        }
        
        file.close();
        std::cout << "[CSV] Candidatos exportados a: " << fname << std::endl;
    }
    
    // Exportar resumen de métricas
    void exportSummary(const ProcessContext& context, const std::vector<Token>& tokens, 
                      const std::string& filename = "") {
        std::string fname = filename.empty() ? baseFilename + "_resumen.csv" : filename;
        std::ofstream file(fname);
        
        if (!file.is_open()) {
            std::cerr << "Error: No se pudo crear " << fname << std::endl;
            return;
        }
        
        // Calcular estadísticas
        int totalTokens = tokens.size();
        int completedTokens = 0;
        double totalCycleTime = 0.0;
        double minCycleTime = 1e9;
        double maxCycleTime = 0.0;
        
        for (const auto& token : tokens) {
            if (token.isCompleted()) {
                completedTokens++;
                double cycleTime = token.getCycleTime();
                totalCycleTime += cycleTime;
                if (cycleTime < minCycleTime) minCycleTime = cycleTime;
                if (cycleTime > maxCycleTime) maxCycleTime = cycleTime;
            }
        }
        
        double avgCycleTime = completedTokens > 0 ? totalCycleTime / completedTokens : 0.0;
        
        // Header y datos
        file << "Metrica,Valor\\n";
        file << "Total_Candidatos," << totalTokens << "\\n";
        file << "Candidatos_Completados," << completedTokens << "\\n";
        file << "Tasa_Completado_Porcentaje," << std::fixed << std::setprecision(2) 
             << (completedTokens * 100.0 / totalTokens) << "\\n";
        file << "Tiempo_Ciclo_Promedio_Minutos," << avgCycleTime << "\\n";
        file << "Tiempo_Ciclo_Promedio_Horas," << (avgCycleTime / 60.0) << "\\n";
        file << "Tiempo_Ciclo_Promedio_Dias_Laborables," << (avgCycleTime / 420.0) << "\\n";
        file << "Tiempo_Ciclo_Minimo_Minutos," << (minCycleTime < 1e9 ? minCycleTime : 0) << "\\n";
        file << "Tiempo_Ciclo_Maximo_Minutos," << maxCycleTime << "\\n";
        
        file.close();
        std::cout << "[CSV] Resumen exportado a: " << fname << std::endl;
    }
    
    // Exportar todo (conveniencia)
    void exportAll(const ProcessContext& context, const std::vector<Token>& tokens) {
        exportTokens(tokens);
        exportSummary(context, tokens);
        std::cout << "[CSV] Exportacion completa finalizada\\n";
    }
};

#endif // METRICS_EXPORTER_H
