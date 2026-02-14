#pragma once

/**
 * @file simulation.hpp
 * @brief Main simulation orchestrator
 * 
 * Manages the simulation loop:
 * 1. Initialize population with distributed traits
 * 2. Run tick-by-tick simulation
 * 3. Render grid and statistics
 * 4. Export data for analysis
 */

#include <vector>
#include <iostream>
#include <chrono>
#include <thread>
#include <algorithm>
#include "config.hpp"
#include "grid.hpp"
#include "agent.hpp"
#include "statistics.hpp"
#include "random.hpp"

class Simulation {
private:
    Grid grid;
    std::vector<Agent> agents;
    Statistics stats;
    int currentTick;
    bool running;
    bool paused;
    
public:
    Simulation()
        : grid(config::GRID_WIDTH, config::GRID_HEIGHT)
        , currentTick(0)
        , running(true)
        , paused(false)
    {}
    
    /**
     * Initialize simulation with population and environment
     */
    void initialize() {
        // Generate environment
        grid.generateWalls();
        grid.placeGoals(5);
        grid.clearSpawnArea();
        
        // Create population with distributed traits
        createPopulation();
        
        // Initial statistics
        stats.reset();
        stats.update(agents, 0);
        
        printDisclaimer();
    }
    
    /**
     * Create population with trait distributions
     * Based on thesis: ~15% Dark Agents, ~10% Toxic, ~75% Normal
     */
    void createPopulation() {
        agents.clear();
        
        for (int i = 0; i < config::POPULATION_SIZE; i++) {
            float g, s_agency, vigilance, psycap, pops;
            
            // Determine agent type based on distribution
            float typeRoll = globalRng.uniform(0.0f, 1.0f);
            
            if (typeRoll < config::DARK_AGENT_RATIO) {
                // Dark Agent: High S_Agency, moderate G
                g = globalRng.normalClamped(0.35f, 0.15f);      // Lower G
                s_agency = globalRng.normalClamped(0.82f, 0.08f); // High S_Agency
                vigilance = globalRng.normalClamped(0.75f, 0.12f); // High VEE
                psycap = globalRng.normalClamped(0.70f, 0.12f);   // Good PsyCap
                pops = globalRng.normalClamped(0.65f, 0.15f);     // Higher POPS
            }
            else if (typeRoll < config::DARK_AGENT_RATIO + config::TOXIC_AGENT_RATIO) {
                // Toxic Agent: High G
                g = globalRng.normalClamped(0.82f, 0.08f);        // High G
                s_agency = globalRng.normalClamped(0.45f, 0.20f); // Variable S_Agency
                vigilance = globalRng.normalClamped(0.40f, 0.15f); // Lower VEE
                psycap = globalRng.normalClamped(0.35f, 0.15f);    // Lower PsyCap
                pops = globalRng.normalClamped(0.50f, 0.20f);      // Variable POPS
            }
            else {
                // Normal Agent: Low G, low S_Agency
                g = globalRng.normalClamped(0.30f, 0.15f);         // Low G
                s_agency = globalRng.normalClamped(0.35f, 0.15f);  // Low S_Agency
                vigilance = globalRng.normalClamped(0.45f, 0.15f); // Moderate VEE
                psycap = globalRng.normalClamped(0.55f, 0.15f);    // Moderate PsyCap
                pops = globalRng.normalClamped(0.40f, 0.15f);      // Lower POPS
            }
            
            // Random spawn position on left side
            int startX = globalRng.uniformInt(0, 4);
            int startY = globalRng.uniformInt(0, grid.getHeight() - 1);
            
            agents.emplace_back(i, g, s_agency, vigilance, psycap, pops, 
                               startX, startY);
        }
    }
    
    /**
     * Run simulation loop
     */
    void run(bool visual = true, int delayMs = config::RENDER_DELAY_MS) {
        for (currentTick = 0; currentTick < config::MAX_TICKS && running; currentTick++) {
            step();
            
            if (visual) {
                render();
                std::this_thread::sleep_for(std::chrono::milliseconds(delayMs));
            } else {
                // Progress indicator for non-visual mode
                if (currentTick % 500 == 0) {
                    std::cout << "Tick: " << currentTick << "/" << config::MAX_TICKS << "\r" << std::flush;
                }
            }
            
            // Check if all agents exhausted
            int aliveCount = std::count_if(agents.begin(), agents.end(),
                                           [](const Agent& a) { return a.isAlive(); });
            if (aliveCount == 0) {
                std::cout << "\nAll agents exhausted at tick " << currentTick << "\n";
                break;
            }
        }
        
        // Final render and report
        render();
        showFinalReport();
    }
    
    /**
     * Execute one simulation step
     */
    void step() {
        // Each agent makes a decision and executes it
        for (Agent& agent : agents) {
            if (agent.isAlive()) {
                Decision d = agent.decide(grid);
                agent.execute(d, grid, agents);
            }
        }
        
        // Update statistics
        stats.update(agents, currentTick);
    }
    
