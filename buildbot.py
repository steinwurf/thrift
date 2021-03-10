#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

project_name = 'thrift'


def run_command(args):
    print("Running: {}".format(args))
    sys.stdout.flush()
    subprocess.check_call(args)


def get_tool_options(properties):
    options = []
    if 'tool_options' in properties:
        # Make sure that the values are correctly comma separated
        for key, value in properties['tool_options'].items():
            if value is None:
                options += ['--{0}'.format(key)]
            else:
                options += ['--{0}={1}'.format(key, value)]

    return options


def configure(properties):
    command = [sys.executable, 'waf']

    if properties.get('build_distclean'):
        command += ['distclean']

    command += ['configure', '--git_protocol=git@']

    if 'waf_resolve_path' in properties:
        command += ['--resolve_path=' + properties['waf_resolve_path']]

    if 'dependency_project' in properties:
        command += ['--{0}_checkout={1}'.format(
            properties['dependency_project'],
            properties['dependency_checkout'])]

    if 'cxx_mkspec' in properties:
        command += ["--cxx_mkspec={}".format(properties['cxx_mkspec'])]

    if 'nodebug' in properties:
        command += ["--cxx_nodebug"]
    command += get_tool_options(properties)

    run_command(command)


def build(properties):
    command = [sys.executable, 'waf', 'build', '-v']
    run_command(command)


def run_tests(properties):
    command = [sys.executable, 'waf', '-v', '--run_tests']
    run_cmd = '%s'

    if properties.get('valgrind_run'):
        run_cmd = 'valgrind --error-exitcode=1 %s --profile=embedded'
    elif 'test_type' in properties:
        run_cmd += ' --profile={0}'.format(properties['test_type'])

    if run_cmd:
        command += ["--run_cmd={}".format(run_cmd)]

    command += get_tool_options(properties)

    run_command(command)

    # Dry run the benchmarks after the unit tests
    command = [sys.executable, 'waf', '-v']
    command += ['--run_benchmarks', '--run_cmd=%s --dry_run']
    run_command(command)


def install(properties):
    command = [sys.executable, 'waf', '-v', 'install']

    if 'install_path' in properties:
        install_path = properties['install_path']
        command += ['--destdir={0}'.format(install_path)]
        # Make sure that the previous install folder is removed
        if os.path.isdir(install_path):
            shutil.rmtree(install_path)

    run_command(command)


def main():

    argv = sys.argv

    if len(argv) != 3:
        print("Usage: {} <command> <properties>".format(argv[0]))
        sys.exit(0)

    cmd = argv[1]
    properties = json.loads(argv[2])

    if cmd == 'configure':
        configure(properties)
    elif cmd == 'build':
        build(properties)
    elif cmd == 'run_tests':
        run_tests(properties)
    elif cmd == 'install':
        install(properties)
    else:
        print("Unknown command: {}".format(cmd))


if __name__ == '__main__':
    main()
