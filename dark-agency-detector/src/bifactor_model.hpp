#pragma once

/**
 * @file bifactor_model.hpp
 * @brief Bifactor S-1 Model implementation
 * 
 * Core of the thesis: Extracting G-factor and calculating S_Agency
 * to classify employees into behavioral profiles.
 * 
 * Based on thesis: "Dark Agency in Institutional Voids:
 * Intrapreneurial Innovation and Bureaucratic Rule-Breaking"
 */

#include <cmath>
#include <algorithm>
#include <string>
#include "config.hpp"

/**
 * Raw psychometric scores from Dark Tetrad assessment
 * All values normalized to [0, 1]
 */
struct PsychometricProfile {
    float narcissism;        // NPI-16 normalized
    float machiavellianism;  // MACH-IV normalized
    float psychopathy;       // SRP-III normalized
    float sadism;            // SSIS normalized
    
    // Additional constructs
    float vigilance;         // VEE: Strategic Environmental Vigilance
    float psycap;            // PsyCap: Psychological Capital
    float pops;              // POPS: Perceived Organizational Politics
    
    PsychometricProfile(float n = 0.5f, float m = 0.5f, float p = 0.5f, float s = 0.5f,
                        float v = 0.5f, float pc = 0.5f, float po = 0.5f)
        : narcissism(n), machiavellianism(m), psychopathy(p), sadism(s)
        , vigilance(v), psycap(pc), pops(po) {}
};

/**
 * Behavioral event counters
 */
struct BehavioralMetrics {
    int innovation_proposals = 0;   // EIB
    int rule_violations = 0;        // CWB-O
    int interpersonal_conflicts = 0; // CWB-I
    int walls_crossed = 0;          // Successful transgressions
    int time_waiting = 0;           // Bureaucratic stagnation
    float kpi_score = 0.5f;         // Performance metric
    
    float getInnovationRatio() const {
        return static_cast<float>(innovation_proposals) / 
               std::max(1, rule_violations);
    }
    
    float getConflictRatio() const {
        return static_cast<float>(interpersonal_conflicts) /
               std::max(0.1f, kpi_score);
    }
};

/**
 * Classification output from the Bifactor model
 */
enum class AgencyClassification {
    NORMAL,           // Low G, Low S_Agency
    DARK_INNOVATOR,   // Low G, High S_Agency - The productive rebels
    MAVERICK_AT_RISK, // Transitional - High S_Agency, increasing G
    TOXIC             // High G - Destructive patterns
};

inline std::string classificationToString(AgencyClassification c) {
    switch (c) {
        case AgencyClassification::NORMAL: return "NORMAL";
        case AgencyClassification::DARK_INNOVATOR: return "DARK_INNOVATOR";
        case AgencyClassification::MAVERICK_AT_RISK: return "MAVERICK_AT_RISK";
        case AgencyClassification::TOXIC: return "TOXIC";
        default: return "UNKNOWN";
    }
}

/**
 * Complete prediction output
 */
struct AgencyPrediction {
    AgencyClassification classification;
    float g_factor;           // Extracted antagonistic core
    float s_agency;           // Residual dark agency
    float eib_score;          // Predicted intrapreneurial behavior
    float cwb_o_risk;         // Organizational transgression risk
    float cwb_i_risk;         // Interpersonal transgression risk
    float confidence;         // Model confidence
    
    std::string getAlertLevel() const {
        switch (classification) {
            case AgencyClassification::TOXIC: return "CRITICAL";
            case AgencyClassification::MAVERICK_AT_RISK: return "HIGH";
            case AgencyClassification::DARK_INNOVATOR: return "MEDIUM";
            default: return "LOW";
        }
    }
};

/**
 * Bifactor S-1 Model Implementation
 * 
 * The model extracts G (general antagonistic factor) from the Dark Tetrad,
 * then calculates S_Agency as the residual variance that drives
 * instrumental (not destructive) transgression.
 */
