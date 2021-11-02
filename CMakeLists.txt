cmake_minimum_required(VERSION 3.4)
project(thrift)

find_package(Python COMPONENTS Interpreter)

# Use waf to resolve dependencies
if (NOT DEFINED STEINWURF_RESOLVE)
    message(STATUS "Resolving dependencies...")
    execute_process(
            COMMAND ${Python_EXECUTABLE} waf resolve ${STEINWURF_RESOLVE_OPTIONS}
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            RESULT_VARIABLE STATUS)
    if (STATUS AND NOT STATUS EQUAL 0)
        message(FATAL_ERROR "Failed: ${STATUS}")
    endif ()
    set(STEINWURF_RESOLVE "${CMAKE_CURRENT_SOURCE_DIR}/resolve_symlinks")
    set(STEINWURF_TOP_NAME ${PROJECT_NAME})
endif ()

# Set required thrift targets
option(BUILD_CPP "" ON)
option(BUILD_JAVA "" OFF)
option(BUILD_JAVASCRIPT "" OFF)
option(BUILD_NODEJS "" OFF)
option(BUILD_PYTHON "" OFF)
option(BUILD_HASKELL "" OFF)
option(BUILD_COMPILER "" OFF)
option(BUILD_TUTORIALS "" OFF)
option(BUILD_TESTING "" OFF)

# Set cpp library options
set(BOOST_ROOT "${STEINWURF_RESOLVE}/boost")
message(STATUS "BOOST_ROOT: ${BOOST_ROOT}")
option(WITH_LIBEVENT "" OFF)
option(WITH_ZLIB "" OFF)
option(WITH_QT5 "" OFF)

# Option for thrift ssl support
option(THRIFT_SSL_SUPPORT "Enable SSL support for thrift" OFF)
if(THRIFT_SSL_SUPPORT)
    option(WITH_SSL "" OFF)
endif ()

# Add the thrift CMakeLists.txt
add_subdirectory("${STEINWURF_RESOLVE}/thrift-source" thrift EXCLUDE_FROM_ALL)

# Header files
target_include_directories(thrift PUBLIC
    $<BUILD_INTERFACE:${STEINWURF_RESOLVE}/thrift-source/lib/cpp/src>
)
target_include_directories(thrift PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/lib>
)

# Steinwurf target alias
add_library(steinwurf::thrift ALIAS thrift)