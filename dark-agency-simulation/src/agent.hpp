#pragma once

/**
 * @file agent.hpp
 * @brief Agent class representing employees in the simulation
 * 
 * This is the core of the thesis implementation:
 * - g_factor: General Antagonistic Factor
 * - s_agency: Dark Agency (S_Agency)
 * - vigilance: Strategic Environmental Vigilance (VEE)
 * - psycap: Psychological Capital
 * - perceived_politics: POPS
 * 
 * Decision algorithm implements H1a-c, H2, H3, H4 from the thesis.
 */

#include <string>
#include <cmath>
#include "config.hpp"
#include "cell.hpp"
#include "grid.hpp"
#include "random.hpp"

// Decision outcomes
enum class Decision {
    MOVE_FORWARD,           // Normal movement
    BREAK_RULE_AND_ADVANCE, // Instrumental transgression (Dark Agent)
    SABOTAGE_NO_ADVANCE,    // Destructive behavior (Toxic)
    WAIT_FOR_PERMISSION,    // Bureaucratic waiting (Normal)
    AVOID_OBSTACLE,         // Try alternative path
    EXHAUSTED               // Out of energy
};

// Agent type classification
enum class AgentType {
    DARK_AGENT,    // High S_Agency, moderate G
    TOXIC_AGENT,   // High G
    NORMAL_AGENT   // Low S_Agency, low G
};

class Agent {
private:
    // ================================================================
    // MEMBER DECLARATIONS - Order matches constructor initialization
    // ================================================================
    int id;                 // Unique identifier (FIRST to avoid -Wreorder)
    
    // Personality traits (from thesis constructs)
    float g_factor;         // G: General Antagonistic Factor [0,1]
    float s_agency;         // S_Agency: Dark Agency [0,1]
    float vigilance;        // VEE: Strategic Environmental Vigilance [0,1]
    float psycap;           // PsyCap: Psychological Capital [0,1]
    float perceived_politics; // POPS: Perceived Organizational Politics [0,1]
    
    // State
    int x, y;               // Position in grid
    float energy;           // Current energy level
    bool alive;             // Is agent still active
    
    // ================================================================
    // BEHAVIORAL COUNTERS (outcome variables)
    // ================================================================
    int innovation_score;   // EIB: Innovations achieved
    int cwb_o_count;        // CWB-O: Organizational transgressions
    int cwb_i_count;        // CWB-I: Interpersonal damage
    int wait_time;          // Ticks spent waiting
    int walls_crossed;      // Walls successfully crossed
    
    // Internal state
    int direction_x, direction_y;  // Current movement direction
    int stuck_counter;             // Ticks without progress
    
public:
    // ================================================================
    // CONSTRUCTOR
    // ================================================================
    Agent(int agentId, float g, float s, float vig, float pc, float pops, 
          int startX, int startY)
        : id(agentId)
        , g_factor(g)
        , s_agency(s)
        , vigilance(vig)
        , psycap(pc)
        , perceived_politics(pops)
        , x(startX)
        , y(startY)
        , energy(config::INITIAL_ENERGY)
        , alive(true)
        , innovation_score(0)
        , cwb_o_count(0)
        , cwb_i_count(0)
        , wait_time(0)
        , walls_crossed(0)
        , direction_x(1)
        , direction_y(0)
        , stuck_counter(0)
    {}
    
    // ================================================================
    // AGENT TYPE CLASSIFICATION (H1 criteria)
    // ================================================================
    
    /**
     * H1a-b: Dark Agent = High S_Agency AND S_Agency > G
     * These agents transgress instrumentally to achieve goals
     */
    bool isDarkAgent() const {
        return s_agency > config::S_AGENCY_THRESHOLD && 
               g_factor <= s_agency;
    }
    
    /**
     * H1c: Toxic Agent = High G
     * These agents are destructive without productive purpose
     */
    bool isToxic() const {
        return g_factor > config::G_THRESHOLD;
    }
    
    /**
     * Normal Agent = Neither Dark nor Toxic
     * These agents follow rules and wait for permission
     */
    bool isNormal() const {
        return !isDarkAgent() && !isToxic();
    }
    
    AgentType getType() const {
        if (isDarkAgent()) return AgentType::DARK_AGENT;
        if (isToxic()) return AgentType::TOXIC_AGENT;
        return AgentType::NORMAL_AGENT;
    }
    
    std::string getTypeName() const {
        switch (getType()) {
            case AgentType::DARK_AGENT: return "Dark";
            case AgentType::TOXIC_AGENT: return "Toxic";
            default: return "Normal";
        }
    }
    
    // ================================================================
    // CORE DECISION ALGORITHM (The Thesis in Code)
    // ================================================================
    
