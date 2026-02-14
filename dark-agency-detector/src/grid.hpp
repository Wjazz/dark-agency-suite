#pragma once

/**
 * @file grid.hpp
 * @brief Organizational environment grid
 */

#include <vector>
#include <cmath>
#include "config.hpp"
#include "random.hpp"

enum class CellType {
    EMPTY,
    WALL,              // Institutional void / Bureaucratic barrier
    GOAL,              // Innovation target
    INNOVATION_TRAIL,  // Left by Dark Innovators
    DAMAGE_TRAIL       // Left by Toxic agents
};

class Grid {
private:
    std::vector<std::vector<CellType>> cells;
    int width, height;
    std::vector<std::pair<int, int>> goals;
    
public:
    Grid(int w = config::GRID_WIDTH, int h = config::GRID_HEIGHT)
        : width(w), height(h) {
        cells.resize(height, std::vector<CellType>(width, CellType::EMPTY));
    }
    
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    
    CellType getCell(int x, int y) const {
        if (x < 0 || x >= width || y < 0 || y >= height) return CellType::WALL;
        return cells[y][x];
    }
    
    void setCell(int x, int y, CellType type) {
        if (x >= 0 && x < width && y >= 0 && y < height) {
            cells[y][x] = type;
        }
    }
    
    bool isPassable(int x, int y) const {
        CellType c = getCell(x, y);
        return c != CellType::WALL;
    }
    
    bool isGoal(int x, int y) const {
        return getCell(x, y) == CellType::GOAL;
    }
    
    void generateEnvironment() {
        // Create vertical bureaucratic barriers
        int numBarriers = 4;
        int spacing = width / (numBarriers + 1);
        
        for (int b = 1; b <= numBarriers; b++) {
            int x = b * spacing;
            
            // Create barrier with gaps
            int numGaps = rng.uniformInt(2, 3);
            std::vector<int> gaps;
            for (int g = 0; g < numGaps; g++) {
                gaps.push_back(rng.uniformInt(3, height - 4));
            }
            
            for (int y = 1; y < height - 1; y++) {
                bool isGap = false;
                for (int gap : gaps) {
                    if (std::abs(y - gap) <= 2) {
                        isGap = true;
                        break;
                    }
                }
                if (!isGap) {
                    cells[y][x] = CellType::WALL;
                }
            }
        }
        
        // Add some random scattered walls
        for (int i = 0; i < (width * height) / 20; i++) {
            int x = rng.uniformInt(5, width - 5);
            int y = rng.uniformInt(1, height - 2);
            cells[y][x] = CellType::WALL;
        }
        
        // Clear spawn area
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < 6; x++) {
                cells[y][x] = CellType::EMPTY;
            }
        }
        
        // Place goals on right side
        goals.clear();
        for (int i = 0; i < 5; i++) {
            int x = width - 3;
            int y = (height / 6) * (i + 1);
            cells[y][x] = CellType::GOAL;
            goals.push_back({x, y});
        }
    }
    
    std::pair<int, int> directionToGoal(int x, int y) const {
        if (goals.empty()) return {1, 0};
        
        float minDist = 9999.0f;
        std::pair<int, int> nearest = goals[0];
        
        for (const auto& g : goals) {
            float dx = static_cast<float>(g.first - x);
            float dy = static_cast<float>(g.second - y);
            float dist = std::sqrt(dx*dx + dy*dy);
            if (dist < minDist) {
                minDist = dist;
                nearest = g;
            }
        }
        
        int dirX = (nearest.first > x) ? 1 : (nearest.first < x) ? -1 : 0;
        int dirY = (nearest.second > y) ? 1 : (nearest.second < y) ? -1 : 0;
        
        return {dirX, dirY};
    }
    
    float distanceToGoal(int x, int y) const {
        if (goals.empty()) return 9999.0f;
        
        float minDist = 9999.0f;
        for (const auto& g : goals) {
            float dx = static_cast<float>(g.first - x);
            float dy = static_cast<float>(g.second - y);
            float dist = std::sqrt(dx*dx + dy*dy);
            if (dist < minDist) minDist = dist;
        }
        return minDist;
    }
    
    const std::vector<std::vector<CellType>>& getCells() const { return cells; }
};