    /**
     * Render current state to terminal
     */
    void render() {
        // Clear screen
        std::cout << "\033[2J\033[H";
        
        // Create display buffer
        std::vector<std::vector<char>> display(
            grid.getHeight(), 
            std::vector<char>(grid.getWidth(), ' ')
        );
        std::vector<std::vector<std::string>> colors(
            grid.getHeight(), 
            std::vector<std::string>(grid.getWidth(), config::COLOR_RESET)
        );
        
        // Draw grid
        for (int y = 0; y < grid.getHeight(); y++) {
            for (int x = 0; x < grid.getWidth(); x++) {
                Cell c = grid.getCell(x, y);
                switch (c) {
                    case Cell::WALL:
                        display[y][x] = config::CHAR_WALL;
                        colors[y][x] = config::COLOR_YELLOW;
                        break;
                    case Cell::GOAL:
                        display[y][x] = config::CHAR_GOAL;
                        colors[y][x] = config::COLOR_CYAN;
                        break;
                    case Cell::INNOVATION_TRAIL:
                        display[y][x] = config::CHAR_INNOVATION_TRAIL;
                        colors[y][x] = config::COLOR_MAGENTA;
                        break;
                    case Cell::DAMAGE_TRAIL:
                        display[y][x] = config::CHAR_DAMAGE_TRAIL;
                        colors[y][x] = config::COLOR_RED;
                        break;
                    default:
                        display[y][x] = config::CHAR_EMPTY;
                        break;
                }
            }
        }
        
        // Draw agents (on top of grid)
        for (const Agent& agent : agents) {
            if (agent.isAlive()) {
                int ax = agent.getX();
                int ay = agent.getY();
                if (ax >= 0 && ax < grid.getWidth() && 
                    ay >= 0 && ay < grid.getHeight()) {
                    display[ay][ax] = agent.getDisplayChar();
                    colors[ay][ax] = agent.getDisplayColor();
                }
            }
        }
        
        // Print grid with border
        std::cout << "╔";
        for (int x = 0; x < grid.getWidth(); x++) std::cout << "═";
        std::cout << "╗\n";
        
        for (int y = 0; y < grid.getHeight(); y++) {
            std::cout << "║";
            for (int x = 0; x < grid.getWidth(); x++) {
                std::cout << colors[y][x] << display[y][x] << config::COLOR_RESET;
            }
            std::cout << "║\n";
        }
        
        std::cout << "╚";
        for (int x = 0; x < grid.getWidth(); x++) std::cout << "═";
        std::cout << "╝\n";
        
        // Print legend
        std::cout << "\nLeyenda: ";
        std::cout << config::COLOR_GREEN << "D" << config::COLOR_RESET << "=Dark Agent  ";
        std::cout << config::COLOR_RED << "T" << config::COLOR_RESET << "=Toxic  ";
        std::cout << config::COLOR_BLUE << "N" << config::COLOR_RESET << "=Normal  ";
        std::cout << config::COLOR_YELLOW << "#" << config::COLOR_RESET << "=Muro  ";
        std::cout << config::COLOR_CYAN << "*" << config::COLOR_RESET << "=Meta  ";
        std::cout << config::COLOR_MAGENTA << "+" << config::COLOR_RESET << "=Innovación\n";
        
        // Print statistics
        std::cout << stats.getSummary();
    }
    
    /**
     * Show final report with hypothesis validation
     */
    void showFinalReport() {
        std::cout << stats.getHypothesisReport();
        
        // Export data
        stats.exportCSV(config::OUTPUT_DIR + config::LOG_FILE);
        stats.exportReport(config::OUTPUT_DIR + config::REPORT_FILE);
        
        std::cout << "\nDatos exportados a:\n";
        std::cout << "  - " << config::OUTPUT_DIR + config::LOG_FILE << "\n";
        std::cout << "  - " << config::OUTPUT_DIR + config::REPORT_FILE << "\n";
    }
    
    /**
     * Print ethical disclaimer
     */
    void printDisclaimer() {
        std::cout << "\n";
        std::cout << "╔════════════════════════════════════════════════════════════╗\n";
        std::cout << "║ DARK AGENCY IN INSTITUTIONAL VOIDS                         ║\n";
        std::cout << "║ Simulation based on thesis by James                        ║\n";
        std::cout << "╠════════════════════════════════════════════════════════════╣\n";
        std::cout << "║ DISCLAIMER: Esta simulación es un modelo teórico que       ║\n";
        std::cout << "║ explora cómo ciertos perfiles de personalidad navegan      ║\n";
        std::cout << "║ entornos de vacíos institucionales. No promueve ni         ║\n";
        std::cout << "║ normaliza la transgresión normativa, sino que describe     ║\n";
        std::cout << "║ mecanismos adaptativos documentados en la literatura.      ║\n";
        std::cout << "╚════════════════════════════════════════════════════════════╝\n\n";
        
        std::cout << "Presiona Enter para iniciar la simulación...";
        std::cin.get();
    }
    
    // Getters
    const std::vector<Agent>& getAgents() const { return agents; }
    const Grid& getGrid() const { return grid; }
    const Statistics& getStats() const { return stats; }
    int getCurrentTick() const { return currentTick; }
};
