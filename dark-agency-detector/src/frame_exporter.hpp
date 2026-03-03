#pragma once

/**
 * @file frame_exporter.hpp
 * @brief PPM image exporter for GIF animation generation
 * 
 * Exports simulation frames as PPM images that can be
 * converted to GIF using ImageMagick or Python
 */

#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>
#include <vector>
#include "config.hpp"
#include "grid.hpp"
#include "agent.hpp"

class FrameExporter {
private:
    int frameCount;
    int imageWidth;
    int imageHeight;
    std::vector<std::vector<config::Color>> buffer;
    
public:
    FrameExporter()
        : frameCount(0)
        , imageWidth(config::GRID_WIDTH * config::CELL_SIZE)
        , imageHeight(config::GRID_HEIGHT * config::CELL_SIZE)
    {
        // Initialize buffer
        buffer.resize(imageHeight, 
                      std::vector<config::Color>(imageWidth, config::COLOR_EMPTY));
    }
    
    void reset() {
        frameCount = 0;
    }
    
    /**
     * Render grid and agents to PPM file
     */
    void exportFrame(const Grid& grid, const std::vector<Agent>& agents,
                     int tick, const std::string& prefix = config::FRAMES_DIR) {
        // Clear buffer
        for (auto& row : buffer) {
            for (auto& pixel : row) {
                pixel = config::COLOR_EMPTY;
            }
        }
        
        // Draw grid
        for (int gy = 0; gy < grid.getHeight(); gy++) {
            for (int gx = 0; gx < grid.getWidth(); gx++) {
                config::Color cellColor;
                
                switch (grid.getCell(gx, gy)) {
                    case CellType::WALL:
                        cellColor = config::COLOR_WALL;
                        break;
                    case CellType::GOAL:
                        cellColor = config::COLOR_GOAL;
                        break;
                    case CellType::INNOVATION_TRAIL:
                        cellColor = config::COLOR_INNOVATION_TRAIL;
                        break;
                    case CellType::DAMAGE_TRAIL:
                        cellColor = config::COLOR_DAMAGE_TRAIL;
                        break;
                    default:
                        cellColor = config::COLOR_EMPTY;
                        break;
                }
                
                fillCell(gx, gy, cellColor);
            }
        }
        
        // Draw agents
        for (const Agent& agent : agents) {
            if (agent.isAlive()) {
                drawAgent(agent.getX(), agent.getY(), agent.getColor());
            }
        }
        
        // Save to file
        std::stringstream filename;
        filename << prefix << "frame_" << std::setfill('0') << std::setw(5) << frameCount << ".ppm";
        savePPM(filename.str());
        
        frameCount++;
    }
    
    int getFrameCount() const { return frameCount; }
    
private:
    void fillCell(int gx, int gy, const config::Color& color) {
        int startX = gx * config::CELL_SIZE;
        int startY = gy * config::CELL_SIZE;
        
        for (int py = 0; py < config::CELL_SIZE; py++) {
            for (int px = 0; px < config::CELL_SIZE; px++) {
                int imgX = startX + px;
                int imgY = startY + py;
                if (imgX >= 0 && imgX < imageWidth && imgY >= 0 && imgY < imageHeight) {
                    buffer[imgY][imgX] = color;
                }
            }
        }
    }
    
    void drawAgent(int gx, int gy, const config::Color& color) {
        int centerX = gx * config::CELL_SIZE + config::CELL_SIZE / 2;
        int centerY = gy * config::CELL_SIZE + config::CELL_SIZE / 2;
        int radius = config::CELL_SIZE / 2 - 1;
        
        // Draw filled circle
        for (int py = -radius; py <= radius; py++) {
            for (int px = -radius; px <= radius; px++) {
                if (px*px + py*py <= radius*radius) {
                    int imgX = centerX + px;
                    int imgY = centerY + py;
                    if (imgX >= 0 && imgX < imageWidth && imgY >= 0 && imgY < imageHeight) {
                        buffer[imgY][imgX] = color;
                    }
                }
            }
        }
    }
    
    void savePPM(const std::string& filename) {
        std::ofstream file(filename, std::ios::binary);
        if (!file.is_open()) return;
        
        // PPM header
        file << "P6\n" << imageWidth << " " << imageHeight << "\n255\n";
        
        // Pixel data
        for (int y = 0; y < imageHeight; y++) {
            for (int x = 0; x < imageWidth; x++) {
                const auto& c = buffer[y][x];
                file.put(static_cast<char>(c.r));
                file.put(static_cast<char>(c.g));
                file.put(static_cast<char>(c.b));
            }
        }
        
        file.close();
    }
};
