import sys
from pathlib import Path

import pytest

from exasol_script_languages_container_ci_setup.lib.config.config_data_model import Config, Build, Ignore, Release
from exasol_script_languages_container_ci_setup.lib.config.pydantic_model_generator import generate_config_data_model, \
    CONFIG_DATA_MODEL_FILE_NAME


def test():
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
    json = config.json()
    Config.parse_raw(json)
