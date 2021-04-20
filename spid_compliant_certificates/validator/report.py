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
from typing import Callable, List, Tuple

SUCCESS = True
FAILURE = not SUCCESS


class Report(object):
    def __init__(self):
        self.result = 'success'
        self.tests = []

    def add_test_result(self, checks: List[Tuple[bool, str]], description: str) -> None:  # noqa
        test = {}
        test['test'] = description
        test['result'] = 'success'
        test['checks'] = []

        for res, msg in checks:
            if res is FAILURE:
                test['result'] = 'failure'
                self.result = 'failure'
                break

        for res, msg in checks:
            check = {}
            check['check'] = msg
            check['value'] = None
            if res is FAILURE:
                check['result'] = 'failure'
            else:
                check['result'] = 'success'
            test['checks'].append(check)

        self.tests.append(test)


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
        json_report = {}
        json_report['result'] = report.result
        json_report['tests'] = report.tests
        return json.dumps(json_report)

    def _txt_serializer(self, report: Report) -> str:
        lines = []
        lines.append(f'Validation result: {report.result}')

        for test in report.tests:
            lines.append(f'\t{test["test"]}: {test["result"]}')
            for check in test['checks']:
                lines.append(f'\t\t{check["check"]}: {check["result"]} ({check["value"]})')  # noqa

        return '\n'.join(lines)

    def _xml_serializer(self, report: Report) -> str:
        return '<validation><result>failure</result></validation>'
