#pragma once

/**
 * @file statistics.hpp
 * @brief Statistics collection and hypothesis validation
 */

#include <vector>
#include <cmath>
#include <sstream>
#include <iomanip>
#include <fstream>
#include "agent.hpp"
#include "config.hpp"

struct ClassificationStats {
    int count = 0;
    int alive = 0;
    float total_eib = 0;
    float total_cwbo = 0;
    float total_cwbi = 0;
    float avg_g = 0;
    float avg_s = 0;
    
    float avgEIB() const { return count > 0 ? total_eib / count : 0; }
    float avgCWBO() const { return count > 0 ? total_cwbo / count : 0; }
    float avgCWBI() const { return count > 0 ? total_cwbi / count : 0; }
};

class Statistics {
private:
    std::vector<std::pair<float, float>> s_agency_eib_pairs;
    std::vector<std::pair<float, float>> g_cwbi_pairs;
    std::vector<std::pair<float, float>> g_eib_pairs;
    
    ClassificationStats dark_stats;
    ClassificationStats toxic_stats;
    ClassificationStats maverick_stats;
    ClassificationStats normal_stats;
    
    int tick = 0;
    
public:
    void update(const std::vector<Agent>& agents, int currentTick) {
        tick = currentTick;
        
        // Reset stats
        dark_stats = toxic_stats = maverick_stats = normal_stats = ClassificationStats();
        s_agency_eib_pairs.clear();
        g_cwbi_pairs.clear();
        g_eib_pairs.clear();
        
        for (const Agent& a : agents) {
            const auto& m = a.getMetrics();
            
            ClassificationStats* stats = nullptr;
            switch (a.getClassification()) {
                case AgencyClassification::DARK_INNOVATOR: stats = &dark_stats; break;
                case AgencyClassification::TOXIC: stats = &toxic_stats; break;
                case AgencyClassification::MAVERICK_AT_RISK: stats = &maverick_stats; break;
                default: stats = &normal_stats; break;
            }
            
            stats->count++;
            if (a.isAlive()) stats->alive++;
            stats->total_eib += m.innovation_proposals;
            stats->total_cwbo += m.rule_violations;
            stats->total_cwbi += m.interpersonal_conflicts;
            stats->avg_g += a.getGFactor();
            stats->avg_s += a.getSAgency();
            
            // Collect for correlations
            s_agency_eib_pairs.push_back({a.getSAgency(), static_cast<float>(m.innovation_proposals)});
            g_cwbi_pairs.push_back({a.getGFactor(), static_cast<float>(m.interpersonal_conflicts)});
            g_eib_pairs.push_back({a.getGFactor(), static_cast<float>(m.innovation_proposals)});
        }
        
        // Finalize averages
        auto finalize = [](ClassificationStats& s) {
            if (s.count > 0) {
                s.avg_g /= s.count;
                s.avg_s /= s.count;
            }
        };
        finalize(dark_stats);
        finalize(toxic_stats);
        finalize(maverick_stats);
        finalize(normal_stats);
    }
    
    float pearson(const std::vector<std::pair<float, float>>& pairs) const {
        if (pairs.size() < 2) return 0.0f;
        
        float sum_x = 0, sum_y = 0, sum_xy = 0;
        float sum_x2 = 0, sum_y2 = 0;
        size_t n = pairs.size();
        
        for (const auto& p : pairs) {
            sum_x += p.first;
            sum_y += p.second;
            sum_xy += p.first * p.second;
            sum_x2 += p.first * p.first;
            sum_y2 += p.second * p.second;
        }
        
        float num = n * sum_xy - sum_x * sum_y;
        float den = std::sqrt((n * sum_x2 - sum_x * sum_x) * 
                              (n * sum_y2 - sum_y * sum_y));
        
        return den != 0 ? num / den : 0.0f;
    }
    
    float corrSAgencyEIB() const { return pearson(s_agency_eib_pairs); }
    float corrG_CWBI() const { return pearson(g_cwbi_pairs); }
    float corrG_EIB() const { return pearson(g_eib_pairs); }
    
    const ClassificationStats& getDarkStats() const { return dark_stats; }
    const ClassificationStats& getToxicStats() const { return toxic_stats; }
    const ClassificationStats& getMaverickStats() const { return maverick_stats; }
    const ClassificationStats& getNormalStats() const { return normal_stats; }
    
