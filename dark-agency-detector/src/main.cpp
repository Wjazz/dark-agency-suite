/**
 * @file main.cpp
 * @brief DarkAgencyDetector - Inference Engine Simulation
 * 
 * Agent-Based Model demonstrating the Bifactor S-1 model:
 * - Dark Innovators (Cyan): High S_Agency, Low G → Innovate through transgression
 * - Mavericks (Yellow): High S_Agency, Rising G → At risk of becoming toxic
 * - Toxic (Red): High G → Destructive without purpose
 * - Normal (Blue): Low S_Agency, Low G → Follow rules
 * 
 * Exports frames for GIF generation.
 */

#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include <cstring>
#include "config.hpp"
#include "random.hpp"
#include "grid.hpp"
#include "agent.hpp"
#include "statistics.hpp"
#include "frame_exporter.hpp"

void printBanner() {
    std::cout << R"(
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   ██████╗  █████╗ ██████╗ ██╗  ██╗     █████╗  ██████╗ ███████╗  ║
    ║   ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██╔════╝ ██╔════╝  ║
    ║   ██║  ██║███████║██████╔╝█████╔╝     ███████║██║  ███╗█████╗    ║
    ║   ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██╔══██║██║   ██║██╔══╝    ║
    ║   ██████╔╝██║  ██║██║  ██║██║  ██╗    ██║  ██║╚██████╔╝███████╗  ║
    ║   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝  ║
    ║                                                                  ║
    ║              D E T E C T O R   v1.0                              ║
    ║                                                                  ║
    ║   Bifactor S-1 Inference Engine                                  ║
    ║   "La rebeldía calculada es rentabilidad"                        ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    )" << std::endl;
}

void printDisclaimer() {
    std::cout << "\n";
    std::cout << "╔══════════════════════════════════════════════════════════════════════╗\n";
    std::cout << "║ DISCLAIMER: Este motor de inferencia es un modelo teórico basado    ║\n";
    std::cout << "║ en investigación académica. Describe mecanismos funcionales sin     ║\n";
    std::cout << "║ prescribir normativamente que deban ser promovidos.                 ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════════════════╝\n\n";
}

std::vector<Agent> createPopulation() {
    std::vector<Agent> agents;
    
    for (int i = 0; i < config::POPULATION_SIZE; i++) {
        PsychometricProfile profile;
        
        float typeRoll = rng.uniform(0.0f, 1.0f);
        
        if (typeRoll < config::DARK_INNOVATOR_RATIO) {
            // Dark Innovator: High S_Agency components, low G components
            profile.narcissism = rng.normalClamped(0.75f, 0.10f);
            profile.machiavellianism = rng.normalClamped(0.80f, 0.08f);
            profile.psychopathy = rng.normalClamped(0.25f, 0.10f);
            profile.sadism = rng.normalClamped(0.15f, 0.08f);
            profile.vigilance = rng.normalClamped(0.80f, 0.10f);
            profile.psycap = rng.normalClamped(0.75f, 0.10f);
            profile.pops = rng.normalClamped(0.70f, 0.12f);
        }
        else if (typeRoll < config::DARK_INNOVATOR_RATIO + config::TOXIC_RATIO) {
            // Toxic: High G components
            profile.narcissism = rng.normalClamped(0.50f, 0.20f);
            profile.machiavellianism = rng.normalClamped(0.45f, 0.15f);
            profile.psychopathy = rng.normalClamped(0.85f, 0.08f);
            profile.sadism = rng.normalClamped(0.80f, 0.10f);
            profile.vigilance = rng.normalClamped(0.35f, 0.15f);
            profile.psycap = rng.normalClamped(0.30f, 0.12f);
            profile.pops = rng.normalClamped(0.50f, 0.20f);
        }
        else if (typeRoll < config::DARK_INNOVATOR_RATIO + config::TOXIC_RATIO + config::MAVERICK_RISK_RATIO) {
            // Maverick at Risk: High both, transitional
            profile.narcissism = rng.normalClamped(0.70f, 0.12f);
            profile.machiavellianism = rng.normalClamped(0.75f, 0.10f);
            profile.psychopathy = rng.normalClamped(0.55f, 0.12f);
            profile.sadism = rng.normalClamped(0.50f, 0.15f);
            profile.vigilance = rng.normalClamped(0.65f, 0.12f);
            profile.psycap = rng.normalClamped(0.50f, 0.15f);
            profile.pops = rng.normalClamped(0.65f, 0.15f);
        }
        else {
            // Normal: Low everything
            profile.narcissism = rng.normalClamped(0.35f, 0.15f);
            profile.machiavellianism = rng.normalClamped(0.30f, 0.12f);
            profile.psychopathy = rng.normalClamped(0.20f, 0.10f);
            profile.sadism = rng.normalClamped(0.15f, 0.08f);
            profile.vigilance = rng.normalClamped(0.45f, 0.15f);
            profile.psycap = rng.normalClamped(0.55f, 0.12f);
            profile.pops = rng.normalClamped(0.35f, 0.15f);
        }
        
        int startX = rng.uniformInt(0, 5);
        int startY = rng.uniformInt(0, config::GRID_HEIGHT - 1);
        
        agents.emplace_back(i, profile, startX, startY);
    }
    
    return agents;
}

