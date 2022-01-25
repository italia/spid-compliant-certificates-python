import datetime

from cryptography import x509
from typing import Any, List, Tuple


def not_expired(cert: x509.Certificate) -> List[Tuple[bool, str, Any]]:
    checks = []

    msg = f"The Certificate expires in {cert.not_valid_after}"

    res = cert.not_valid_after > datetime.datetime.now()
    checks.append((res, msg, cert.not_valid_after))

    return checks
