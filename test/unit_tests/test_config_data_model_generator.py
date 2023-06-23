import sys

from exasol_script_languages_container_ci_setup.lib.config.data_model_generator import CONFIG_DATA_MODEL_FILE_NAME, \
    generate_config_data_model


def test_loading_generated_module(tmp_path):
    config_data_model_file = tmp_path / CONFIG_DATA_MODEL_FILE_NAME
    generate_config_data_model(config_data_model_file)
    module = load_module(config_data_model_file)
    assert True


def test_using_generated_module(tmp_path, expected_json_config):
    config_data_model_file = tmp_path / CONFIG_DATA_MODEL_FILE_NAME
    generate_config_data_model(config_data_model_file)
    module = load_module(config_data_model_file)
    config = create_config(module)
    actual_json = config.json(indent=4)
    assert actual_json == expected_json_config


def create_config(module):
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
    return config


def load_module(config_data_model_file):
    import importlib.util
    module_name = "test_create_model_can_be_imported"
    spec = importlib.util.spec_from_file_location(module_name, config_data_model_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