class BifactorModel {
public:
    /**
     * Extract G-factor using factor loadings from literature
     * 
     * G represents the "core of darkness" - primarily psychopathy and sadism
     * which are associated with destructive outcomes (CWB-I)
     * 
     * @param p Psychometric profile
     * @return G-factor score [0, 1]
     */
    float extractGFactor(const PsychometricProfile& p) const {
        // G is the shared variance of the Dark Tetrad
        // Psychopathy and Sadism have highest loadings (antagonistic core)
        float g = config::LOADING_PSYCHOPATHY * p.psychopathy +
                  config::LOADING_SADISM * p.sadism +
                  config::LOADING_MACH * p.machiavellianism +
                  config::LOADING_NARC * p.narcissism;
        
        return std::clamp(g, 0.0f, 1.0f);
    }
    
    /**
     * Calculate S_Agency (Dark Agency) as residual
     * 
     * S_Agency = "Strategic darkness" after removing G
     * This is what drives intrapreneurial behavior (EIB)
     * 
     * From thesis: Narcissism and Machiavellianism load on S_Agency
     * after controlling for G
     * 
     * @param p Psychometric profile
     * @param g Extracted G-factor
     * @return S_Agency score [0, 1]
     */
    float calculateSAgency(const PsychometricProfile& p, float g) const {
        // Raw agency from Narcissism + Machiavellianism
        float raw_agency = 0.50f * p.machiavellianism + 0.50f * p.narcissism;
        
        // Remove G contamination (orthogonalize)
        // The 0.35 coefficient represents the correlation of G with raw_agency
        float s_agency = raw_agency - (g * 0.35f);
        
        // VEE (vigilance) amplifies S_Agency expression
        s_agency *= (1.0f + p.vigilance * 0.2f);
        
        return std::clamp(s_agency, 0.0f, 1.0f);
    }
    
    /**
     * H2: Calculate effective VEE (mediator)
     * 
     * VEE mediates the relationship S_Agency → EIB
     * POPS moderates the S_Agency → VEE relationship (H3)
     * 
     * @param p Psychometric profile
     * @param s_agency Calculated S_Agency
     * @return Effective VEE score
     */
    float calculateEffectiveVEE(const PsychometricProfile& p, float s_agency) const {
        // H3: POPS × S_Agency → VEE
        // In political environments, S_Agency activates VEE
        float pops_moderation = 1.0f + (p.pops * s_agency * 0.5f);
        return p.vigilance * pops_moderation;
    }
    
    /**
     * Predict EIB (Intrapreneurial Behavior) score
     * 
     * H1a: S_Agency → EIB (+)
     * H1c: G → EIB (-)
     * H2: VEE mediates
     * H4: PsyCap moderates
     * 
     * @param p Psychometric profile
     * @param g G-factor
     * @param s S_Agency
     * @return Predicted EIB score [0, 1]
     */
    float predictEIB(const PsychometricProfile& p, float g, float s) const {
        float effective_vee = calculateEffectiveVEE(p, s);
        
        // From thesis structural model
        float eib = 0.30f * s +                    // H1a: S_Agency → EIB (+)
                   -0.20f * g +                    // H1c: G → EIB (-)
                    0.25f * effective_vee +        // H2: VEE → EIB (+)
                    0.15f * p.psycap +             // PsyCap direct effect
                    0.10f * (s * p.psycap);        // H4: S_Agency × PsyCap
        
        return std::clamp(eib + 0.3f, 0.0f, 1.0f);  // Baseline adjustment
    }
    
    /**
     * Predict CWB-O (Organizational transgression) risk
     * 
     * H1b: S_Agency → CWB-O (+)
     * 
     * @return CWB-O risk score [0, 1]
     */
    float predictCWB_O(float g, float s) const {
        // Both G and S_Agency predict CWB-O, but for different reasons
        float cwb_o = 0.30f * s +   // H1b: Instrumental transgression
                      0.25f * g;     // Also driven by antagonism
        return std::clamp(cwb_o, 0.0f, 1.0f);
    }
    
