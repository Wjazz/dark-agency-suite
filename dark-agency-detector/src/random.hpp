#pragma once

/**
 * @file random.hpp
 * @brief Random number generation utilities
 */

#include <random>
#include <chrono>

class RandomGenerator {
private:
    std::mt19937 rng;
    
public:
    RandomGenerator() {
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        rng.seed(seed);
    }
    
    void seed(unsigned s) { rng.seed(s); }
    
    float uniform(float min, float max) {
        std::uniform_real_distribution<float> dist(min, max);
        return dist(rng);
    }
    
    int uniformInt(int min, int max) {
        std::uniform_int_distribution<int> dist(min, max);
        return dist(rng);
    }
    
    bool chance(float p) {
        return uniform(0.0f, 1.0f) < p;
    }
    
    float normal(float mean, float stddev) {
        std::normal_distribution<float> dist(mean, stddev);
        return dist(rng);
    }
    
    float normalClamped(float mean, float stddev, float min = 0.0f, float max = 1.0f) {
        float val = normal(mean, stddev);
        if (val < min) return min;
        if (val > max) return max;
        return val;
    }
};

inline RandomGenerator rng;
