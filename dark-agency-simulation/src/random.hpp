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
    
    // Seed for reproducible results
    void seed(unsigned s) {
        rng.seed(s);
    }
    
    // Uniform float in [min, max]
    float uniform(float min, float max) {
        std::uniform_real_distribution<float> dist(min, max);
        return dist(rng);
    }
    
    // Uniform int in [min, max]
    int uniformInt(int min, int max) {
        std::uniform_int_distribution<int> dist(min, max);
        return dist(rng);
    }
    
    // Bernoulli trial with probability p
    bool chance(float p) {
        return uniform(0.0f, 1.0f) < p;
    }
    
    // Normal distribution
    float normal(float mean, float stddev) {
        std::normal_distribution<float> dist(mean, stddev);
        return dist(rng);
    }
    
    // Clamp normal to [0, 1] for personality traits
    float normalClamped(float mean, float stddev) {
        float val = normal(mean, stddev);
        if (val < 0.0f) return 0.0f;
        if (val > 1.0f) return 1.0f;
        return val;
    }
};

// Global random generator
inline RandomGenerator globalRng;
