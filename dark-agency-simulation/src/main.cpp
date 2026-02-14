/**
 * @file main.cpp
 * @brief Entry point for Dark Agency Simulation
 * 
 * Dark Agency in Institutional Voids:
 * Intrapreneurial Innovation and Bureaucratic Rule-Breaking
 * 
 * A simulation demonstrating how agents with high Dark Agency (S_Agency)
 * but moderate G-factor can navigate institutional voids to achieve
 * innovation, while toxic agents (high G) cause damage without progress.
 * 
 * Based on thesis by James
 * 
 * Validates hypotheses H1a-c:
 * - H1a: S_Agency → EIB (+)
 * - H1b: S_Agency → CWB-O (+), CWB-I (neutral)
 * - H1c: G → CWB-I (+), EIB (-)
 */

#include <iostream>
#include <string>
#include <cstring>
#include "simulation.hpp"
#include "config.hpp"

void printUsage(const char* programName) {
    std::cout << "Uso: " << programName << " [opciones]\n\n";
    std::cout << "Opciones:\n";
    std::cout << "  --help, -h        Muestra esta ayuda\n";
    std::cout << "  --fast, -f        Modo rápido (sin visualización)\n";
    std::cout << "  --slow, -s        Modo lento (200ms entre frames)\n";
    std::cout << "  --delay N         Delay personalizado (ms)\n";
    std::cout << "  --ticks N         Número de ticks (default: " << config::MAX_TICKS << ")\n";
    std::cout << "  --population N    Tamaño de población (default: " << config::POPULATION_SIZE << ")\n";
    std::cout << "\nEjemplos:\n";
    std::cout << "  " << programName << "              # Simulación visual normal\n";
    std::cout << "  " << programName << " --fast       # Solo estadísticas finales\n";
    std::cout << "  " << programName << " --delay 100  # Más rápido\n";
}

int main(int argc, char* argv[]) {
    // Default options
    bool visual = true;
    int delayMs = config::RENDER_DELAY_MS;
    
    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            printUsage(argv[0]);
            return 0;
        }
        else if (strcmp(argv[i], "--fast") == 0 || strcmp(argv[i], "-f") == 0) {
            visual = false;
        }
        else if (strcmp(argv[i], "--slow") == 0 || strcmp(argv[i], "-s") == 0) {
            delayMs = 200;
        }
        else if (strcmp(argv[i], "--delay") == 0 && i + 1 < argc) {
            delayMs = std::stoi(argv[++i]);
        }
    }
    
    // Header
    std::cout << "\n";
    std::cout << "   ____    _    ____  _  __     _    ____ _____ _   _  ______   __\n";
    std::cout << "  |  _ \\  / \\  |  _ \\| |/ /    / \\  / ___| ____| \\ | |/ ___\\ \\ / /\n";
    std::cout << "  | | | |/ _ \\ | |_) | ' /    / _ \\| |  _|  _| |  \\| | |    \\ V / \n";
    std::cout << "  | |_| / ___ \\|  _ <| . \\   / ___ \\ |_| | |___| |\\  | |___  | |  \n";
    std::cout << "  |____/_/   \\_\\_| \\_\\_|\\_\\ /_/   \\_\\____|_____|_| \\_|\\____| |_|  \n";
    std::cout << "\n";
    std::cout << "  In Institutional Voids: Intrapreneurial Innovation\n";
    std::cout << "  and Bureaucratic Rule-Breaking in Service Organizations\n";
    std::cout << "\n";
    
    // Create and run simulation
    Simulation sim;
    sim.initialize();
    sim.run(visual, delayMs);
    
    std::cout << "\n¡Simulación completada!\n";
    std::cout << "Revisa los archivos en output/ para análisis detallado.\n\n";
    
    // Narrative
    std::cout << "═══════════════════════════════════════════════════════════════\n";
    std::cout << "NARRATIVA:\n";
    std::cout << "───────────────────────────────────────────────────────────────\n";
    std::cout << "\"Mira el código. La mayoría de empresas (el 'else') se detienen\n";
    std::cout << "ante el muro. Mis 'Dark Agents' (if s_agency > 0.7) son los\n";
    std::cout << "únicos que cruzan. El código demuestra que sin ellos, la empresa\n";
    std::cout << "se estanca. Matemáticamente, la rebeldía instrumentalmente\n";
    std::cout << "calculada es rentabilidad.\"\n";
    std::cout << "═══════════════════════════════════════════════════════════════\n\n";
    
    return 0;
}
