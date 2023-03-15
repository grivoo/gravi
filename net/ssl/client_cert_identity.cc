#include "net/ssl/client_cert_identity.h"

#include <utility>

#include "base/functional/bind.h"
#include "net/cert/x509_util.h"
#include "net/ssl/ssl_private_key.h"

namespace net {
    namespace {
        void IdentityOwningPrivateKeyCallback(
            std::unique_ptr<ClientCertIdentity> identity,
            base::OnceCallback<void(scoped_refptr<SSLPrivateKey>)> private_key_callback,
            scoped_refptr<SSLPrivateKey> private_key
        ) {
            std::move(private_key_callback).Run(std::move(private_key));
        }
    } // namespace

    ClientCertIdentity::ClientCertIdentity(scoped_refptr<net::X509Certificate> cert)
        : cert_(std::move(cert)) {}
    
    ClientCertIdentity::~ClientCertIdentity() = default;

    // estático
    void ClientCertIdentity::SelfOwningAcquirePrivateKey(
        std::unique_ptr<ClientCertIdentity> self,
        base::OnceCallback<void(scoped_refptr<SSLPrivateKey>)> private_key_callback
    ) {
        ClientCertIdentity* self_ptr = self.get();

        auto wrapped_private_key_callback = base::BindOnce(&IdentityOwningPrivateKeyCallback, std::move(self), std::move(private_key_callback));

        self_ptr->AcquirePrivateKey(std::move(wrapped_private_key_callback));
    }

    void ClientCertIdentity::SetIntermediates(
        std::vector<bssl::UniquePtr<CRYPTO_BUFFER>> intermediates
    ) {
        X509Certificate::UnsafeCreateOptions options;
        options.printable_string_is_utf8 = true;

        cert_ = X509Certificate::CreateFromBufferUnsafeOptions(
            bssl::UpRef(cert_->cert_buffer()), std::move(intermediates), options
        );

        DCHECK(cert_);
    }

    ClientCertIdentitySorter::ClientCertIdentitySorter()
        : now_(base::Time::Now()) {}

    bool ClientCertIdentitySorter::operator()(
        const std::unique_ptr<ClientCertIdentity>& a_identity,
        const std::unique_ptr<ClientCertIdentity>& b_identity
    ) const {
        X509Certificate* a = a_identity->certificate();
        X509Certificate* b = b_identity->certificate();

        DCHECK(a);
        DCHECK(b);

        bool a_is_valid = now_ >= a->valid_start() && now_ <= a->valid_expiry();
        bool b_is_valid = now_ >= b->valid_start() && now_ <= b->valid_expiry();

        if (a_is_valid != b_is_valid)
            return a_is_valid && !b_is_valid;

        if (a->valid_expiry() != b->valid_expiry())
            return a->valid_expiry() > b->valid_expiry();

        if (a->valid_start() != b->valid_start())
            return a->valid_start() > b->valid_start();

        const auto& a_intermediates = a->intermediate_buffers();
        const auto& b_intermediates = b->intermediate_buffers();

        return a_intermediates.size() < b_intermediates.size();
    }
} // namespace net