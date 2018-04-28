PROJECT(Speed_Evaluate)

CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
#set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
#include_directories(${CMAKE_CURRENT_SOURCE_DIR})
#message(STATUS "    cmake_dir: ${CMAKE_SOURCE_DIR}")
#message(STATUS "    cmake_current_dir: ${CMAKE_CURRENT_SOURCE_DIR}")

set(OpenCV_DIR /usr/local/share/OpenCV)
FIND_PACKAGE( OpenCV REQUIRED )
message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")

set(CMAKE_CXX_STANDARD 11)
list(APPEND CMAKE_CXX_FLAGS "-pthread")

SET(CMAKE_BUILD_TYPE "Debug")

ADD_EXECUTABLE(Speed_Evaluate thread_test.cpp)

TARGET_LINK_LIBRARIES(Speed_Evaluate ${OpenCV_LIBS})