    /**
     * Main decision function implementing H1-H4
     * 
     * H1a: S_Agency → EIB (+)
     * H1b: S_Agency → CWB-O (+), CWB-I (neutral)
     * H1c: G → CWB (+), EIB (-)
     * H2: VEE mediates S_Agency → EIB
     * H3: POPS × S_Agency → VEE
     * H4: PsyCap × S_Agency → EIB
     */
    Decision decide(Grid& grid) {
        if (!alive || energy <= 0) {
            alive = false;
            return Decision::EXHAUSTED;
        }
        
        // Update direction toward nearest goal
        auto goalDir = grid.directionToGoal(x, y);
        if (goalDir.first != 0 || goalDir.second != 0) {
            direction_x = goalDir.first;
            direction_y = goalDir.second;
        }
        
        // Check what's ahead
        int nextX = x + direction_x;
        int nextY = y + direction_y;
        Cell ahead = grid.getCell(nextX, nextY);
        
        // ============================================================
        // PATH IS CLEAR - Move normally
        // ============================================================
        if (ahead == Cell::EMPTY || ahead == Cell::GOAL || 
            ahead == Cell::INNOVATION_TRAIL) {
            return Decision::MOVE_FORWARD;
        }
        
        // ============================================================
        // WALL AHEAD - This is where the thesis logic kicks in
        // ============================================================
        if (ahead == Cell::WALL) {
            // H3: POPS moderates VEE activation
            float effective_vee = calculateEffectiveVEE();
            
            // ========================================================
            // CASE 1: DARK AGENT (H1a-b)
            // "Instrumental transgression for productive outcomes"
            // ========================================================
            if (isDarkAgent()) {
                // Calculate risk/benefit ratio
                float benefit = calculateBenefit(grid);
                float risk = calculateRisk(grid);
                
                // H4: PsyCap moderates risk tolerance
                // H2: VEE enhances decision-making effectiveness
                float risk_tolerance = s_agency * (0.5f + psycap * 0.5f) * (0.8f + effective_vee * 0.2f);
                
                if (benefit * risk_tolerance > risk) {
                    // Strategic decision: Break the rule to advance
                    return Decision::BREAK_RULE_AND_ADVANCE;
                } else {
                    // Too risky, try another path
                    return Decision::AVOID_OBSTACLE;
                }
            }
            
            // ========================================================
            // CASE 2: TOXIC AGENT (H1c)
            // "Destructive behavior without productive purpose"
            // ========================================================
            else if (isToxic()) {
                // High G → Sabotage (CWB-I and CWB-O)
                // But does NOT advance toward goal
                if (globalRng.chance(g_factor * 0.5f)) {
                    return Decision::SABOTAGE_NO_ADVANCE;
                }
                return Decision::WAIT_FOR_PERMISSION;
            }
            
            // ========================================================
            // CASE 3: NORMAL AGENT
            // "Follows rules, waits for formal permission"
            // ========================================================
            else {
                // Try to find alternative path
                if (stuck_counter < 10 && globalRng.chance(vigilance)) {
                    return Decision::AVOID_OBSTACLE;
                }
                // Give up and wait
                return Decision::WAIT_FOR_PERMISSION;
            }
        }
        
        return Decision::AVOID_OBSTACLE;
    }
    
    /**
     * Execute the decision
     */
    void execute(Decision d, Grid& grid, std::vector<Agent>& allAgents) {
        switch (d) {
            case Decision::MOVE_FORWARD:
                moveForward(grid);
                break;
                
            case Decision::BREAK_RULE_AND_ADVANCE:
                breakRuleAndAdvance(grid);
                break;
                
            case Decision::SABOTAGE_NO_ADVANCE:
                sabotage(grid, allAgents);
                break;
                
            case Decision::WAIT_FOR_PERMISSION:
                waitForPermission();
                break;
                
            case Decision::AVOID_OBSTACLE:
                avoidObstacle(grid);
                break;
                
            case Decision::EXHAUSTED:
                alive = false;
                break;
        }
    }
    
    // ================================================================
    // BEHAVIORAL IMPLEMENTATIONS
    // ================================================================
    
private:
    /**
     * Normal movement - costs minimal energy
     */
    void moveForward(Grid& grid) {
        int nextX = x + direction_x;
        int nextY = y + direction_y;
        
        if (grid.isPassable(nextX, nextY)) {
            // Check for goal
            if (grid.isGoal(nextX, nextY)) {
                innovation_score++;  // EIB achieved!
            }
            
            x = nextX;
            y = nextY;
            energy -= config::MOVE_COST;
            stuck_counter = 0;
        } else {
            stuck_counter++;
        }
    }
    
    /**
     * H1a-b: Instrumental transgression (Dark Agent behavior)
     * Breaks organizational rules to advance toward goal
     */
    void breakRuleAndAdvance(Grid& grid) {
        cwb_o_count++;  // Organizational transgression
        energy -= config::RULE_BREAKING_COST;
        
        // Detection probability modified by POPS
        // High POPS = "rules are flexible" = lower detection
        float detection_prob = config::BASE_DETECTION_PROB * 
                               (1.0f - perceived_politics * 0.5f);
        
        if (globalRng.chance(detection_prob)) {
            // Caught! Penalty applied
            energy -= config::DETECTION_PENALTY;
        } else {
            // Success! Move through the wall
            int nextX = x + direction_x;
            int nextY = y + direction_y;
            
            // Leave innovation trail
            grid.setCell(x, y, Cell::INNOVATION_TRAIL);
            
            x = nextX;
            y = nextY;
            walls_crossed++;
            stuck_counter = 0;
            
            // Check if reached goal
            if (grid.isGoal(x, y)) {
                innovation_score++;  // EIB achieved through transgression!
            }
        }
    }
    
