cmake_minimum_required(VERSION 3.14)
project(csv_accel)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native -flto")

find_package(pybind11 REQUIRED)
pybind11_add_module(csv_accel pybind_module.cpp csv_reader.cpp)
