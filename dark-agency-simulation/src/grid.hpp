#pragma once

/**
 * @file grid.hpp
 * @brief Grid class representing the institutional environment
 * 
 * The grid is a 2D matrix where:
 * - EMPTY cells represent normal bureaucracy
 * - WALL cells represent institutional voids (barriers)
 * - GOAL cells represent innovation opportunities
 */

#include <vector>
#include <utility>
#include "cell.hpp"
#include "config.hpp"
#include "random.hpp"

class Grid {
private:
    std::vector<std::vector<Cell>> cells;
    int width;
    int height;
    std::vector<std::pair<int, int>> goalPositions;
    
public:
    Grid(int w = config::GRID_WIDTH, int h = config::GRID_HEIGHT)
        : width(w), height(h) {
        cells.resize(height, std::vector<Cell>(width, Cell::EMPTY));
    }
    
    // Getters
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    
    // Cell access
    Cell getCell(int x, int y) const {
        if (x < 0 || x >= width || y < 0 || y >= height) {
            return Cell::WALL;  // Out of bounds = wall
        }
        return cells[y][x];
    }
    
    void setCell(int x, int y, Cell cell) {
        if (x >= 0 && x < width && y >= 0 && y < height) {
            cells[y][x] = cell;
        }
    }
    
    // Query functions
    bool hasWall(int x, int y) const {
        return getCell(x, y) == Cell::WALL;
    }
    
    bool isGoal(int x, int y) const {
        return getCell(x, y) == Cell::GOAL;
    }
    
    bool isPassable(int x, int y) const {
        Cell c = getCell(x, y);
        return c == Cell::EMPTY || c == Cell::GOAL || 
               c == Cell::INNOVATION_TRAIL || c == Cell::DAMAGE_TRAIL;
    }
    
    bool inBounds(int x, int y) const {
        return x >= 0 && x < width && y >= 0 && y < height;
    }
    
    // Find nearest goal from position
    float distanceToNearestGoal(int x, int y) const {
        float minDist = 9999.0f;
        for (const auto& goal : goalPositions) {
            float dx = static_cast<float>(goal.first - x);
            float dy = static_cast<float>(goal.second - y);
            float dist = std::sqrt(dx*dx + dy*dy);
            if (dist < minDist) minDist = dist;
        }
        return minDist;
    }
    
    // Direction to nearest goal
    std::pair<int, int> directionToGoal(int x, int y) const {
        if (goalPositions.empty()) return {0, 0};
        
        float minDist = 9999.0f;
        std::pair<int, int> nearest = goalPositions[0];
        
        for (const auto& goal : goalPositions) {
            float dx = static_cast<float>(goal.first - x);
            float dy = static_cast<float>(goal.second - y);
            float dist = std::sqrt(dx*dx + dy*dy);
            if (dist < minDist) {
                minDist = dist;
                nearest = goal;
            }
        }
        
        int dirX = (nearest.first > x) ? 1 : (nearest.first < x) ? -1 : 0;
        int dirY = (nearest.second > y) ? 1 : (nearest.second < y) ? -1 : 0;
        
        return {dirX, dirY};
    }
    
    // Generate random walls (institutional voids)
    void generateWalls(float probability = config::WALL_SPAWN_PROBABILITY) {
        for (int y = 1; y < height - 1; y++) {
            for (int x = 1; x < width - 1; x++) {
                if (globalRng.chance(probability)) {
                    cells[y][x] = Cell::WALL;
                }
            }
        }
        
        // Create some structured wall patterns (bureaucratic barriers)
        createBureaucraticBarriers();
    }
    
    // Place goals on the right side of the grid
    void placeGoals(int count = 5) {
        goalPositions.clear();
        for (int i = 0; i < count; i++) {
            int x = width - 2;  // Near right edge
            int y = globalRng.uniformInt(1, height - 2);
            cells[y][x] = Cell::GOAL;
            goalPositions.push_back({x, y});
        }
    }
    
    // Clear spawn area on the left
    void clearSpawnArea() {
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < 5; x++) {
                if (cells[y][x] == Cell::WALL) {
                    cells[y][x] = Cell::EMPTY;
                }
            }
        }
    }
    
    const std::vector<std::pair<int, int>>& getGoalPositions() const {
        return goalPositions;
    }
    
private:
    // Create vertical barriers representing bureaucratic walls
    void createBureaucraticBarriers() {
        // Create 3-4 vertical barriers with gaps
        int numBarriers = globalRng.uniformInt(3, 4);
        int spacing = width / (numBarriers + 1);
        
        for (int i = 1; i <= numBarriers; i++) {
            int barrierX = i * spacing;
            
            // Create barrier with 1-2 gaps (opportunities to pass)
            int gapCount = globalRng.uniformInt(1, 2);
            std::vector<int> gaps;
            for (int g = 0; g < gapCount; g++) {
                gaps.push_back(globalRng.uniformInt(2, height - 3));
            }
            
            for (int y = 1; y < height - 1; y++) {
                bool isGap = false;
                for (int gap : gaps) {
                    if (std::abs(y - gap) <= 1) {  // Gap of 3 cells
                        isGap = true;
                        break;
                    }
                }
                if (!isGap) {
                    cells[y][barrierX] = Cell::WALL;
                }
            }
        }
    }
};