    /**
     * H1c: Destructive behavior (Toxic Agent behavior)
     * Damages others and organization without advancing
     */
    void sabotage(Grid& grid, std::vector<Agent>& allAgents) {
        cwb_o_count++;  // Some organizational damage
        energy -= config::SABOTAGE_COST;
        
        // Damage nearby agents (CWB-I)
        for (Agent& other : allAgents) {
            if (other.id != id && 
                std::abs(other.x - x) <= 1 && 
                std::abs(other.y - y) <= 1) {
                other.receiveDamage(10.0f);
                cwb_i_count++;
            }
        }
        
        // Leave damage trail
        grid.setCell(x, y, Cell::DAMAGE_TRAIL);
        
        stuck_counter++;
    }
    
    /**
     * Normal Agent behavior: Wait for formal permission
     */
    void waitForPermission() {
        wait_time++;
        energy -= config::WAIT_COST;
        stuck_counter++;
    }
    
    /**
     * Try to find an alternative path around obstacle
     */
    void avoidObstacle(Grid& grid) {
        // Try perpendicular directions
        int altDirs[4][2] = {
            {0, 1}, {0, -1}, {1, 0}, {-1, 0}
        };
        
        for (auto& dir : altDirs) {
            int testX = x + dir[0];
            int testY = y + dir[1];
            if (grid.isPassable(testX, testY)) {
                direction_x = dir[0];
                direction_y = dir[1];
                moveForward(grid);
                return;
            }
        }
        
        // No path found, wait
        stuck_counter++;
        energy -= config::WAIT_COST;
    }
    
    // ================================================================
    // HELPER CALCULATIONS
    // ================================================================
    
    /**
     * H3: POPS × S_Agency → VEE
     * Calculate effective vigilance moderated by political perception
     */
    float calculateEffectiveVEE() const {
        // In political environments, S_Agency activates VEE
        float pops_moderation = 1.0f + (perceived_politics * s_agency);
        return vigilance * pops_moderation;
    }
    
    /**
     * Estimate benefit of transgression
     */
    float calculateBenefit(const Grid& grid) const {
        float goalDist = grid.distanceToNearestGoal(x, y);
        // Closer to goal = higher benefit
        return 1.0f / (1.0f + goalDist * 0.1f);
    }
    
    /**
     * Estimate risk of transgression
     * Uses grid to assess environmental factors affecting detection
     */
    float calculateRisk(const Grid& grid) const {
        float base_risk = config::BASE_DETECTION_PROB;
        // POPS reduces perceived risk ("rules are flexible")
        // Distance to goal affects perceived urgency/caution
        float goal_proximity = 1.0f / (1.0f + grid.distanceToNearestGoal(x, y) * 0.05f);
        return base_risk * (1.0f - perceived_politics * 0.3f) * (1.0f - goal_proximity * 0.1f);
    }
    
public:
    /**
     * Receive damage from toxic agent
     */
    void receiveDamage(float damage) {
        energy -= damage;
        if (energy <= 0) {
            alive = false;
        }
    }
    
    // ================================================================
    // GETTERS
    // ================================================================
    int getId() const { return id; }
    int getX() const { return x; }
    int getY() const { return y; }
    float getEnergy() const { return energy; }
    bool isAlive() const { return alive && energy > 0; }
    
    float getGFactor() const { return g_factor; }
    float getSAgency() const { return s_agency; }
    float getVigilance() const { return vigilance; }
    float getPsyCap() const { return psycap; }
    float getPerceivedPolitics() const { return perceived_politics; }
    
    int getInnovationScore() const { return innovation_score; }
    int getCWB_O() const { return cwb_o_count; }
    int getCWB_I() const { return cwb_i_count; }
    int getWaitTime() const { return wait_time; }
    int getWallsCrossed() const { return walls_crossed; }
    
    // ================================================================
    // DISPLAY
    // ================================================================
    char getDisplayChar() const {
        if (!isAlive()) return '.';
        switch (getType()) {
            case AgentType::DARK_AGENT: return config::CHAR_DARK_AGENT;
            case AgentType::TOXIC_AGENT: return config::CHAR_TOXIC_AGENT;
            default: return config::CHAR_NORMAL_AGENT;
        }
    }
    
    std::string getDisplayColor() const {
        if (!isAlive()) return config::COLOR_RESET;
        switch (getType()) {
            case AgentType::DARK_AGENT: return config::COLOR_GREEN;
            case AgentType::TOXIC_AGENT: return config::COLOR_RED;
            default: return config::COLOR_BLUE;
        }
    }
};
