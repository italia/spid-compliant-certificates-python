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

import logging
import platform

RED = '\x1b[31m'
GREEN = '\x1b[32m'
YELLOW = '\x1b[33m'
CYAN = '\x1b[36m'


class ColourFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        levelno = record.levelno
        if levelno >= logging.CRITICAL:
            record.color = RED
        elif levelno >= logging.ERROR:
            record.color = RED
        elif levelno >= logging.WARNING:
            record.color = YELLOW
        elif levelno >= logging.INFO:
            record.color = GREEN
        elif levelno >= logging.DEBUG:
            record.color = CYAN
        else:
            record.color = '\x1b[0m'
        return True


def _c(f: str) -> str:
    return '%(color)s' + f + '\x1b[0m'


_sh = logging.StreamHandler()
_sh.setLevel(logging.DEBUG)

if platform.system() == 'Windows':
    fmt = '[%(levelname)1.1s] %(message)s'
    _sh.setFormatter(logging.Formatter(fmt))
else:
    levelname = _c('%(levelname)1.1s')
    fmt = '[' + levelname + '] %(message)s'
    _sh.setFormatter(logging.Formatter(fmt))
    _sh.addFilter(ColourFilter())

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
LOG.addHandler(_sh)