    std::string getSummary() const {
        std::stringstream ss;
        ss << std::fixed << std::setprecision(1);
        
        ss << "╔═══════════════════════════════════════════════════════════════════════════╗\n";
        ss << "║  DARK AGENCY DETECTOR - Tick: " << std::setw(4) << tick;
        ss << "                                       ║\n";
        ss << "╠═══════════════════════════════════════════════════════════════════════════╣\n";
        
        ss << "║  🔵 DARK INNOVATOR: " << std::setw(3) << dark_stats.alive << "/" << std::setw(3) << dark_stats.count;
        ss << "  EIB: " << std::setw(5) << dark_stats.avgEIB() << "  CWB-O: " << std::setw(5) << dark_stats.avgCWBO();
        ss << "  CWB-I: " << std::setw(5) << dark_stats.avgCWBI() << "  ║\n";
        
        ss << "║  🟡 MAVERICK RISK:  " << std::setw(3) << maverick_stats.alive << "/" << std::setw(3) << maverick_stats.count;
        ss << "  EIB: " << std::setw(5) << maverick_stats.avgEIB() << "  CWB-O: " << std::setw(5) << maverick_stats.avgCWBO();
        ss << "  CWB-I: " << std::setw(5) << maverick_stats.avgCWBI() << "  ║\n";
        
        ss << "║  🔴 TOXIC:          " << std::setw(3) << toxic_stats.alive << "/" << std::setw(3) << toxic_stats.count;
        ss << "  EIB: " << std::setw(5) << toxic_stats.avgEIB() << "  CWB-O: " << std::setw(5) << toxic_stats.avgCWBO();
        ss << "  CWB-I: " << std::setw(5) << toxic_stats.avgCWBI() << "  ║\n";
        
        ss << "║  ⚪ NORMAL:         " << std::setw(3) << normal_stats.alive << "/" << std::setw(3) << normal_stats.count;
        ss << "  EIB: " << std::setw(5) << normal_stats.avgEIB() << "  CWB-O: " << std::setw(5) << normal_stats.avgCWBO();
        ss << "  CWB-I: " << std::setw(5) << normal_stats.avgCWBI() << "  ║\n";
        
        ss << "╚═══════════════════════════════════════════════════════════════════════════╝\n";
        
        return ss.str();
    }
    
    std::string getHypothesisReport() const {
        std::stringstream ss;
        ss << std::fixed << std::setprecision(2);
        
        float r_sa_eib = corrSAgencyEIB();
        float r_g_cwbi = corrG_CWBI();
        float r_g_eib = corrG_EIB();
        
        ss << "\n═══════════════════════════════════════════════════════════════════════════\n";
        ss << "                    VALIDACIÓN DE HIPÓTESIS - BIFACTOR S-1\n";
        ss << "═══════════════════════════════════════════════════════════════════════════\n\n";
        
        ss << "H1a: S_Agency predice EIB positivamente\n";
        ss << "     r(S_Agency, EIB) = " << r_sa_eib << "\n";
        ss << "     " << (r_sa_eib > 0.1f ? "✓ CONFIRMADA" : "✗ NO CONFIRMADA") << "\n\n";
        
        ss << "H1c: G predice CWB-I positivamente, EIB negativamente\n";
        ss << "     r(G, CWB-I) = " << r_g_cwbi << "\n";
        ss << "     r(G, EIB) = " << r_g_eib << "\n";
        ss << "     " << (r_g_cwbi > 0.1f && r_g_eib < 0.0f ? "✓ CONFIRMADA" : "✗ NO CONFIRMADA") << "\n\n";
        
        ss << "───────────────────────────────────────────────────────────────────────────\n";
        ss << "CONCLUSIÓN: ";
        if (r_sa_eib > 0.1f && r_g_eib < 0.0f) {
            ss << "La Agencia Oscura (S_Agency), separada del Factor G,\n";
            ss << "           se asocia POSITIVAMENTE con innovación.\n";
            ss << "           Los Dark Innovators superan a todos los demás perfiles.\n";
        }
        ss << "═══════════════════════════════════════════════════════════════════════════\n";
        
        return ss.str();
    }
    
    void exportCSV(const std::string& filename) const {
        std::ofstream f(filename);
        f << "classification,count,alive,avg_eib,avg_cwbo,avg_cwbi,avg_g,avg_s\n";
        
        auto write = [&f](const std::string& name, const ClassificationStats& s) {
            f << name << "," << s.count << "," << s.alive << ","
              << s.avgEIB() << "," << s.avgCWBO() << "," << s.avgCWBI() << ","
              << s.avg_g << "," << s.avg_s << "\n";
        };
        
        write("DARK_INNOVATOR", dark_stats);
        write("MAVERICK_AT_RISK", maverick_stats);
        write("TOXIC", toxic_stats);
        write("NORMAL", normal_stats);
        
        f.close();
    }
};
