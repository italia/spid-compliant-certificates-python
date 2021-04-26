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


def key_usage(extensions: x509.Extensions) -> List[Tuple[bool, str, Any]]:
    checks = []

    # keyUsage: critical;nonRepudiation
    ext_cls = x509.KeyUsage
    ext_name = ext_cls.oid._name

    try:
        ext = extensions.get_extension_for_class(ext_cls)

        msg = f'{ext_name} must be critical'
        res = SUCCESS if ext.critical else FAILURE
        checks.append((res, msg, ext.critical))

        for usage in ['content_commitment', 'digital_signature']:
            msg = f'{usage} bit must be set'
            val = getattr(ext.value, usage)
            res = SUCCESS if val else FAILURE
            checks.append((res, msg, val))

        for usage in ['crl_sign', 'data_encipherment', 'key_agreement',
                      'key_cert_sign', 'key_encipherment']:
            msg = f'{usage} bit must be unset'
            val = getattr(ext.value, usage)
            res = SUCCESS if not val else FAILURE
            checks.append((res, msg, val))
    except x509.ExtensionNotFound as e:
        msg = f'{ext_name} must be present'
        res = FAILURE
        checks.append((res, msg, str(e)))

    return checks
