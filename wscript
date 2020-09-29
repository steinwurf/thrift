#! /usr/bin/env python
# encoding: utf-8

import os
from waflib import Task, TaskGen

APPNAME = 'thrift'
VERSION = '1.0.0'


def configure(conf):
    if conf.is_mkspec_platform('linux') and not conf.env['LIB_PTHREAD']:
        conf.check_cxx(lib='pthread')


def build(bld):
    bld.env.append_unique(
        'DEFINES_STEINWURF_VERSION',
        'STEINWURF_THRIFT_VERSION="{}"'.format(VERSION))

    use_flags = []
    if bld.is_mkspec_platform('linux'):
        use_flags += ['PTHREAD']

    # Path to the thrift repo
    thrift_path = bld.dependency_node("thrift")

    # Create system include for thrift
    # bld(name='thrift_includes', export_includes=thrift_path.find_dir('lib/cpp').abspath())
    # use_flags += ['thrift_includes']

    # C++ source files
    library_path = thrift_path.find_dir('lib/cpp/src')

    sources = thrift_path.ant_glob(
        ['lib/cpp/src/thrift/TApplicationException.cpp',
         'lib/cpp/src/thrift/TOutput.cpp',
         'lib/cpp/src/thrift/async/TAsyncChannel.cpp',
         'lib/cpp/src/thrift/async/TAsyncProtocolProcessor.cpp',
         'lib/cpp/src/thrift/async/TConcurrentClientSyncInfo.cpp',
         'lib/cpp/src/thrift/concurrency/ThreadManager.cpp',
         'lib/cpp/src/thrift/concurrency/TimerManager.cpp',
         'lib/cpp/src/thrift/processor/PeekProcessor.cpp',
         'lib/cpp/src/thrift/protocol/TBase64Utils.cpp',
         'lib/cpp/src/thrift/protocol/TDebugProtocol.cpp',
         'lib/cpp/src/thrift/protocol/TJSONProtocol.cpp',
         'lib/cpp/src/thrift/protocol/TMultiplexedProtocol.cpp',
         'lib/cpp/src/thrift/protocol/TProtocol.cpp',
         'lib/cpp/src/thrift/transport/TTransportException.cpp',
         'lib/cpp/src/thrift/transport/TFDTransport.cpp',
         'lib/cpp/src/thrift/transport/TSimpleFileTransport.cpp',
         'lib/cpp/src/thrift/transport/THttpTransport.cpp',
         'lib/cpp/src/thrift/transport/THttpClient.cpp',
         'lib/cpp/src/thrift/transport/THttpServer.cpp',
         'lib/cpp/src/thrift/transport/TSocket.cpp',
         'lib/cpp/src/thrift/transport/TSocketPool.cpp',
         'lib/cpp/src/thrift/transport/TServerSocket.cpp',
         'lib/cpp/src/thrift/transport/TTransportUtils.cpp',
         'lib/cpp/src/thrift/transport/TBufferTransports.cpp',
         'lib/cpp/src/thrift/transport/TWebSocketServer.h',
         'lib/cpp/src/thrift/transport/TWebSocketServer.cpp',
         'lib/cpp/src/thrift/transport/SocketCommon.cpp',
         'lib/cpp/src/thrift/server/TConnectedClient.cpp',
         'lib/cpp/src/thrift/server/TServerFramework.cpp',
         'lib/cpp/src/thrift/server/TSimpleServer.cpp',
         'lib/cpp/src/thrift/server/TThreadPoolServer.cpp',
         'lib/cpp/src/thrift/server/TThreadedServer.cpp'])

    # Build static library if this is top-level, otherwise just .o files
    features = ['cxx']
    if bld.is_toplevel():
        features += ['cxxstlib']

    bld(features=features,
        source=sources,
        includes=[library_path.abspath(), 'src'],
        target='thrift',
        use=use_flags + ['boost_includes'],
        export_includes=[library_path])

    # Would like to build thrift's own tests - however our Boost does
    # not ship with Boost test which is a requirement. We should fix this
    # and build the tests at some point.
    #
    #
    # if bld.is_toplevel():
    #     # Only build tests when executed from the top-level wscript,
    #     # i.e. not when included as a dependency

    #     test_sources = thrift_path.ant_glob(
    #         ['lib/cpp/test/UnitTestMain.cpp'])

    #     bld.program(
    #         features='cxx test',
    #         source=test_sources,
    #         target='thrift_tests',
    #         use=['boost_includes', 'thrift'])
