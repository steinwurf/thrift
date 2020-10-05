Apache Thrift
=============

Apache Thrift build script wrapper for the waf build system.

Maintainer notes
----------------

In order to make Thrift compile (easily) with Waf we made two change in order
to avoid autoconf'n'friends.

1. For the Thrift library we provide a `config.h` file with the needed includes
   on Linux. Thrift already ships with a `config.h` for Windows, but the Linux
   variant was auto generated. We add one to avoid that step.

   You can find our version in `lib/thrift/config.h`.

2. For the Thrift compiler we supply a `version.h` file. Again this file is
   auto generated. However, in recent version of Thrift and actual version.h file
   have been added. So when we upgrade from version 0.13.0 we may no longer need
   to provide this.
