cmake_minimum_required(VERSION 3.4)
project(thrift)
set(thrift_VERSION "0.15.0")

# Use waf to resolve dependencies
find_package(Python COMPONENTS Interpreter)
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

# Paths
set(THRIFT_SOURCEFORK_DIR "${STEINWURF_RESOLVE}/thrift-source/lib/cpp")

# Boost
if (NOT TARGET steinwurf::boost)
    # Add to include path to the resolved boost dependency to enable cmake to use
    # the same header files as the waf build system.
    add_library(boost INTERFACE)

    target_include_directories(boost INTERFACE "${STEINWURF_RESOLVE}/boost")
    target_compile_definitions(
            boost INTERFACE BOOST_ALL_NO_LIB=1 BOOST_DETAIL_NO_CONTAINER_FWD
            BOOST_SYSTEM_NO_DEPRECATED BOOST_NO_AUTO_PTR)
    add_library(steinwurf::boost ALIAS boost)
endif ()

# SYSLIBS contains libraries that need to be linked to all lib targets
set(SYSLIBS boost)

# Create the thrift C++ library
set(thriftcpp_SOURCES
        src/thrift/TApplicationException.cpp
        src/thrift/TOutput.cpp
        src/thrift/async/TAsyncChannel.cpp
        src/thrift/async/TAsyncProtocolProcessor.cpp
        src/thrift/async/TConcurrentClientSyncInfo.h
        src/thrift/async/TConcurrentClientSyncInfo.cpp
        src/thrift/concurrency/ThreadManager.cpp
        src/thrift/concurrency/TimerManager.cpp
        src/thrift/processor/PeekProcessor.cpp
        src/thrift/protocol/TBase64Utils.cpp
        src/thrift/protocol/TDebugProtocol.cpp
        src/thrift/protocol/TJSONProtocol.cpp
        src/thrift/protocol/TMultiplexedProtocol.cpp
        src/thrift/protocol/TProtocol.cpp
        src/thrift/transport/TTransportException.cpp
        src/thrift/transport/TFDTransport.cpp
        src/thrift/transport/TSimpleFileTransport.cpp
        src/thrift/transport/THttpTransport.cpp
        src/thrift/transport/THttpClient.cpp
        src/thrift/transport/THttpServer.cpp
        src/thrift/transport/TSocket.cpp
        src/thrift/transport/TSocketPool.cpp
        src/thrift/transport/TServerSocket.cpp
        src/thrift/transport/TTransportUtils.cpp
        src/thrift/transport/TBufferTransports.cpp
        src/thrift/transport/SocketCommon.cpp
        src/thrift/server/TConnectedClient.cpp
        src/thrift/server/TServerFramework.cpp
        src/thrift/server/TSimpleServer.cpp
        src/thrift/server/TThreadPoolServer.cpp
        src/thrift/server/TThreadedServer.cpp
        src/thrift/concurrency/ThreadFactory.cpp
        src/thrift/concurrency/Thread.cpp
        src/thrift/concurrency/Monitor.cpp
        src/thrift/concurrency/Mutex.cpp
        )

# These files don't work on Windows CE as there is no pipe support
if (NOT WINCE)
    list(APPEND thriftcpp_SOURCES
            src/thrift/transport/TPipe.cpp
            src/thrift/transport/TPipeServer.cpp
            src/thrift/transport/TFileTransport.cpp
            )
endif()

# OS dependencies
if (WIN32)
    list(APPEND thriftcpp_SOURCES
            src/thrift/windows/TWinsockSingleton.cpp
            src/thrift/windows/SocketPair.cpp
            src/thrift/windows/GetTimeOfDay.cpp
            src/thrift/windows/WinFcntl.cpp
            )
    if(NOT WINCE)
        # This file uses pipes so it currently won't work on Windows CE
        list(APPEND thriftcpp_SOURCES
                src/thrift/windows/OverlappedSubmissionThread.cpp
                )
    endif()
else()
    # These files evaluate to nothing on Windows, so omit them from the
    # Windows build
    list(APPEND thriftcpp_SOURCES
            src/thrift/VirtualProfiling.cpp
            src/thrift/server/TServer.cpp
            )
endif()

# Threading support
if(UNIX)
    if(ANDROID)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
    else()
        list(APPEND SYSLIBS pthread)
    endif()
endif()

# Add resolve path for all sources
list(TRANSFORM thriftcpp_SOURCES PREPEND ${THRIFT_SOURCEFORK_DIR}/)

# Library target
add_library(thrift ${thriftcpp_SOURCES})
add_library(steinwurf::thrift ALIAS thrift)
set_target_properties(thrift PROPERTIES
        OUTPUT_NAME thrift
        VERSION ${thrift_VERSION}
        CXX_STANDARD 14)
add_definitions("-DTHRIFT_STATIC_DEFINE")

# Dependencies
target_link_libraries(thrift PUBLIC ${SYSLIBS})

# Includes
target_include_directories(thrift PRIVATE ${THRIFT_SOURCEFORK_DIR}/src)
target_include_directories(thrift PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/lib)

# Include interfaces
target_include_directories(thrift INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/lib>)
target_include_directories(thrift INTERFACE $<BUILD_INTERFACE:${THRIFT_SOURCEFORK_DIR}/src>)
