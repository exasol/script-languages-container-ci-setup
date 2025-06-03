import logging
from pathlib import Path
from typing import (
    Optional,
    Tuple,
)

from exasol_script_languages_container_ci_setup.lib.generate_buildspec_common import (
    get_config_file_parameter,
    validate_config_file,
    write_batch_build_spec,
)
from exasol_script_languages_container_ci_setup.lib.render_template import (
    render_template,
)


def run_generate_buildspec(
    flavor_root_paths: tuple[str, ...], output_pathname: str, config_file: Optional[str]
):
    validate_config_file(config_file)

    logging.info(f"Run run_generate_buildspec for paths: {flavor_root_paths}")

    write_batch_build_spec(flavor_root_paths, output_pathname)

    result_build_yaml = render_template(
        "build_buildspec.yaml",
        config_file_parameter=get_config_file_parameter(config_file),
    )

    with open(Path(output_pathname) / "build_buildspec.yaml", "w") as output_file:
        output_file.write(result_build_yaml)
