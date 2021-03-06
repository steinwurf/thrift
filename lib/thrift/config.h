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

#if (defined(_POSIX_C_SOURCE) || defined(_XOPEN_SOURCE)) && defined(_GNU_SOURCE) 
#if !((_POSIX_C_SOURCE >= 200112L || _XOPEN_SOURCE >= 600) && !_GNU_SOURCE)
#define STRERROR_R_CHAR_P 1
#endif
#endif


#define HAVE_STRERROR_R 1
#endif



#define PACKAGE_VERSION "0.13.0"