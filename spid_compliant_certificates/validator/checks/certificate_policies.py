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

from typing import Any, List, Tuple

from cryptography import x509

SUCCESS = True
FAILURE = not SUCCESS


def certificate_policies(extensions: x509.Extensions, sector: str) -> List[Tuple[bool, str, Any]]:  # noqa
    checks = []

    # certificatePolicies: agIDcert(agIDcert)
    ext_cls = x509.CertificatePolicies
    ext_name = ext_cls.oid._name

    # expected policies
    exp_policies = [
        '1.3.76.16.6'  # agIDCert
    ]

    if sector == 'private':
        exp_policies.append('1.3.76.16.4.3.1')  # spid-private-sp

    if sector == 'public':
        exp_policies.append('1.3.76.16.4.2.1')  # spid-public-sp

    try:
        ext = extensions.get_extension_for_class(ext_cls)

        # check if critical
        msg = f'{ext_name} must be not critical'
        res = FAILURE if ext.critical else SUCCESS
        checks.append((res, msg, ext.critical))

        # check if expected policies are present
        policies = ext.value
        for ep in exp_policies:
            is_present = any(
                p.policy_identifier.dotted_string == ep for p in policies
            )
            msg = f'policy {ep} must be present'
            res = SUCCESS if is_present else FAILURE
            checks.append((res, msg, is_present))

        # check the content of the policies
        for p in policies:
            oid = p.policy_identifier.dotted_string
            if oid == '1.3.76.16.6':
                for q in p.policy_qualifiers:
                    if isinstance(q, x509.extensions.UserNotice):
                        exp_etext = 'agIDcert'
                        etext = q.explicit_text

                        msg = f'policy {oid} must have '
                        msg += f'UserNotice.ExplicitText={exp_etext}'  # noqa

                        res = FAILURE if etext != exp_etext else SUCCESS
                        checks.append((res, msg, etext))

            if sector == 'public' and oid == '1.3.76.16.4.2.1':
                for q in p.policy_qualifiers:
                    if isinstance(q, x509.extensions.UserNotice):
                        exp_etext = 'cert_SP_Pub'
                        etext = q.explicit_text

                        msg = f'policy {oid} must have '
                        msg += f'UserNotice.ExplicitText={exp_etext}'  # noqa

                        res = FAILURE if etext != exp_etext else SUCCESS
                        checks.append((res, msg, etext))
            if sector == 'private' and oid == '1.3.76.16.4.3.1':
                _qualifiers = p.policy_qualifiers or []
                msg = f'policy {oid} must have '
                for q in _qualifiers:
                    if isinstance(q, x509.extensions.UserNotice):
                        exp_etext = 'cert_SP_Priv'
                        etext = q.explicit_text

                        msg += f'UserNotice.ExplicitText={exp_etext}'  # noqa

                        res = FAILURE if etext != exp_etext else SUCCESS
                        checks.append((res, msg, etext))

                if not _qualifiers:
                    checks.append(
                        (
                            FAILURE,
                            f'policy {oid} must have a valid policy',
                            ""
                        )
                    )

    except x509.ExtensionNotFound as e:
        msg = f'{ext_name} must be present'
        checks.append((FAILURE, msg, str(e)))

    return checks
