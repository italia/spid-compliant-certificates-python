# Copyright 2021 Paolo Smiraglia <paolo.smiraglia@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List, Tuple

from cryptography import x509

from spid_compliant_certificates.validator import checks
from spid_compliant_certificates.validator.report import Check, Report, Test
from spid_compliant_certificates.validator.utils import pem_to_der


def _do_check(checks: List[Tuple[bool, str]], base_msg: str) -> Test:
    t = Test(base_msg)
    for res, msg, val in checks:
        t.add_check(Check(msg, 'success' if res else 'failure', val))
    return t


def validate(crt_file: str, sector: str) -> Report:
    # load certificate file
    crt = None
    der, msg = pem_to_der(crt_file)
    if der:
        crt = x509.load_der_x509_certificate(der)
    else:
        raise Exception(msg)

    rep = Report(str(crt_file.absolute()))

    # check key type and size
    rep.add_test(_do_check(
        checks.key_type_and_size(crt),
        'Checking the key type and size'
    ))

    # check digest algorithm
    rep.add_test(_do_check(
        checks.digest_algorithm(crt.signature_hash_algorithm.name),
        'Checking the signature digest algorithm'
    ))

    # check SubjectDN
    rep.add_test(_do_check(
        checks.subject_dn(crt.subject, sector),
        'Checking the SubjectDN'
    ))

    # check time 
    rep.add_test(_do_check(
        checks.not_expired(crt),
        'Checking that the certificates is not expired'
    ))

    # check basicConstraints
    _ext_msg = 'Checking basicConstraints x509 extension'
    try:
        rep.add_test(_do_check(
            checks.basic_constraints(crt.extensions),
            _ext_msg
        ))

        # check keyUsage
        rep.add_test(_do_check(
            checks.key_usage(crt.extensions),
            'Checking keyUsage x509 extension'
        ))
        # check certificatePolicies
        rep.add_test(_do_check(
            checks.certificate_policies(crt.extensions, sector),
            'Checking certificatePolicies x509 extension'
        ))

    except ValueError as e:
        test = Test(f"Critical Error on parsing extensions: {e}")
        test.add_check(Check(f"{_ext_msg} critical error", 'failure', False))
        rep.add_test(test)

    return rep
