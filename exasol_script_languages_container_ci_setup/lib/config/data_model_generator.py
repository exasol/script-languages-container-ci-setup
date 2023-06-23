import json
import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from datamodel_code_generator import generate, InputFileType

from exasol_script_languages_container_ci_setup.lib.render_template import render_template

logger = logging.getLogger(__name__)

CONFIG_DATA_MODEL_FILE_NAME = "config_data_model.py"


def config_data_model_default_output_file() -> Path:
    return Path(__file__).parent / CONFIG_DATA_MODEL_FILE_NAME


def generate_config_data_model(output_file: Path) -> Path:
    schema_dict = json.loads(render_template("config_schema.json"))
    schema_json = json.dumps(schema_dict)
    with TemporaryDirectory() as directory:
        temp_output_file = Path(directory) / CONFIG_DATA_MODEL_FILE_NAME
        generate(schema_json, input_file_type=InputFileType.JsonSchema, output=temp_output_file,
                 class_name="Config", apply_default_values_for_required_fields=True)
        with temp_output_file.open("rt") as temp_output_file_handle:
            with output_file.open("wt") as output_file_handle:
                lines = (line for line in temp_output_file_handle)
                lines = filter(lambda line: "#   timestamp: " not in line, lines)
                for line in lines:
                    output_file_handle.write(line)
    return output_file


def regenerate_config_data_model(output_file: Path):
    with TemporaryDirectory() as directory:
        temp_output_file = Path(directory) / CONFIG_DATA_MODEL_FILE_NAME
        generate_config_data_model(temp_output_file)
        with temp_output_file.open("rt") as file:
            new_model = file.read()
        if output_file.is_file():
            with output_file.open("rt") as file:
                old_model = file.read()
            if new_model != old_model:
                logger.warning(f"Regenerating config pydantic model to {output_file}")
                with output_file.open("wt") as file:
                    file.write(new_model)
        else:
            logger.info(f"Generating config pydantic model to new file {output_file}")
            with output_file.open("wt") as file:
                file.write(new_model)
