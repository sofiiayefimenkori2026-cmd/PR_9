cmake_minimum_required(VERSION 3.15)
project(Lab_09 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(PR_9.1 PR_9.2_1)

# Source programs
add_executable(Lab_09_1 PR_9.1/var.cpp PR_9.1/dod.cpp PR_9.1/sum.cpp PR_9.1/Lab_09_1.cpp)

add_executable(Lab_09_2_1_b1 PR_9.2_1/Lab_09_2_1.cpp)
target_compile_definitions(Lab_09_2_1_b1 PRIVATE Z=15)

add_executable(Lab_09_2_1_b2 PR_9.2_1/Lab_09_2_1.cpp)
target_compile_definitions(Lab_09_2_1_b2 PRIVATE Z=5)

# Testing
enable_testing()

add_executable(UnitTest_09_1 tests/UnitTest_09_1.cpp PR_9.1/var.cpp PR_9.1/dod.cpp PR_9.1/sum.cpp)
target_include_directories(UnitTest_09_1 PRIVATE tests PR_9.1)
add_test(NAME Test_09_1 COMMAND UnitTest_09_1)

add_executable(UnitTest_09_2_1 tests/UnitTest_09_2_1.cpp)
target_include_directories(UnitTest_09_2_1 PRIVATE tests PR_9.2_1)
add_test(NAME Test_09_2_1 COMMAND UnitTest_09_2_1)
