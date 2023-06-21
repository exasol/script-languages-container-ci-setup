import sys
from pathlib import Path

import pytest

from exasol_script_languages_container_ci_setup.lib.config.data_model_generator import CONFIG_DATA_MODEL_FILE_NAME, \
    generate_config_data_model


@pytest.fixture
def config_data_model_file(tmp_path) -> Path:
    output_file = tmp_path / CONFIG_DATA_MODEL_FILE_NAME
    generate_config_data_model(output_file)
    yield output_file


def test_config_data_model_generation(config_data_model_file):
    import importlib.util
    module_name = "test_create_model_can_be_imported"
    spec = importlib.util.spec_from_file_location(module_name, config_data_model_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    config = module.Config(
        build=module.Build(
            ignore=module.Ignore(
                paths=[
                    "a/b/c",
                    "e/f/g"
                ]
            ),
            base_branch=""
        ),
        release=module.Release(
            timeout_in_minutes=1
        )
    )
    assert True
