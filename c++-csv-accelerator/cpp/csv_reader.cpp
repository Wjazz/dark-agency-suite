// csv_reader.cpp - minimal high-performance numeric CSV reader
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <cmath>

std::vector<double> parse_numeric_column(const std::string &path, size_t column_index, char delim=',') {
    std::ifstream in(path);
    std::string line;
    std::vector<double> out;
    out.reserve(1000000);
    if (!std::getline(in, line)) return out; // saltar header
    while (std::getline(in, line)) {
        const char* s = line.c_str();
        size_t len = line.size();
        size_t col = 0;
        const char* start = s;
        for (size_t i=0; i<=len; i++) {
            if (i==len || s[i]==delim) {
                if (col==column_index) {
                    std::string token(start, s + i);
                    try {
                        out.push_back(std::stod(token));
                    } catch(...) {
                        out.push_back(NAN);
                    }
                    break;
                }
                col++;
                start = s + i + 1;
            }
        }
    }
    return out;
}
