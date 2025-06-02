import logging
from dataclasses import dataclass
from pathlib import Path
from typing import (
    List,
    Optional,
    Tuple,
)

from exasol_script_languages_container_ci.lib.config.config_data_model import Config

from exasol_script_languages_container_ci_setup.lib.render_template import (
    render_template,
)


@dataclass(eq=True, frozen=True, order=True)
class Flavor:
    """
    Holds the name and the formatted name used for generating the buildspec.
    """

    flavor_original: str

    @property
    def flavor_formatted(self) -> str:
        return self.flavor_original.replace(".", "").replace("-", "_")


def validate_config_file(config_file: Optional[str]):
    """
    Validates config file, path given by parameter config_file.
    :raises:
        `pydantic.ValidationError` if the config file has invalid JSON format.
        `ValueError` if the ignored path given in the config file does not exist.
    """
    if config_file is None:
        return
    config = Config.parse_file(config_file)
    ignored_paths = config.build.ignore.paths
    for ignored_path in ignored_paths:
        folder_path = Path(ignored_path)
        if not folder_path.exists():
            raise ValueError(f"Ignored folder '{ignored_path}' does not exist.")


def get_config_file_parameter(config_file: Optional[str]):
    if config_file is None:
        return ""
    return f"--config-file {config_file}"


def _find_flavors(flavor_root_paths: tuple[str, ...]) -> list[Flavor]:
    """
    Find flavors under the given path(s) and return them in ordered list.
    """
    flavors = set()
    for flavor_root_path in [Path(f).resolve() for f in flavor_root_paths]:
        assert flavor_root_path.is_dir()
        assert flavor_root_path.exists()
        assert flavor_root_path.name == "flavors"
        dirs = (d for d in flavor_root_path.iterdir() if d.is_dir())
        flavors.update(map(lambda directory: Flavor(directory.name), dirs))
    logging.info(f"Found flavors: {flavors}")
    return_value = list(flavors)
    return_value.sort()
    return return_value


def write_batch_build_spec(
    flavor_root_paths: tuple[str, ...], output_pathname: str
) -> None:
    buildspec_body = []
    flavors = _find_flavors(flavor_root_paths)
    for flavor in flavors:
        buildspec_body.append(
            render_template(
                "buildspec_batch_entry.yaml",
                flavor_original=flavor.flavor_original,
                flavor_formatted=flavor.flavor_formatted,
                out_path=output_pathname,
            )
        )

    result_yaml = render_template(
        "buildspec_hull.yaml", batch_entries="\n".join(buildspec_body)
    )

    with open(Path(output_pathname) / "buildspec.yaml", "w") as output_file:
        output_file.write(result_yaml)
