#pragma once

/**
 * @file cell.hpp
 * @brief Cell types for the simulation grid
 * 
 * Represents the institutional environment:
 * - EMPTY: Normal bureaucracy (passable)
 * - WALL: Institutional void (barrier requiring transgression)
 * - GOAL: Innovation target (generates EIB when reached)
 */

enum class Cell {
    EMPTY,              // Normal space (burocracia normal)
    WALL,               // Institutional void (barrera burocrática)
    GOAL,               // Innovation target (meta de innovación)
    INNOVATION_TRAIL,   // Left by Dark Agents who innovated
    DAMAGE_TRAIL        // Left by Toxic Agents who sabotaged
};
