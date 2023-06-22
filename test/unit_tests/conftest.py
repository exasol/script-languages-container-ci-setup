from inspect import cleandoc

import pytest


@pytest.fixture
def expected_config_json() -> str:
    json = cleandoc("""
    {
        "build": {
            "ignore": {
                "paths": [
                    "a/b/c",
                    "e/f/g"
                ]
            },
            "base_branch": ""
        },
        "release": {
            "timeout_in_minutes": 1
        }
    }""")
    return json