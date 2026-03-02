#pragma once

/**
 * @file config.hpp
 * @brief Configuration constants for Dark Agency Simulation
 * 
 * Based on thesis: "Dark Agency in Institutional Voids:
 * Intrapreneurial Innovation and Bureaucratic Rule-Breaking"
 */

#include <string>

namespace config {

// ============================================================
// GRID CONFIGURATION
// ============================================================
constexpr int GRID_WIDTH = 60;
constexpr int GRID_HEIGHT = 25;

// ============================================================
// SIMULATION PARAMETERS
// ============================================================
constexpr int POPULATION_SIZE = 100;
constexpr int MAX_TICKS = 3000;
constexpr int RENDER_DELAY_MS = 50;  // Delay between frames

// ============================================================
// AGENT DISTRIBUTION (based on personality literature)
// ============================================================
constexpr float DARK_AGENT_RATIO = 0.15f;    // 15% Dark Agents
constexpr float TOXIC_AGENT_RATIO = 0.10f;   // 10% Toxic Agents
// Remaining 75% are Normal Agents

// ============================================================
// PERSONALITY THRESHOLDS (H1a-c criteria)
// ============================================================
constexpr float S_AGENCY_THRESHOLD = 0.70f;  // High S_Agency
constexpr float G_THRESHOLD = 0.70f;         // High G-factor

// ============================================================
// BEHAVIORAL COSTS
// ============================================================
constexpr float MOVE_COST = 1.0f;
constexpr float WAIT_COST = 0.5f;
constexpr float RULE_BREAKING_COST = 10.0f;
constexpr float SABOTAGE_COST = 5.0f;
constexpr float DETECTION_PENALTY = 20.0f;

// ============================================================
// PROBABILITIES
// ============================================================
constexpr float BASE_DETECTION_PROB = 0.20f;   // 20% base detection
constexpr float WALL_SPAWN_PROBABILITY = 0.15f; // 15% cells are walls

// ============================================================
// INITIAL VALUES
// ============================================================
constexpr float INITIAL_ENERGY = 100.0f;

// ============================================================
// VISUAL CONFIGURATION
// ============================================================
constexpr char CHAR_EMPTY = ' ';
constexpr char CHAR_WALL = '#';
constexpr char CHAR_GOAL = '*';
constexpr char CHAR_DARK_AGENT = 'D';
constexpr char CHAR_TOXIC_AGENT = 'T';
constexpr char CHAR_NORMAL_AGENT = 'N';
constexpr char CHAR_INNOVATION_TRAIL = '+';
constexpr char CHAR_DAMAGE_TRAIL = 'x';

// ANSI Color codes
const std::string COLOR_RESET = "\033[0m";
const std::string COLOR_GREEN = "\033[32m";    // Dark Agent
const std::string COLOR_RED = "\033[31m";      // Toxic Agent
const std::string COLOR_BLUE = "\033[34m";     // Normal Agent
const std::string COLOR_YELLOW = "\033[33m";   // Wall
const std::string COLOR_CYAN = "\033[36m";     // Goal
const std::string COLOR_MAGENTA = "\033[35m";  // Innovation

// ============================================================
// OUTPUT FILES
// ============================================================
const std::string OUTPUT_DIR = "output/";
const std::string LOG_FILE = "simulation_log.csv";
const std::string REPORT_FILE = "final_report.txt";

} // namespace config
