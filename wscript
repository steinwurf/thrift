#! /usr/bin/env python
# encoding: utf-8

import os
from waflib import Task, TaskGen
from waflib.TaskGen import extension
from waflib.TaskGen import feature
from waflib.TaskGen import after_method

APPNAME = 'thrift'
VERSION = '1.0.0'


class bison(Task.Task):
    """Compiles bison files"""
    color = 'BLUE'
    run_str = '${BISON} ${BISONFLAGS} ${SRC[0].abspath()} -o ${TGT[0].abspath()}'
    ext_out = ['.h']  # just to make sure


class flex(Task.Task):
    """Compiles flex files"""
    color = 'BLUE'
    run_str = '${FLEX} -o ${TGT[0].abspath()} ${SRC[0].abspath()}'
    ext_out = ['.h']  # just to make sure


# class move_thrifty(Task.Task):
#     """Compiles flex files"""
#     color = 'BLUE'
#     after = ['bison']
#     always_run = True

#     def run(self):
#         print("HELLO")
#         assert 0

#         # dst = self.path.get_bld().make_node('thrift/thrifty.hh')
#         # src = self.path.get_bld().find_node('thrifty.hh')

#         # print(self.path.get_bld())

#         # dst.write(src.read())


@extension('.yy')
def run_bison(self, node):
    """
    Creates a bison task, which must be executed from the directory of the output file.
    """
    cpp_file = self.path.get_bld().find_or_declare(node.change_ext('.cc').name)
    hpp_file = self.path.get_bld().find_or_declare(node.change_ext('.hh').name)

    self.create_task('bison', node, [cpp_file, hpp_file])
    self.source.append(cpp_file)


@extension('.ll')
def run_flex(self, node):
    """
    Creates a flex task, which must be executed from the directory of the output file.
    """

    cpp_file = self.path.get_bld().find_or_declare(node.change_ext('.cc').name)

    self.create_task('flex', node, [cpp_file])
    self.source.append(cpp_file)


@feature('cxx')
@after_method('apply_incpaths')
def insert_blddir(self):
    self.env.prepend_value('INCPATHS', '.')


def configure(conf):
    if conf.is_mkspec_platform('linux') and not conf.env['LIB_PTHREAD']:
        conf.check_cxx(lib='pthread')

    if True:  # opt.enable_compiler

        # errmsg = """not found, is available in the following packages:
        #     Debian/Ubuntu: apt install bison
        # """
        # conf.find_program('bison', errmsg=errmsg)
        conf.find_program('bison', var='BISON')
        conf.env.BISONFLAGS = ['-d']

        errmsg = """not found, is available in the following packages:
                    Debian/Ubuntu: apt install flex
                """
        conf.find_program('flex', errmsg=errmsg)


def build(bld):
    # bld.env.append_unique(
    #     'DEFINES_STEINWURF_VERSION',
    #     'STEINWURF_THRIFT_VERSION="{}"'.format(VERSION))

    # use_flags = []
    # if bld.is_mkspec_platform('linux'):
    #     use_flags += ['PTHREAD']

    # Path to the thrift repo
    thrift_path = bld.dependency_node("thrift")

    # # Create system include for thrift
    # # bld(name='thrift_includes', export_includes=thrift_path.find_dir('lib/cpp').abspath())
    # # use_flags += ['thrift_includes']

    # # C++ source files
    # library_path = thrift_path.find_dir('lib/cpp/src')

    # sources = thrift_path.ant_glob(
    #     ['lib/cpp/src/thrift/TApplicationException.cpp',
    #      'lib/cpp/src/thrift/TOutput.cpp',
    #      'lib/cpp/src/thrift/async/TAsyncChannel.cpp',
    #      'lib/cpp/src/thrift/async/TAsyncProtocolProcessor.cpp',
    #      'lib/cpp/src/thrift/async/TConcurrentClientSyncInfo.cpp',
    #      'lib/cpp/src/thrift/concurrency/ThreadManager.cpp',
    #      'lib/cpp/src/thrift/concurrency/TimerManager.cpp',
    #      'lib/cpp/src/thrift/processor/PeekProcessor.cpp',
    #      'lib/cpp/src/thrift/protocol/TBase64Utils.cpp',
    #      'lib/cpp/src/thrift/protocol/TDebugProtocol.cpp',
    #      'lib/cpp/src/thrift/protocol/TJSONProtocol.cpp',
    #      'lib/cpp/src/thrift/protocol/TMultiplexedProtocol.cpp',
    #      'lib/cpp/src/thrift/protocol/TProtocol.cpp',
    #      'lib/cpp/src/thrift/transport/TTransportException.cpp',
    #      'lib/cpp/src/thrift/transport/TFDTransport.cpp',
    #      'lib/cpp/src/thrift/transport/TSimpleFileTransport.cpp',
    #      'lib/cpp/src/thrift/transport/THttpTransport.cpp',
    #      'lib/cpp/src/thrift/transport/THttpClient.cpp',
    #      'lib/cpp/src/thrift/transport/THttpServer.cpp',
    #      'lib/cpp/src/thrift/transport/TSocket.cpp',
    #      'lib/cpp/src/thrift/transport/TSocketPool.cpp',
    #      'lib/cpp/src/thrift/transport/TServerSocket.cpp',
    #      'lib/cpp/src/thrift/transport/TTransportUtils.cpp',
    #      'lib/cpp/src/thrift/transport/TBufferTransports.cpp',
    #      'lib/cpp/src/thrift/transport/TWebSocketServer.h',
    #      'lib/cpp/src/thrift/transport/TWebSocketServer.cpp',
    #      'lib/cpp/src/thrift/transport/SocketCommon.cpp',
    #      'lib/cpp/src/thrift/server/TConnectedClient.cpp',
    #      'lib/cpp/src/thrift/server/TServerFramework.cpp',
    #      'lib/cpp/src/thrift/server/TSimpleServer.cpp',
    #      'lib/cpp/src/thrift/server/TThreadPoolServer.cpp',
    #      'lib/cpp/src/thrift/server/TThreadedServer.cpp'])

    # # Build static library if this is top-level, otherwise just .o files
    # features = ['cxx']
    # if bld.is_toplevel():
    #     features += ['cxxstlib']

    # bld(features=features,
    #     source=sources,
    #     includes=[library_path.abspath(), 'lib'],
    #     target='thrift',
    #     use=use_flags + ['boost_includes'],
    #     export_includes=[library_path])

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

    compiler_path = thrift_path.find_dir('compiler/cpp/src')

    # tsk = move_thrifty(env=bld.env)
    # bld.add_to_group(tsk)

    bld(features='cxx cxxprogram',
        name='compiler',
        source=compiler_path.ant_glob(
            '**/*.cc') + compiler_path.ant_glob('**/*.yy') + compiler_path.ant_glob('**/*.ll'),
        includes=[compiler_path.abspath(), 'compiler'],
        target='thrift')