    /**
     * Predict CWB-I (Interpersonal transgression) risk
     * 
     * H1b: S_Agency → CWB-I (neutral/low)
     * H1c: G → CWB-I (+++)
     * 
     * @return CWB-I risk score [0, 1]
     */
    float predictCWB_I(float g, float s) const {
        // G is the primary driver of interpersonal damage
        // S_Agency has minimal effect (the key insight of the thesis)
        float cwb_i = 0.70f * g +    // H1c: G → CWB-I (strong positive)
                      0.05f * s;      // H1b: S_Agency → CWB-I (near zero)
        return std::clamp(cwb_i, 0.0f, 1.0f);
    }
    
    /**
     * Main classification function
     * 
     * Integrates psychometric data with behavioral validation
     * to produce final classification
     */
    AgencyPrediction classify(const PsychometricProfile& psycho,
                              const BehavioralMetrics& behavior) const {
        AgencyPrediction pred;
        
        // Extract latent factors
        pred.g_factor = extractGFactor(psycho);
        pred.s_agency = calculateSAgency(psycho, pred.g_factor);
        
        // Predict outcomes
        pred.eib_score = predictEIB(psycho, pred.g_factor, pred.s_agency);
        pred.cwb_o_risk = predictCWB_O(pred.g_factor, pred.s_agency);
        pred.cwb_i_risk = predictCWB_I(pred.g_factor, pred.s_agency);
        
        // Behavioral validation
        float innovation_ratio = behavior.getInnovationRatio();
        float conflict_ratio = behavior.getConflictRatio();
        
        // Classification logic (H1a-c implementation)
        
        // H1c: High G → Toxic (regardless of S_Agency)
        if (pred.g_factor > config::G_THRESHOLD_TOXIC && conflict_ratio > 0.8f) {
            pred.classification = AgencyClassification::TOXIC;
            pred.confidence = 0.85f + (pred.g_factor - 0.7f);
        }
        // Transitional: Maverick at risk
        else if (pred.s_agency > config::S_AGENCY_THRESHOLD &&
                 pred.g_factor > config::G_THRESHOLD_MAVERICK &&
                 pred.g_factor <= config::G_THRESHOLD_TOXIC) {
            pred.classification = AgencyClassification::MAVERICK_AT_RISK;
            pred.confidence = 0.70f;
        }
        // H1a: High S_Agency + Low G → Dark Innovator
        else if (pred.s_agency > config::S_AGENCY_THRESHOLD &&
                 pred.g_factor <= config::G_THRESHOLD_MAVERICK &&
                 innovation_ratio > 0.3f) {
            pred.classification = AgencyClassification::DARK_INNOVATOR;
            pred.confidence = 0.80f + (pred.s_agency - 0.65f) * 0.5f;
        }
        // Default: Normal
        else {
            pred.classification = AgencyClassification::NORMAL;
            pred.confidence = 0.90f;
        }
        
        pred.confidence = std::clamp(pred.confidence, 0.0f, 1.0f);
        return pred;
    }
    
    /**
     * Quick classification without behavioral data
     * Used in simulation
     */
    AgencyClassification quickClassify(float g, float s) const {
        if (g > config::G_THRESHOLD_TOXIC) {
            return AgencyClassification::TOXIC;
        }
        if (s > config::S_AGENCY_THRESHOLD && g > config::G_THRESHOLD_MAVERICK) {
            return AgencyClassification::MAVERICK_AT_RISK;
        }
        if (s > config::S_AGENCY_THRESHOLD && g <= config::G_THRESHOLD_MAVERICK) {
            return AgencyClassification::DARK_INNOVATOR;
        }
        return AgencyClassification::NORMAL;
    }
};

// Global model instance
inline BifactorModel globalModel;
