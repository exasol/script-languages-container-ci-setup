import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Optional
import jsonschema

from exasol_script_languages_container_ci_setup.lib.render_template import render_template


@dataclass(eq=True, frozen=True)
class Flavor(object):
    """"
    Holds the name and the formatted name used for generating the buildspec.
    """
    flavor_original: str

    def flavor_formatted(self) -> str:
        return self.flavor_original.replace(".", "").replace("-", "_")


def validate_config_file(config_file: Optional[str]):
    if config_file is not None:
        with open(config_file, "r") as config_file_:
            config = json.load(config_file_)
            config_schema = json.loads(render_template("config_schema.json"))
            jsonschema.validate(instance=config, schema=config_schema)
            ignored_paths = config["build_ignore"]["ignored_paths"]
            for ignored_path in ignored_paths:
                folder_path = Path(ignored_path)
                if not folder_path.exists():
                    raise ValueError(f"Ignored folder '{ignored_path}' does not exist.")


def get_config_file_parameter(config_file: Optional[str]):
    if config_file is None:
        return ""
    return f"--config-file {config_file}"


def run_generate_buildspec(
        flavor_root_paths: Tuple[str, ...],
        output_pathname: str,
        config_file: Optional[str]):
    validate_config_file(config_file)
    flavors = set()
    logging.info(f"Run run_generate_buildspec for paths: {flavor_root_paths}")
    for flavor_root_path in [Path(f).resolve() for f in flavor_root_paths]:
        assert flavor_root_path.is_dir()
        assert flavor_root_path.exists()
        assert flavor_root_path.name == "flavors"
        dirs = (d for d in flavor_root_path.iterdir() if d.is_dir())
        flavors.update(map(lambda directory: Flavor(directory.name), dirs))
    logging.info(f"Found flavors: {flavors}")
    buildspec_body = []
    for flavor in flavors:
        buildspec_body.append(render_template("buildspec_batch_entry.yaml",
                                                 flavor_original=flavor.flavor_original,
                                                 flavor_formatted=flavor.flavor_formatted(),
                                                 out_path=output_pathname))

    result_yaml = render_template("buildspec_hull.yaml", batch_entries="\n".join(buildspec_body))

    output_pathname = Path(output_pathname)
    with open(output_pathname / "buildspec.yaml", "w") as output_file:
        output_file.write(result_yaml)

    result_build_yaml = render_template("build_buildspec.yaml",
                                        config_file_parameter=get_config_file_parameter(config_file))

    with open(output_pathname / "build_buildspec.yaml", "w") as output_file:
        output_file.write(result_build_yaml)
