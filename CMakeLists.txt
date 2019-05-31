cmake_minimum_required(VERSION 3.11)

find_package(benchmark REQUIRED)

project(granite CXX)

add_executable(granite bench/main.cpp)

target_compile_features(granite PUBLIC cxx_std_17)

target_link_libraries(granite PUBLIC benchmark pthread)


