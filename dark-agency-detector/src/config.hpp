#pragma once

/**
 * @file config.hpp
 * @brief Configuration for DarkAgencyDetector inference engine
 * 
 * Enterprise-grade configuration for the Bifactor S-1 model
 */

#include <string>

namespace config {

// ============================================================
// SIMULATION GRID
// ============================================================
constexpr int GRID_WIDTH = 80;
constexpr int GRID_HEIGHT = 40;
constexpr int MAX_TICKS = 500;

// ============================================================
// POPULATION
// ============================================================
constexpr int POPULATION_SIZE = 150;
constexpr float DARK_INNOVATOR_RATIO = 0.12f;  // 12%
constexpr float TOXIC_RATIO = 0.08f;           // 8%
constexpr float MAVERICK_RISK_RATIO = 0.05f;   // 5%
// Remaining 75% are Normal

// ============================================================
// BIFACTOR MODEL THRESHOLDS (from thesis)
// ============================================================
constexpr float G_THRESHOLD_TOXIC = 0.70f;
constexpr float G_THRESHOLD_MAVERICK = 0.50f;
constexpr float S_AGENCY_THRESHOLD = 0.65f;

// Factor loadings for G extraction (based on literature)
constexpr float LOADING_PSYCHOPATHY = 0.45f;
constexpr float LOADING_SADISM = 0.40f;
constexpr float LOADING_MACH = 0.10f;
constexpr float LOADING_NARC = 0.05f;

// ============================================================
// BEHAVIORAL PARAMETERS
// ============================================================
constexpr float INITIAL_ENERGY = 100.0f;
constexpr float MOVE_COST = 0.5f;
constexpr float TRANSGRESSION_COST = 8.0f;
constexpr float SABOTAGE_COST = 3.0f;
constexpr float WAIT_COST = 0.3f;
constexpr float DETECTION_PENALTY = 15.0f;
constexpr float BASE_DETECTION_PROB = 0.15f;

// ============================================================
// VISUALIZATION (PPM export for GIF generation)
// ============================================================
constexpr int CELL_SIZE = 12;  // Pixels per cell
constexpr int FRAME_SKIP = 5;  // Export every N ticks

// Colors (RGB)
struct Color {
    unsigned char r, g, b;
};

// Agent colors
const Color COLOR_DARK_INNOVATOR = {0, 255, 200};    // Cyan
const Color COLOR_TOXIC = {255, 60, 60};              // Red
const Color COLOR_MAVERICK = {255, 200, 0};           // Yellow/Orange
const Color COLOR_NORMAL = {100, 150, 255};           // Blue
const Color COLOR_DEAD = {80, 80, 80};                // Gray

// Environment colors
const Color COLOR_EMPTY = {30, 30, 40};               // Dark gray
const Color COLOR_WALL = {120, 100, 80};              // Brown/bureaucracy
const Color COLOR_GOAL = {0, 255, 100};               // Green/innovation
const Color COLOR_INNOVATION_TRAIL = {100, 0, 200};   // Purple
const Color COLOR_DAMAGE_TRAIL = {150, 0, 0};         // Dark red

// ============================================================
// OUTPUT
// ============================================================
const std::string FRAMES_DIR = "frames/";
const std::string OUTPUT_DIR = "output/";

} // namespace config
