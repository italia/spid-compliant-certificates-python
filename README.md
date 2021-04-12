# spid-compliant-certificates

Python native solution to generate and validate X.509 certificates according
to [Avviso SPID n.29 v3](https://www.agid.gov.it/sites/default/files/repository_files/spid-avviso-n29v3-specifiche_sp_pubblici_e_privati_0.pdf).

## Installation

Nothing more than

    $ pip install spid-compliant-certificates

Alternatively, you can install it from sources

    $ pip install -r requirements.txt
    $ python setup.py install

## Command line usage

Generate private key, self-signed X.509 ertificate and CSR for public sector
SPID service provider

    $ spid-compliant-certificates generator \
        --key-size 3072 \
        --common-name "A.C.M.E" \
        --days 365 \
        --entity-id https://spid.acme.it \
        --locality-name Roma \
        --org-id "PA:IT-c_h501" \
        --org-name "A Company Making Everything" \
        --sector public
    [DEBUG] Starting new HTTPS connection (1): indicepa.gov.it:443
    [DEBUG] https://indicepa.gov.it:443 "GET /ricerca/n-dettaglioamministrazione.php?cod_amm=c_h501 HTTP/1.1" 200 23778
    [INFO ] Private key saved to key.pem
    [INFO ]   Inspect with OpenSSL: openssl rsa -in key.pem -noout -text
    [INFO ] CSR saved to csr.pem
    [INFO ]   Inspect with OpenSSL: openssl req -in csr.pem -noout -text
    [INFO ]   Inspect with OpenSSL: openssl asn1parse -i -inform PEM -in csr.pem
    [INFO ] Self-signed certificate saved to crt.pem
    [INFO ]   Inspect with OpenSSL: openssl x509 -noout -text -in crt.pem
    [INFO ]   Inspect with OpenSSL: openssl asn1parse -i -inform PEM -in crt.pem

Validate the self-signed X.509 certificate

    $ spid-compliant-certificates validator --sector public
    [INFO ] Validating certificate crt.pem against public sector specifications
    [INFO ] Checking the key type and size: success
    [INFO ]     The keypair must be RSA
    [INFO ]     The key size must be greater than or equal to 2048 (now: 3072)
    [INFO ]     The key size must be one of [2048, 3072, 4096] (now: 3072)
    [INFO ] Checking the signature digest algorithm: success
    [INFO ]     The digest algorithm must be one of ['sha256', 'sha512'] (now: sha256)
    [INFO ] Checking the SubjectDN: success
    [INFO ]     Name attribute [initials, 2.5.4.43] is not allowed in subjectDN
    [INFO ]     Name attribute [name, 2.5.4.41] is not allowed in subjectDN
    [INFO ]     Name attribute [emailAddress, 1.2.840.113549.1.9.1] is not allowed in subjectDN
    [INFO ]     Name attribute [givenName, 2.5.4.42] is not allowed in subjectDN
    [INFO ]     Name attribute [pseudonym, 2.5.4.65] is not allowed in subjectDN
    [INFO ]     Name attribute [surname, 2.5.4.4] is not allowed in subjectDN
    [INFO ]     Name attribute [organizationIdentifier, 2.5.4.97] must be present in subjectDN
    [INFO ]     Name attribute [uri, 2.5.4.83] must be present in subjectDN
    [INFO ]     Name attribute [commonName, 2.5.4.3] must be present in subjectDN
    [INFO ]     Name attribute [countryName, 2.5.4.6] must be present in subjectDN
    [INFO ]     Name attribute [localityName, 2.5.4.7] must be present in subjectDN
    [INFO ]     Name attribute [localityName, 2.5.4.7] must be present in subjectDN
    [INFO ]     Name attribute [organizationName, 2.5.4.10] must be present in subjectDN
    [INFO ]     Value for name attribute [organizationName, 2.5.4.10] can not be empty
    [INFO ]     Value for name attribute [commonName, 2.5.4.3] can not be empty
    [INFO ]     Value for name attribute [Unknown OID, 2.5.4.83] can not be empty
    [INFO ]     Value for name attribute [Unknown OID, 2.5.4.97] can not be empty
    [INFO ]     Value for name attribute [Unknown OID, 2.5.4.97] must match [^PA:IT-\S{1,11}$] (now: PA:IT-c_h501)
    [INFO ]     Value for name attribute [countryName, 2.5.4.6] can not be empty
    [INFO ]     Value for name attribute [countryName, 2.5.4.6] is not a valid country code (IT)
    [INFO ]     Value for name attribute [localityName, 2.5.4.7] can not be empty
    [INFO ] Checking basicConstraints x509 extension: success
    [INFO ]     basicConstraints can not be set as critical
    [INFO ]     CA must be FALSE
    [INFO ] Checking keyUsage x509 extension: success
    [INFO ]     keyUsage must be set as critical
    [INFO ]     content_commitment must be set
    [INFO ]     digital_signature must be set
    [INFO ]     crl_sign must be unset
    [INFO ]     data_encipherment must be unset
    [INFO ]     key_agreement must be unset
    [INFO ]     key_cert_sign must be unset
    [INFO ]     key_encipherment must be unset
    [INFO ] Checking certificatePolicies x509 extension: success
    [INFO ]     certificatePolicies can not be set as critical
    [INFO ]     policy 1.3.76.16.6 must be present
    [INFO ]     policy 1.3.76.16.4.2.1 must be present
    [INFO ]     policy 1.3.76.16.6 must have UserNotice.ExplicitText=agIDcert (now: agIDcert)
    [INFO ]     policy 1.3.76.16.4.2.1 must have UserNotice.ExplicitText=cert_SP_Pub (now: cert_SP_Pub)

Generate private key and CSR for private sector SPID service provider

    $ spid-compliant-certificates generator \
        --key-size 3072 \
        --common-name "A.C.M.E" \
        --days 365 \
        --entity-id https://spid.acme.it \
        --locality-name Roma \
        --org-id "VATIT-12345678901" \
        --org-name "A Company Making Everything" \
        --sector private
    [INFO ] Private key saved to key.pem
    [INFO ]   Inspect with OpenSSL: openssl rsa -in key.pem -noout -text
    [INFO ] CSR saved to csr.pem
    [INFO ]   Inspect with OpenSSL: openssl req -in csr.pem -noout -text
    [INFO ]   Inspect with OpenSSL: openssl asn1parse -i -inform PEM -in csr.pem

Are you looking for further info?

    $ spid-compliant-certificates --help
    $ spid-compliant-certificates generator --help
    $ spid-compliant-certificates validator --help

## Docker usage

Build the image locally

    $ docker build --tag local/spid-compliant-certificates .

or pull it from [Docker Hub](https://hub.docker.com/r/italia/spid-compliant-certificates)

    $ docker pull italia/spid-compliant-certificates

In order to access files generated/validated by the container, mount your
local path to `/certs`, which is the default container working directory.

    $ docker run -ti --rm \
        -v "/your/local/path:/certs" \
        italia/spid-compliant-certificates generator \
            --key-size 3072 \
            --common-name "A.C.M.E" \
            --days 365 \
            --entity-id https://spid.acme.it \
            --locality-name Roma \
            --org-id "PA:IT-c_h501" \
            --org-name "A Company Making Everything" \
            --sector public
    [DEBUG] Starting new HTTPS connection (1): indicepa.gov.it:443
    [DEBUG] https://indicepa.gov.it:443 "GET /ricerca/n-dettaglioamministrazione.php?cod_amm=c_h501 HTTP/1.1" 200 23778
    [INFO ] Private key saved to key.pem
    [INFO ]   Inspect with OpenSSL: openssl rsa -in key.pem -noout -text
    [INFO ] CSR saved to csr.pem
    [INFO ]   Inspect with OpenSSL: openssl req -in csr.pem -noout -text
    [INFO ]   Inspect with OpenSSL: openssl asn1parse -i -inform PEM -in csr.pem
    [INFO ] Self-signed certificate saved to crt.pem
    [INFO ]   Inspect with OpenSSL: openssl x509 -noout -text -in crt.pem
    [INFO ]   Inspect with OpenSSL: openssl asn1parse -i -inform PEM -in crt.pem

## Dev usage

The package provides Pyton `unittest` test cases that can be imported in your
Python project

```.py
import unittest

from spid_compliant_certificates.validator.test_cases import TestPrivateSector
from spid_compliant_certificates.validator.test_cases import TestPublicSector

if __name__ == '__main__':
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    test_cases = (TestPrivateSector, TestPublicSector, YourOtherTestCase)
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)
```

Furtermore, they can also be executed from the command line as follows

    $ CERT_FILE=/path/to/your/cert.pem python -m unittest -vv spid_compliant_certificates.validator.test_cases.TestPrivateSector
    test_basic_constraints (spid_compliant_certificates.validator.test_cases.private_sector.TestPrivateSector) ... ok
    test_certificate_policies (spid_compliant_certificates.validator.test_cases.private_sector.TestPrivateSector) ... ok
    test_digest_algorithm (spid_compliant_certificates.validator.test_cases.private_sector.TestPrivateSector) ... ok
    test_key_type_and_size (spid_compliant_certificates.validator.test_cases.private_sector.TestPrivateSector) ... ok
    test_key_usage (spid_compliant_certificates.validator.test_cases.private_sector.TestPrivateSector) ... ok
    test_subject_dn (spid_compliant_certificates.validator.test_cases.private_sector.TestPrivateSector) ... ok

    ----------------------------------------------------------------------
    Ran 6 tests in 0.030s

    OK


    $ CERT_FILE=/path/to/your/cert.pem python -m unittest -vv spid_compliant_certificates.validator.test_cases.TestPublicSector
    test_basic_constraints (spid_compliant_certificates.validator.test_cases.public_sector.TestPublicSector) ... ok
    test_certificate_policies (spid_compliant_certificates.validator.test_cases.public_sector.TestPublicSector) ... ok
    test_digest_algorithm (spid_compliant_certificates.validator.test_cases.public_sector.TestPublicSector) ... ok
    test_key_type_and_size (spid_compliant_certificates.validator.test_cases.public_sector.TestPublicSector) ... ok
    test_key_usage (spid_compliant_certificates.validator.test_cases.public_sector.TestPublicSector) ... ok
    test_subject_dn (spid_compliant_certificates.validator.test_cases.public_sector.TestPublicSector) ... ok

    ----------------------------------------------------------------------
    Ran 6 tests in 0.019s

    OK
