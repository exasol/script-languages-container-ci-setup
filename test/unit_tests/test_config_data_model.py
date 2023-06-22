from inspect import cleandoc

import pytest

from exasol_script_languages_container_ci_setup.lib.config.config_data_model import Config, Build, Ignore, Release


@pytest.fixture
def expected_config() -> Config:
    config = Config(
        build=Build(
            ignore=Ignore(
                paths=[
                    "a/b/c",
                    "e/f/g"
                ]
            ),
            base_branch=""
        ),
        release=Release(
            timeout_in_minutes=1
        )
    )
    return config


def test_serialization(expected_config, expected_config_json):
    actual_json = expected_config.json(indent=4)
    print(actual_json)
    assert actual_json == expected_config_json


def test_json_deserialization(expected_config, expected_config_json):
    actual_config = Config.parse_raw(expected_config_json)
    assert actual_config == expected_config
