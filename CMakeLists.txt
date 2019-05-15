cmake_minimum_required(VERSION 3.11)

project(granite CXX)

add_library(granite INTERFACE)

target_compile_features(granite INTERFACE cxx_std_14)

