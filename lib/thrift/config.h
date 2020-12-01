#pragma once
#ifdef _WIN32
#include <thrift/windows/config.h>
#else
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <netdb.h>
#include <poll.h>
#include <netinet/tcp.h>

#define HAVE_SYS_STAT_H 1

#define XSTR(x) STR(x)
#define STR(x) #x
//#define MSG(x) _Pragma (STR(error (x)))


#define __STRINGIFY(TEXT) #TEXT
#define __WARNING(TEXT) __STRINGIFY(GCC warning TEXT)
#define WARNING(VALUE) __WARNING(__STRINGIFY(VALUE))


#if defined((_POSIX_C_SOURCE) || defined(_XOPEN_SOURCE)) && defined(_GNU_SOURCE) 
//_Pragma (WARNING(_POSIX_C_SOURCE _XOPEN_SOURCE _GNU_SOURCE))
//#warning("macros: " XSTR(#_POSIX_C_SOURCE) " " XSTR(#_XOPEN_SOURCE) " " XSTR(#_POSIX_C_SOURCE))
#if !((_POSIX_C_SOURCE >= 200112L || _XOPEN_SOURCE >= 600) && !_GNU_SOURCE)
#define STRERROR_R_CHAR_P 1
#endif
#endif




#define HAVE_STRERROR_R 1
#endif



#define PACKAGE_VERSION "0.13.0"