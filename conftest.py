import pytest
from _pytest.reports import TestReport


class CustomReport(TestReport):

    @TestReport.head_line.getter
    def head_line(self):
        return f'my headline: {self.nodeid}'


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    return CustomReport.from_item_and_call(item, call)