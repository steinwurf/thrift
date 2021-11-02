#!  /usr/bin/env python
# encoding: utf-8
import os
from waflib import Task, TaskGen
from waflib.TaskGen import extension
from waflib.TaskGen import feature
from waflib.TaskGen import after_method

APPNAME = 'thrift'
VERSION = "1.1.0"


class bison(Task.Task):
    """Compiles bison files"""
    color = 'BLUE'
    run_str = '${BISON} ${SRC} --defines=${TGT[1].abspath()} -o ${TGT[0].abspath()}'
    ext_out = ['.h']  # just to make sure


class flex(Task.Task):
    """Compiles flex files"""
    color = 'BLUE'
    run_str = '${FLEX} -o ${TGT[0].abspath()} ${SRC}'
    ext_out = ['.h']  # just to make sure


@extension('.yy')
def run_bison(self, node):
    """
    Creates a bison task, which must be executed from the directory of the output file.
    """
    cpp_file = node.change_ext('.cc').name
    hpp_file = node.change_ext('.hh').name

    cpp_out = node.parent.find_or_declare(cpp_file)
    hpp_out = node.parent.find_or_declare(hpp_file)

    # The .hpp file will be ../compiler/cpp/src/thrift/thrifty.hh we need to
    # set
    # the include path to ../compiler/cpp/src/
    self.includes.append(hpp_out.parent.parent)

    self.create_task('bison', node, [cpp_out, hpp_out])
    self.source.append(cpp_out)


@extension('.ll')
def run_flex(self, node):
    """
    Creates a flex task, which must be executed from the directory of the output file.
    """

    cpp_file = node.change_ext('.cc').name
    cpp_out = node.parent.find_or_declare(cpp_file)

    self.create_task('flex', node, [cpp_out])
    self.source.append(cpp_out)


def options(opt):
    opt.add_option("--thrift_compiler", default=False, action="store_true",
                   help="Build the thrift compiler")


def configure(conf):
    if conf.is_mkspec_platform('linux') and not conf.env['LIB_PTHREAD']:
        conf.check_cxx(lib='pthread')

    # We need bison and flex to build the thrift compiler
    conf.find_program('bison', mandatory=False)
    conf.find_program('flex', mandatory=False)


def build(bld):

    use_flags = []
    if bld.is_mkspec_platform('linux'):
        use_flags += ['PTHREAD']

    bld.env.append_unique('DEFINES_STEINWURF_VERSION',
                          'STEINWURF_THRIFT_VERSION="{}"'.format(VERSION))

    # Path to the thrift repo
    thrift_path = bld.dependency_node("thrift-source")

    # C++ source files
    library_path = thrift_path.find_dir('lib/cpp/src')

    sources = thrift_path.ant_glob(
        ['lib/cpp/src/thrift/TApplicationException.cpp',
         'lib/cpp/src/thrift/TOutput.cpp',
         'lib/cpp/src/thrift/async/TAsyncChannel.cpp',
         'lib/cpp/src/thrift/async/TAsyncProtocolProcessor.cpp',
         'lib/cpp/src/thrift/async/TConcurrentClientSyncInfo.cpp',
         'lib/cpp/src/thrift/concurrency/Monitor.cpp',
         'lib/cpp/src/thrift/concurrency/Mutex.cpp',
         'lib/cpp/src/thrift/concurrency/Thread.cpp',
         'lib/cpp/src/thrift/concurrency/ThreadFactory.cpp',
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
         'lib/cpp/src/thrift/transport/TFileTransport.cpp',
         'lib/cpp/src/thrift/transport/TSimpleFileTransport.cpp',
         'lib/cpp/src/thrift/transport/THttpTransport.cpp',
         'lib/cpp/src/thrift/transport/THttpClient.cpp',
         'lib/cpp/src/thrift/transport/THttpServer.cpp',
         'lib/cpp/src/thrift/transport/TSocket.cpp',
         'lib/cpp/src/thrift/transport/TSocketPool.cpp',
         'lib/cpp/src/thrift/transport/TServerSocket.cpp',
         'lib/cpp/src/thrift/transport/TTransportUtils.cpp',
         'lib/cpp/src/thrift/transport/TBufferTransports.cpp',
         'lib/cpp/src/thrift/transport/SocketCommon.cpp',
         'lib/cpp/src/thrift/server/TConnectedClient.cpp',
         'lib/cpp/src/thrift/server/TServerFramework.cpp',
         'lib/cpp/src/thrift/server/TSimpleServer.cpp',
         'lib/cpp/src/thrift/server/TThreadPoolServer.cpp',
         'lib/cpp/src/thrift/server/TThreadedServer.cpp'])

    if bld.is_mkspec_platform('windows'):
        sources += thrift_path.ant_glob(
            ['lib/cpp/src/thrift/windows/GetTimeOfDay.cpp',
             'lib/cpp/src/thrift/windows/OverlappedSubmissionThread.cpp',
             'lib/cpp/src/thrift/windows/SocketPair.cpp',
             'lib/cpp/src/thrift/windows/TWinsockSingleton.cpp',
             'lib/cpp/src/thrift/windows/WinFcntl.cpp'])

    # Build static library if this is top-level, otherwise just .o files
    features = ['cxx']
    if bld.is_toplevel():
        features += ['cxxstlib']

    bld(features=features,
        source=sources,
        includes=[library_path.abspath(), 'lib'],
        target='thrift',
        defines=['THRIFT_STATIC_DEFINE'],
        export_defines=['THRIFT_STATIC_DEFINE'],
        use=use_flags + ['boost_includes'],
        export_includes=[library_path, 'lib'])

    if bld.is_toplevel():

        bld(features='cxx cxxprogram',
            source=thrift_path.ant_glob(
                'test/cpp/src/StressTest.cpp') + bld.path.ant_glob('test/*.cpp'),
            includes='test',
            target='thrift_stress_test',
            use=['thrift'])

    # # Would like to build thrift's own tests - however our Boost does
    # # not ship with Boost test which is a requirement.  We should fix this
    # # and build the tests at some point.
    # if bld.is_toplevel():
    #     # Only build tests when executed from the top-level wscript,
    #     # i.e.  not when included as a dependency

    #     test_sources = thrift_path.ant_glob(
    #         ['lib/cpp/test/UnitTestMain.cpp'])

    #     bld.program(
    #         features='cxx test',
    #         source=test_sources,
    #         target='thrift_tests',
    #         use=['boost_includes', 'thrift'])

    if bld.options.thrift_compiler:

        if not bld.env.BISON:

            bld.fatal("""Bison not found, is available in the following packages:
                Debian/Ubuntu: apt install bison""")

        if not bld.env.FLEX:

            bld.fatal("""Flex not found, is available in the following packages:
                Debian/Ubuntu: apt install flex""")

        compiler_path = thrift_path.find_dir('compiler/cpp/src')

        bld(features='cxx cxxprogram',
            name='compiler',
            source=compiler_path.ant_glob(['**/*.cc', '**/*.cpp', '**/*.yy', '**/*.ll'],
                                          excl=['**/logging.cc']),
            includes=[compiler_path.abspath(), 'compiler'],
            target='thrift')
