#include "net/ssl/cert_compression.h"

#include <cstdint>

#include "third_party/boringssl/src/include/openssl/ssl.h"

#if !defined(NET_DISABLE_BROTLI)
#include "third_party/brotli/include/brotli/decode.h"
#endif

namespace net {
    namespace {
        #if !defined(NET_DISABLE_BROTLI)

        int DecompressBrotliCert(SSL* ssl, CRYPTO_BUFFER** out, size_t uncompressed_len, const uint8_t* in, size_t in_len) {
            uint8_t* data;

            bssl::UniquePtr<CRYPTO_BUFFER> decompressed(
                CRYPTO_BUFFER_alloc(&data, uncompressed_len)
            );

            if (!decompressed) {
                return 0;
            }

            size_t output_size = uncompressed_len;

            if (BrotliDecoderDecompress(
                in_len,
                in,
                &output_size,
                data
            ) != BROTLI_DECODER_RESULT_SUCCESS || output_size != uncompressed_len) {
                return 0;
            }

            *out = decompressed.release();

            return 1;
        }

        #endif
    } // namespace

    void ConfigureCertificateCompression(SSL_CTX* ctx) {
        #if !defined(NET_DISABLE_BROTLI)
    }
}