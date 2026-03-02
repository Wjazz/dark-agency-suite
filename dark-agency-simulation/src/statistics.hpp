#pragma once

/**
 * @file statistics.hpp
 * @brief Statistics collection and analysis for hypothesis validation
 * 
 * Collects data to validate:
 * H1a: S_Agency → EIB (+)
 * H1b: S_Agency → CWB-O (+), CWB-I (neutral)
 * H1c: G → CWB (+), EIB (-)
 * H2-H4: Moderation effects
 */

#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <fstream>
#include <iomanip>
#include <sstream>
#include "agent.hpp"
#include "config.hpp"

struct AgentSnapshot {
    int id;
    AgentType type;
    float g_factor;
    float s_agency;
    float vigilance;
    float psycap;
    float perceived_politics;
    int innovation_score;
    int cwb_o;
    int cwb_i;
    int wait_time;
    bool alive;
};

struct TypeStatistics {
    int count = 0;
    int alive_count = 0;
    float avg_eib = 0.0f;
    float avg_cwb_o = 0.0f;
    float avg_cwb_i = 0.0f;
    float avg_wait_time = 0.0f;
    float total_eib = 0;
    float total_cwb_o = 0;
    float total_cwb_i = 0;
};

class Statistics {
private:
    std::vector<AgentSnapshot> snapshots;
    std::vector<std::vector<float>> tick_data;  // Data per tick for CSV
    
    TypeStatistics dark_stats;
    TypeStatistics toxic_stats;
    TypeStatistics normal_stats;
    
    int total_innovations = 0;
    int total_cwb_o = 0;
    int total_cwb_i = 0;
    int current_tick = 0;
    
public:
    void reset() {
        snapshots.clear();
        tick_data.clear();
        dark_stats = TypeStatistics();
        toxic_stats = TypeStatistics();
        normal_stats = TypeStatistics();
        total_innovations = 0;
        total_cwb_o = 0;
        total_cwb_i = 0;
        current_tick = 0;
    }
    
    void update(const std::vector<Agent>& agents, int tick) {
        current_tick = tick;
        
        // Reset type stats
        dark_stats = TypeStatistics();
        toxic_stats = TypeStatistics();
        normal_stats = TypeStatistics();
        total_innovations = 0;
        total_cwb_o = 0;
        total_cwb_i = 0;
        
        // Collect snapshots
        snapshots.clear();
        for (const Agent& a : agents) {
            AgentSnapshot snap;
            snap.id = a.getId();
            snap.type = a.getType();
            snap.g_factor = a.getGFactor();
            snap.s_agency = a.getSAgency();
            snap.vigilance = a.getVigilance();
            snap.psycap = a.getPsyCap();
            snap.perceived_politics = a.getPerceivedPolitics();
            snap.innovation_score = a.getInnovationScore();
            snap.cwb_o = a.getCWB_O();
            snap.cwb_i = a.getCWB_I();
            snap.wait_time = a.getWaitTime();
            snap.alive = a.isAlive();
            snapshots.push_back(snap);
            
            // Update type statistics
            TypeStatistics* stats = nullptr;
            switch (snap.type) {
                case AgentType::DARK_AGENT: stats = &dark_stats; break;
                case AgentType::TOXIC_AGENT: stats = &toxic_stats; break;
                default: stats = &normal_stats; break;
            }
            
            stats->count++;
            if (snap.alive) stats->alive_count++;
            stats->total_eib += snap.innovation_score;
            stats->total_cwb_o += snap.cwb_o;
            stats->total_cwb_i += snap.cwb_i;
            stats->avg_wait_time += snap.wait_time;
            
            total_innovations += snap.innovation_score;
            total_cwb_o += snap.cwb_o;
            total_cwb_i += snap.cwb_i;
        }
        
        // Calculate averages
        auto calcAvg = [](TypeStatistics& s) {
            if (s.count > 0) {
                s.avg_eib = s.total_eib / s.count;
                s.avg_cwb_o = s.total_cwb_o / s.count;
                s.avg_cwb_i = s.total_cwb_i / s.count;
                s.avg_wait_time /= s.count;
            }
        };
        
        calcAvg(dark_stats);
        calcAvg(toxic_stats);
        calcAvg(normal_stats);
        
        // Store tick data for CSV export
        tick_data.push_back({
            static_cast<float>(tick),
            static_cast<float>(dark_stats.count),
            static_cast<float>(toxic_stats.count),
            static_cast<float>(normal_stats.count),
            dark_stats.avg_eib,
            toxic_stats.avg_eib,
            normal_stats.avg_eib,
            dark_stats.avg_cwb_o,
            toxic_stats.avg_cwb_o,
            normal_stats.avg_cwb_o,
            dark_stats.avg_cwb_i,
            toxic_stats.avg_cwb_i,
            normal_stats.avg_cwb_i
        });
    }
    
