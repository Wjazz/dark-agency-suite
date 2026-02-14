#pragma once

/**
 * @file agent.hpp
 * @brief Agent class with Bifactor model integration
 * 
 * Each agent represents an employee with Dark Tetrad traits.
 * Decision-making is driven by the Bifactor model classification.
 */

#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include "config.hpp"
#include "bifactor_model.hpp"
#include "grid.hpp"
#include "random.hpp"

enum class Decision {
    MOVE_FORWARD,
    BREAK_RULE_AND_ADVANCE,  // Dark Innovator behavior
    SABOTAGE,                // Toxic behavior
    WAIT,                    // Normal behavior
    AVOID,
    EXHAUSTED
};

class Agent {
private:
    int id;
    int x, y;
    float energy;
    bool alive;
    
    // Psychometric profile
    PsychometricProfile psycho;
    
    // Calculated factors
    float g_factor;
    float s_agency;
    AgencyClassification classification;
    
    // Behavioral metrics
    BehavioralMetrics metrics;
    
    // Movement
    int dirX, dirY;
    int stuckCounter;
    
public:
    Agent(int agentId, const PsychometricProfile& profile, int startX, int startY)
        : id(agentId)
        , x(startX), y(startY)
        , energy(config::INITIAL_ENERGY)
        , alive(true)
        , psycho(profile)
        , dirX(1), dirY(0)
        , stuckCounter(0)
    {
        // Calculate factors using Bifactor model
        g_factor = globalModel.extractGFactor(psycho);
        s_agency = globalModel.calculateSAgency(psycho, g_factor);
        classification = globalModel.quickClassify(g_factor, s_agency);
    }
    
    // Getters
    int getId() const { return id; }
    int getX() const { return x; }
    int getY() const { return y; }
    float getEnergy() const { return energy; }
    bool isAlive() const { return alive && energy > 0; }
    float getGFactor() const { return g_factor; }
    float getSAgency() const { return s_agency; }
    AgencyClassification getClassification() const { return classification; }
    const BehavioralMetrics& getMetrics() const { return metrics; }
    
    /**
     * Main decision function - the thesis in action
     */
    Decision decide(Grid& grid) {
        if (!isAlive()) return Decision::EXHAUSTED;
        
        // Update direction toward goal
        auto goalDir = grid.directionToGoal(x, y);
        if (goalDir.first != 0 || goalDir.second != 0) {
            dirX = goalDir.first;
            dirY = goalDir.second;
        }
        
        int nextX = x + dirX;
        int nextY = y + dirY;
        CellType ahead = grid.getCell(nextX, nextY);
        
        // Path is clear
        if (ahead != CellType::WALL) {
            return Decision::MOVE_FORWARD;
        }
        
        // WALL AHEAD - Classification determines behavior
        
        switch (classification) {
            case AgencyClassification::DARK_INNOVATOR:
            case AgencyClassification::MAVERICK_AT_RISK: {
                // Calculate risk/benefit
                float benefit = 1.0f / (1.0f + grid.distanceToGoal(x, y) * 0.1f);
                float risk = config::BASE_DETECTION_PROB * (1.0f - psycho.psycap);
                float tolerance = s_agency * (0.5f + psycho.psycap * 0.5f);
                
                if (benefit * tolerance > risk) {
                    return Decision::BREAK_RULE_AND_ADVANCE;
                }
                return Decision::AVOID;
            }
            
            case AgencyClassification::TOXIC: {
                // High G agents sabotage instead of innovating
                if (rng.chance(g_factor * 0.6f)) {
                    return Decision::SABOTAGE;
                }
                return Decision::WAIT;
            }
            
            default: // NORMAL
                if (stuckCounter < 15 && rng.chance(psycho.vigilance)) {
                    return Decision::AVOID;
                }
                return Decision::WAIT;
        }
    }
    
    /**
     * Execute decision
     */
    void execute(Decision d, Grid& grid, std::vector<Agent>& others) {
        switch (d) {
            case Decision::MOVE_FORWARD:
                moveForward(grid);
                break;
            case Decision::BREAK_RULE_AND_ADVANCE:
                breakRuleAndAdvance(grid);
                break;
            case Decision::SABOTAGE:
                sabotage(grid, others);
                break;
            case Decision::WAIT:
                wait();
                break;
            case Decision::AVOID:
                avoid(grid);
                break;
            case Decision::EXHAUSTED:
                alive = false;
                break;
        }
    }
    
private:
    void moveForward(Grid& grid) {
        int nextX = x + dirX;
        int nextY = y + dirY;
        
        if (grid.isPassable(nextX, nextY)) {
            if (grid.isGoal(nextX, nextY)) {
                metrics.innovation_proposals++;  // EIB achieved!
            }
            x = nextX;
            y = nextY;
            stuckCounter = 0;
        } else {
            stuckCounter++;
        }
        energy -= config::MOVE_COST;
    }
    
    void breakRuleAndAdvance(Grid& grid) {
        metrics.rule_violations++;  // CWB-O
        energy -= config::TRANSGRESSION_COST;
        
        // Detection probability reduced by POPS
        float detection = config::BASE_DETECTION_PROB * (1.0f - psycho.pops * 0.5f);
        
        if (rng.chance(detection)) {
            energy -= config::DETECTION_PENALTY;
        } else {
            // Success - move through wall
            grid.setCell(x, y, CellType::INNOVATION_TRAIL);
            x += dirX;
            y += dirY;
            metrics.walls_crossed++;
            stuckCounter = 0;
            
            if (grid.isGoal(x, y)) {
                metrics.innovation_proposals++;  // EIB through transgression!
            }
        }
    }
    
    void sabotage(Grid& grid, std::vector<Agent>& others) {
        metrics.rule_violations++;
        energy -= config::SABOTAGE_COST;
        
        // Damage nearby agents (CWB-I)
        for (Agent& other : others) {
            if (other.id != id && 
                std::abs(other.x - x) <= 2 && 
                std::abs(other.y - y) <= 2) {
                other.receiveDamage(8.0f);
                metrics.interpersonal_conflicts++;
            }
        }
        
        grid.setCell(x, y, CellType::DAMAGE_TRAIL);
        stuckCounter++;
    }
    
    void wait() {
        metrics.time_waiting++;
        energy -= config::WAIT_COST;
        stuckCounter++;
    }
    
    void avoid(Grid& grid) {
        // Try perpendicular directions
        int dirs[4][2] = {{0,1}, {0,-1}, {1,0}, {-1,0}};
        for (auto& d : dirs) {
            int testX = x + d[0];
            int testY = y + d[1];
            if (grid.isPassable(testX, testY)) {
                dirX = d[0];
                dirY = d[1];
                moveForward(grid);
                return;
            }
        }
        stuckCounter++;
        energy -= config::WAIT_COST;
    }
    
public:
    void receiveDamage(float dmg) {
        energy -= dmg;
        if (energy <= 0) alive = false;
    }
    
    config::Color getColor() const {
        if (!isAlive()) return config::COLOR_DEAD;
        switch (classification) {
            case AgencyClassification::DARK_INNOVATOR: return config::COLOR_DARK_INNOVATOR;
            case AgencyClassification::MAVERICK_AT_RISK: return config::COLOR_MAVERICK;
            case AgencyClassification::TOXIC: return config::COLOR_TOXIC;
            default: return config::COLOR_NORMAL;
        }
    }
};
