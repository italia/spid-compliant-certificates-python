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

import json
from datetime import datetime
from typing import Any, Callable, Dict, Optional

SUCCESS = True
FAILURE = not SUCCESS


class Check(object):
    def __init__(self, description: str, result: str, value: Any):
        self.description = description
        self.result = result
        self.value = value

    def as_dict(self) -> Dict:
        d = {}
        for k in ['description', 'result', 'value']:
            d[k] = getattr(self, k)
        return d

    def as_txt(self, fmt: Optional[str] = None) -> str:
        if fmt:
            return fmt % self.as_dict()
        else:
            return f'{self.description} [{self.result}][{self.value}]'

    def is_success(self) -> bool:
        return (True if self.result == 'success' else False)


class Test(object):
    def __init__(self, description: str):
        self.description = description
        self.result = 'success'
        self.checks = []

    def add_check(self, check: Check) -> None:
        if not check.is_success():
            self.result = 'failure'
        self.checks.append(check)

    def as_dict(self) -> Dict:
        d = {}
        for k in ['description', 'result']:
            d[k] = getattr(self, k)
        d['checks'] = [c.as_dict() for c in self.checks]
        return d

    def as_txt(self, fmt: Optional[str] = None) -> str:
        lines = []
        lines.append(f'Test: {self.description}')
        lines.append(f'Result: {self.result}')
        for line in [f'  {c.as_txt(fmt)}' for c in self.checks]:
            lines.append(line)
        return '\n'.join(lines)

    def is_success(self) -> bool:
        return (True if self.result == 'success' else False)


class Report(object):
    def __init__(self, target: str):
        self.timestamp = datetime.now().strftime('%c')
        self.result = 'success'
        self.target = target
        self.tests = []

    def add_test(self, test: Test) -> None:
        if not test.is_success():
            self.result = 'failure'
        self.tests.append(test)

    def as_dict(self) -> Dict:
        d = {}
        for k in ['result', 'target', 'timestamp']:
            d[k] = getattr(self, k)
        d['tests'] = [t.as_dict() for t in self.tests]
        return d

    def is_success(self) -> bool:
        return (True if self.result == 'success' else False)


class ReportSerializer(object):
    def serialize(self, report: Report, format: str) -> str:
        serializer = self._get_serializer(format)
        return serializer(report)

    def _get_serializer(self, format: str) -> Callable[[Report], str]:
        if format == 'json':
            return self._json_serializer
        elif format == 'txt':
            return self._txt_serializer
        elif format == 'xml':
            return self._xml_serializer
        else:
            emsg = f'Format {format} is not accepted'
            raise ValueError(emsg)

    def _json_serializer(self, report: Report) -> str:
        return json.dumps(report.as_dict())

    def _txt_serializer(self, report: Report) -> str:
        lines = []
        lines.append(f'Result: {report.result}')
        lines.append(f'Target: {report.target}')
        lines.append(f'Timestamp: {report.timestamp}')
        for _lines in [t.as_txt().split('\n') for t in report.tests]:
            for line in [f'  {_line}' for _line in _lines]:
                lines.append(line)
        return '\n'.join(lines)

    def _xml_serializer(self, report: Report) -> str:
        return f'''<report>
    <target>{report.target}</target>
    <timestamp>{report.timestamp}</timestamp>
    <result>{report.result}</result>
</report>'''