    // ================================================================
    // CORRELATION CALCULATIONS (for hypothesis validation)
    // ================================================================
    
    /**
     * Calculate Pearson correlation coefficient
     */
    float pearsonCorrelation(const std::vector<float>& x, 
                             const std::vector<float>& y) const {
        if (x.size() != y.size() || x.empty()) return 0.0f;
        
        size_t n = x.size();
        float sum_x = 0, sum_y = 0, sum_xy = 0;
        float sum_x2 = 0, sum_y2 = 0;
        
        for (size_t i = 0; i < n; i++) {
            sum_x += x[i];
            sum_y += y[i];
            sum_xy += x[i] * y[i];
            sum_x2 += x[i] * x[i];
            sum_y2 += y[i] * y[i];
        }
        
        float numerator = n * sum_xy - sum_x * sum_y;
        float denominator = std::sqrt((n * sum_x2 - sum_x * sum_x) * 
                                       (n * sum_y2 - sum_y * sum_y));
        
        if (denominator == 0) return 0.0f;
        return numerator / denominator;
    }
    
    /**
     * H1a: Correlation S_Agency ↔ EIB (expected: positive)
     */
    float correlationSAgencyEIB() const {
        std::vector<float> s_agency, eib;
        for (const auto& s : snapshots) {
            s_agency.push_back(s.s_agency);
            eib.push_back(static_cast<float>(s.innovation_score));
        }
        return pearsonCorrelation(s_agency, eib);
    }
    
    /**
     * H1b: Correlation S_Agency ↔ CWB-O (expected: positive)
     */
    float correlationSAgencyCWB_O() const {
        std::vector<float> s_agency, cwb_o;
        for (const auto& s : snapshots) {
            s_agency.push_back(s.s_agency);
            cwb_o.push_back(static_cast<float>(s.cwb_o));
        }
        return pearsonCorrelation(s_agency, cwb_o);
    }
    
    /**
     * H1b: Correlation S_Agency ↔ CWB-I (expected: low/neutral)
     */
    float correlationSAgencyCWB_I() const {
        std::vector<float> s_agency, cwb_i;
        for (const auto& s : snapshots) {
            s_agency.push_back(s.s_agency);
            cwb_i.push_back(static_cast<float>(s.cwb_i));
        }
        return pearsonCorrelation(s_agency, cwb_i);
    }
    
    /**
     * H1c: Correlation G ↔ EIB (expected: negative)
     */
    float correlationG_EIB() const {
        std::vector<float> g_factor, eib;
        for (const auto& s : snapshots) {
            g_factor.push_back(s.g_factor);
            eib.push_back(static_cast<float>(s.innovation_score));
        }
        return pearsonCorrelation(g_factor, eib);
    }
    
    /**
     * H1c: Correlation G ↔ CWB-I (expected: positive)
     */
    float correlationG_CWB_I() const {
        std::vector<float> g_factor, cwb_i;
        for (const auto& s : snapshots) {
            g_factor.push_back(s.g_factor);
            cwb_i.push_back(static_cast<float>(s.cwb_i));
        }
        return pearsonCorrelation(g_factor, cwb_i);
    }
    
    // ================================================================
    // GETTERS
    // ================================================================
    
    const TypeStatistics& getDarkStats() const { return dark_stats; }
    const TypeStatistics& getToxicStats() const { return toxic_stats; }
    const TypeStatistics& getNormalStats() const { return normal_stats; }
    
    int getTotalInnovations() const { return total_innovations; }
    int getTotalCWB_O() const { return total_cwb_o; }
    int getTotalCWB_I() const { return total_cwb_i; }
    int getCurrentTick() const { return current_tick; }
    
    // ================================================================
    // OUTPUT
    // ================================================================
    
