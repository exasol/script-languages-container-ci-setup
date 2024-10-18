import re

import pytest

from exasol_script_languages_container_ci_setup.lib.ci_build import (
    CI_BUILD_WEBHOOK_FILTER_PATTERN,
)

testdata = [
    ("refs/heads/feature/test_branch", True),
    ("refs/heads/doc/test_branch", True),
    ("refs/heads/documentation/test_branch", True),
    ("refs/heads/rebuild/feature/test_branch", True),
    ("refs/heads/master", True),
    ("refs/heads/main", True),
    ("refs/heads/develop", True),
    ("refs/heads/master/", False),
    ("refs/heads/main/", False),
    ("refs/heads/develop/", False),
    ("refs/heads/abc", False),
]


@pytest.mark.parametrize("branch,expected", testdata)
def test_webhook_filter_pattern(branch, expected):
    matches = re.match(CI_BUILD_WEBHOOK_FILTER_PATTERN, branch)
    res = False if matches is None else True
    assert res == expected
