from typing import Iterable
from tests.production_tests import subscribed_production_tests


class TestResult:
    def __init__(self, msg: str, error: bool = False):
        self.msg = msg
        self.was_error = error


def run_standard_production_tests() -> list[TestResult]:
    """This runs all the tests that cleanly can be run on the production system."""
    results: list[TestResult] = list()

    for test in subscribed_production_tests:
        try:
            out = test()
        except Exception as e:
            results.append(TestResult(str(e), error=True))
        else:
            if out is not None:
                if isinstance(out, str):
                    results.append(TestResult(f"This was returned: {out}", error=False))
    return results