    std::string getHypothesisReport() const {
        std::stringstream ss;
        
        ss << "\n═══════════════════════════════════════════════════════════\n";
        ss << "          VALIDACIÓN DE HIPÓTESIS - DARK AGENCY\n";
        ss << "═══════════════════════════════════════════════════════════\n\n";
        
        // H1a
        float r_sa_eib = correlationSAgencyEIB();
        ss << "H1a: S_Agency predice EIB positivamente\n";
        ss << "     Correlación calculada: r = " << std::fixed << std::setprecision(2) << r_sa_eib << "\n";
        ss << "     Hipótesis: " << (r_sa_eib > 0.1f ? "CONFIRMADA ✓" : "NO CONFIRMADA ✗") << "\n\n";
        
        // H1b
        float r_sa_cwbo = correlationSAgencyCWB_O();
        float r_sa_cwbi = correlationSAgencyCWB_I();
        ss << "H1b: S_Agency predice CWB-O pero NO CWB-I\n";
        ss << "     r(S_Agency, CWB-O) = " << std::fixed << std::setprecision(2) << r_sa_cwbo << "\n";
        ss << "     r(S_Agency, CWB-I) = " << std::fixed << std::setprecision(2) << r_sa_cwbi << "\n";
        ss << "     Hipótesis: " << (r_sa_cwbo > r_sa_cwbi && r_sa_cwbo > 0.1f ? "CONFIRMADA ✓" : "NO CONFIRMADA ✗") << "\n\n";
        
        // H1c
        float r_g_eib = correlationG_EIB();
        float r_g_cwbi = correlationG_CWB_I();
        ss << "H1c: G predice CWB-I (+) y EIB (-)\n";
        ss << "     r(G, EIB) = " << std::fixed << std::setprecision(2) << r_g_eib << "\n";
        ss << "     r(G, CWB-I) = " << std::fixed << std::setprecision(2) << r_g_cwbi << "\n";
        ss << "     Hipótesis: " << (r_g_eib < 0.0f && r_g_cwbi > 0.1f ? "CONFIRMADA ✓" : "NO CONFIRMADA ✗") << "\n\n";
        
        ss << "═══════════════════════════════════════════════════════════\n";
        ss << "CONCLUSIÓN: ";
        if (r_sa_eib > 0.1f && r_g_eib < 0.0f) {
            ss << "La simulación DEMUESTRA que la Agencia Oscura,\n";
            ss << "separada del Factor G, está asociada positivamente\n";
            ss << "con el comportamiento intraemprendedor (EIB).\n";
        } else {
            ss << "Resultados mixtos. Revisar parámetros.\n";
        }
        ss << "═══════════════════════════════════════════════════════════\n";
        
        return ss.str();
    }
    
    std::string getSummary() const {
        std::stringstream ss;
        
        ss << "╔════════════════════════════════════════════════════════════╗\n";
        ss << "║  DARK AGENCY SIMULATION - Tick: " << std::setw(5) << current_tick;
        ss << "                    ║\n";
        ss << "╠════════════════════════════════════════════════════════════╣\n";
        
        ss << "║  DARK AGENTS  (D): " << std::setw(3) << dark_stats.alive_count << "/" << std::setw(3) << dark_stats.count;
        ss << "    Innovaciones: " << std::setw(4) << static_cast<int>(dark_stats.total_eib) << " 💡    ║\n";
        
        ss << "║  TOXIC AGENTS (T): " << std::setw(3) << toxic_stats.alive_count << "/" << std::setw(3) << toxic_stats.count;
        ss << "    CWB-I: " << std::setw(4) << static_cast<int>(toxic_stats.total_cwb_i) << " 💀           ║\n";
        
        ss << "║  NORMAL AGENTS(N): " << std::setw(3) << normal_stats.alive_count << "/" << std::setw(3) << normal_stats.count;
        ss << "    Esperando: " << std::setw(4) << static_cast<int>(normal_stats.avg_wait_time) << " ⏳      ║\n";
        
        ss << "╠════════════════════════════════════════════════════════════╣\n";
        
        ss << "║  EIB Promedio:   Dark: " << std::fixed << std::setprecision(1) << std::setw(4) << dark_stats.avg_eib;
        ss << " | Toxic: " << std::setw(4) << toxic_stats.avg_eib;
        ss << " | Normal: " << std::setw(4) << normal_stats.avg_eib << "  ║\n";
        
        ss << "║  CWB-O Promedio: Dark: " << std::setw(4) << dark_stats.avg_cwb_o;
        ss << " | Toxic: " << std::setw(4) << toxic_stats.avg_cwb_o;
        ss << " | Normal: " << std::setw(4) << normal_stats.avg_cwb_o << "  ║\n";
        
        ss << "║  CWB-I Promedio: Dark: " << std::setw(4) << dark_stats.avg_cwb_i;
        ss << " | Toxic: " << std::setw(4) << toxic_stats.avg_cwb_i;
        ss << " | Normal: " << std::setw(4) << normal_stats.avg_cwb_i << "  ║\n";
        
        ss << "╚════════════════════════════════════════════════════════════╝\n";
        
        return ss.str();
    }
    
    void exportCSV(const std::string& filename) const {
        std::ofstream file(filename);
        if (!file.is_open()) return;
        
        // Header
        file << "tick,dark_count,toxic_count,normal_count,";
        file << "dark_eib,toxic_eib,normal_eib,";
        file << "dark_cwbo,toxic_cwbo,normal_cwbo,";
        file << "dark_cwbi,toxic_cwbi,normal_cwbi\n";
        
        // Data
        for (const auto& row : tick_data) {
            for (size_t i = 0; i < row.size(); i++) {
                file << row[i];
                if (i < row.size() - 1) file << ",";
            }
            file << "\n";
        }
        
        file.close();
    }
    
    void exportReport(const std::string& filename) const {
        std::ofstream file(filename);
        if (!file.is_open()) return;
        
        file << getHypothesisReport();
        file << "\n\n";
        file << getSummary();
        
        file.close();
    }
};
