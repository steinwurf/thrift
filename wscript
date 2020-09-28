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

    sources = thrift_path.ant_glob(['lib/cpp/src/thrift/TApplicationException.cpp'])

    # include_paths = [thrift_path.find_dir('lib/cpp/src')]


    bld.stlib(
        features='cxx',
        source=sources,
        includes=library_path.abspath(),
        target='thrift',
        use=use_flags,
        #export_includes=[include_paths]
    )

    # if bld.is_toplevel():
    #     # Only build tests when executed from the top-level wscript,
    #     # i.e. not when included as a dependency

    #     # Export thirdparty includes for unit tests
    #     bld(name='thirdparty', export_includes='./thirdparty')

    #     bld.program(
    #         features='cxx test',
    #         source=thrift_path.ant_glob('src/test/c/*.cpp', excl=['**/EmbeddedContentTests.cpp']),
    #         target='thrift_tests',
    #         includes=include_paths,
    #         use=['thirdparty', 'thrift'])
