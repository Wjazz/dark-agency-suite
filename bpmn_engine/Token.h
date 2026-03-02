#ifndef TOKEN_H
#define TOKEN_H

#include <string>
#include <map>

/**
 * Token representa una instancia del proceso en ejecución
 * Cada candidato es un token que fluye por el proceso
 */
class Token {
private:
    int candidateId;
    std::map<std::string, std::string> data; // Datos del candidato
    double startTime;
    double currentTime;
    bool completed;
    std::string endReason; // "Contratado", "Rechazado - Fase 1", etc.
    
public:
    Token(int id, double startTime) 
        : candidateId(id), startTime(startTime), currentTime(startTime), 
          completed(false), endReason("") {}
    
    // Getters
    int getCandidateId() const { return candidateId; }
    double getStartTime() const { return startTime; }
    double getCurrentTime() const { return currentTime; }
    double getCycleTime() const { return currentTime - startTime; }
    bool isCompleted() const { return completed; }
    std::string getEndReason() const { return endReason; }
    
    // Setters
    void setData(const std::string& key, const std::string& value) {
        data[key] = value;
    }
    
    std::string getData(const std::string& key) const {
        auto it = data.find(key);
        return (it != data.end()) ? it->second : "";
    }
    
    void advanceTime(double minutes) {
        currentTime += minutes;
    }
    
    void complete(const std::string& reason) {
        completed = true;
        endReason = reason;
    }
};

#endif // TOKEN_H