int main(int argc, char* argv[]) {
    bool exportFrames = true;
    bool showVisual = true;
    int delayMs = 30;
    
    // Parse args
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--fast") == 0 || strcmp(argv[i], "-f") == 0) {
            showVisual = false;
        }
        else if (strcmp(argv[i], "--no-frames") == 0) {
            exportFrames = false;
        }
        else if (strcmp(argv[i], "--delay") == 0 && i + 1 < argc) {
            delayMs = std::stoi(argv[++i]);
        }
    }
    
    printBanner();
    printDisclaimer();
    
    std::cout << "Inicializando simulación...\n\n";
    
    // Initialize
    Grid grid;
    grid.generateEnvironment();
    
    std::vector<Agent> agents = createPopulation();
    Statistics stats;
    FrameExporter exporter;
    
    // Count by type
    int dark_count = 0, toxic_count = 0, maverick_count = 0, normal_count = 0;
    for (const Agent& a : agents) {
        switch (a.getClassification()) {
            case AgencyClassification::DARK_INNOVATOR: dark_count++; break;
            case AgencyClassification::TOXIC: toxic_count++; break;
            case AgencyClassification::MAVERICK_AT_RISK: maverick_count++; break;
            default: normal_count++; break;
        }
    }
    
    std::cout << "Población inicial:\n";
    std::cout << "  🔵 Dark Innovators: " << dark_count << "\n";
    std::cout << "  🟡 Mavericks at Risk: " << maverick_count << "\n";
    std::cout << "  🔴 Toxic: " << toxic_count << "\n";
    std::cout << "  ⚪ Normal: " << normal_count << "\n\n";
    
    if (exportFrames) {
        std::cout << "Exportando frames a " << config::FRAMES_DIR << " ...\n";
    }
    
    if (showVisual) {
        std::cout << "\nPresiona Enter para iniciar...";
        std::cin.get();
    }
    
    // Main loop
    for (int tick = 0; tick < config::MAX_TICKS; tick++) {
        // Each agent decides and acts
        for (Agent& agent : agents) {
            if (agent.isAlive()) {
                Decision d = agent.decide(grid);
                agent.execute(d, grid, agents);
            }
        }
        
        // Update statistics
        stats.update(agents, tick);
        
        // Export frame
        if (exportFrames && tick % config::FRAME_SKIP == 0) {
            exporter.exportFrame(grid, agents, tick);
        }
        
        // Visual output
        if (showVisual) {
            std::cout << "\033[2J\033[H";  // Clear screen
            std::cout << stats.getSummary();
            std::this_thread::sleep_for(std::chrono::milliseconds(delayMs));
        } else {
            if (tick % 100 == 0) {
                std::cout << "Tick: " << tick << "/" << config::MAX_TICKS << "\r" << std::flush;
            }
        }
        
        // Check if all dead
        int alive = 0;
        for (const Agent& a : agents) {
            if (a.isAlive()) alive++;
        }
        if (alive == 0) break;
    }
    
    // Final statistics
    std::cout << "\n";
    std::cout << stats.getSummary();
    std::cout << stats.getHypothesisReport();
    
    // Export results
    stats.exportCSV(config::OUTPUT_DIR + "results.csv");
    
    if (exportFrames) {
        std::cout << "\n✓ " << exporter.getFrameCount() << " frames exportados a " << config::FRAMES_DIR << "\n";
        std::cout << "\nPara generar el GIF, ejecuta:\n";
        std::cout << "  python3 scripts/make_gif.py\n";
    }
    
    // The pitch
    std::cout << "\n";
    std::cout << "═══════════════════════════════════════════════════════════════════════════\n";
    std::cout << "THE PITCH:\n";
    std::cout << "───────────────────────────────────────────────────────────────────────────\n";
    std::cout << "\"Mira los puntos cian. Esos son los Dark Innovators. Rompen\n";
    std::cout << "burocracia, pero llegan a las metas mientras los rojos destruyen\n";
    std::cout << "sin avanzar. Mi tesis demostró que la rebeldía calculada es rentabilidad.\n";
    std::cout << "Y ahora lo programé en C++ para que cualquier empresa pueda inferirlo.\"\n";
    std::cout << "═══════════════════════════════════════════════════════════════════════════\n\n";
    
    return 0;
}
