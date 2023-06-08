import logging

from exasol_script_languages_container_ci_setup.lib.config.pydantic_model_generator import \
    get_config_data_model_pydantic_model_default_output_file, regenerate_config_data_model

DISABLE_PYDANTIC_MODEL_GENERATION = "--disable-pydantic-model-generation"

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        DISABLE_PYDANTIC_MODEL_GENERATION, action="store_true", default=False,
        help="Disables the generation of the pydantic models from the json schemas"
    )


def pytest_configure(config):
    """
    Some of our tests are based on the pydantic model. We need to make sure, the tests work with the newest
    version. However, we also need regenerate the file as early as possible, before other modules import it.
    For that reason. we are triggering the regeneration in conftest.
    """

    if not config.getoption(DISABLE_PYDANTIC_MODEL_GENERATION):
        output_file = get_config_data_model_pydantic_model_default_output_file()
        regenerate_config_data_model(output_file)
    else:
        logger.warning("Generation of pydantic models from json schema disabled")
