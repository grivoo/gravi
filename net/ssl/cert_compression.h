#ifndef NET_SSL_CERT_COMPRESSION_H_
#define NET_SSL_CERT_COMPRESSION_H_

#include "third_party/boringssl/src/include/openssl/base.h"

namespace net {
    void ConfigureCertificateCompression(SSL_CTX* ctx);
} // namespace net

#endif // NET_SSL_CERT_COMPRESSION_H_