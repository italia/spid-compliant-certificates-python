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

import re
from typing import List, Tuple

from cryptography import x509
from iso3166 import Country, countries

from spid_compliant_certificates.validator.checks.custom_oid import (
    OID_INITIALS,
    OID_NAME,
    OID_ORGANIZATION_IDENTIFIER,
    OID_URI,
)

SUCCESS = True
FAILURE = not SUCCESS

MANDATORY_ATTRS = [
    OID_ORGANIZATION_IDENTIFIER,
    OID_URI,
    x509.OID_COMMON_NAME,
    x509.OID_COUNTRY_NAME,
    x509.OID_LOCALITY_NAME,
    x509.OID_LOCALITY_NAME,
    x509.OID_ORGANIZATION_NAME,
]

NOT_ALLOWED_ATTRS = [
    OID_INITIALS,
    OID_NAME,
    x509.OID_EMAIL_ADDRESS,
    x509.OID_GIVEN_NAME,
    x509.OID_PSEUDONYM,
    x509.OID_SURNAME,
]


def subject_dn(subj: x509.Name, sector: str) -> List[Tuple[bool, str]]:
    checks = []
    subj_attrs = [attr.oid for attr in subj]

    # check if not allowed attrs are present
    for attr in NOT_ALLOWED_ATTRS:
        msg = 'Name attribute [{attr._name}, {attr.dotted_string}] is not allowed in subjectDN'  # noqa
        res = FAILURE if attr in subj_attrs else SUCCESS
        checks.append((res, msg))

    # check if all the mandatory attre are present
    for attr in MANDATORY_ATTRS:
        msg = f'Name attribute [{attr._name}, {attr.dotted_string}] must be present in subjectDN'  # noqa
        res = FAILURE if attr not in subj_attrs else SUCCESS
        checks.append((res, msg))

    # check the name attribute value
    for attr in subj:
        msg = f'Value for name attribute [{attr.oid._name}, {attr.oid.dotted_string}] can not be empty'  # noqa
        res = FAILURE if not attr.value else SUCCESS
        checks.append((res, msg))

        value = attr.value

        if attr.oid == OID_ORGANIZATION_IDENTIFIER:
            if sector == 'public':
                pattern = r'^PA:IT-\S{1,11}$'
            elif sector == 'private':
                pattern = r'^(CF:IT-[a-zA-Z0-9]{16}|VATIT-\d{11})$'
            else:
                msg = f'Invalid sector ({sector})'
                res = FAILURE
                checks.append((res, msg))

            msg = f'Value for name attribute [{attr.oid._name}, {attr.oid.dotted_string}] must match [{pattern}] (now: {value})'  # noqa
            res = FAILURE if not re.match(pattern, value) else SUCCESS
            checks.append((res, msg))

        if attr.oid == x509.OID_COUNTRY_NAME:
            msg = f'Value for name attribute [{attr.oid._name}, {attr.oid.dotted_string}] is not a valid country code ({value})'  # noqa
            try:
                res = FAILURE if not isinstance(countries.get(value), Country) else SUCCESS  # noqa
                checks.append((res, msg))
            except KeyError:
                res = FAILURE
                checks.append((res, msg))

    return checks
