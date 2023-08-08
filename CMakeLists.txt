cmake_minimum_required(VERSION 3.10)

# set the project name
project(CoCBuilderBaseBot)

add_subdirectory(pybind11)

pybind11_add_module(LineComputation LineComputation.cpp)

# Configure project to inject source path as include directory on dependent projects
target_include_directories( LineComputation
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/pybind11/include/> )

set_target_properties( LineComputation
  PROPERTIES
  CXX_STANDARD 17
  CXX_STANDARD_REQUIRED ON
  PREFIX ""
)
