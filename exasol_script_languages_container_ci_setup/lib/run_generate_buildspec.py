from pathlib import Path
from typing import Tuple

import pkg_resources


from exasol_script_languages_container_ci_setup.lib.render_template import render_template


class Flavor(object):
    """"
    Holds the name and the formatted name used for generating the buildspec.
    """

    def __init__(self, flavor: str):
        self.flavor_original = flavor
        self.flavor_formatted = flavor.replace(".", "").replace("-", "_")

    def __str__(self):
        return f"Flavor(original={self.flavor_original}, formatted={self.flavor_formatted})"

    def __repr__(self):
        return self.__str__()


def get_pip_location_for_pkg(dependent_pkg: str):
    self_pkg_requirements = pkg_resources.working_set.by_key["script-languages-container-ci-setup"].requires()
    searched_pgk_url = [pkg.url for pkg in self_pkg_requirements if pkg.name == dependent_pkg]
    if len(searched_pgk_url) == 0:
        raise RuntimeError(f"Missing dependency to package '{dependent_pkg}'")
    elif len(searched_pgk_url) > 1:
        raise RuntimeError(f"Multiple dependency entries found for package '{dependent_pkg}'")
    return searched_pgk_url[0]


def run_generate_buildspec(
        flavor_root_paths: Tuple[str, ...],
        output_pathname: str):
    flavors = set()
    for flavor_root_path in [Path(f).resolve() for f in flavor_root_paths]:
        assert flavor_root_path.is_dir()
        assert flavor_root_path.exists()
        assert flavor_root_path.name == "flavors"
        for child in flavor_root_path.iterdir():
            if child.is_dir():
                flavors.add(Flavor(child.name))

    buildspec_body = []
    for flavor in flavors:
        buildspec_body.append(render_template("buildspec_batch_entry.yaml",
                                                 flavor_original=flavor.flavor_original,
                                                 flavor_formatted=flavor.flavor_formatted,
                                                 out_path=output_pathname))

    result_yaml = render_template("buildspec_hull.yaml", batch_entries="\n".join(buildspec_body))

    output_pathname = Path(output_pathname)
    with open(output_pathname / "buildspec.yaml", "w") as output_file:
        output_file.write(result_yaml)

    script_languages_ci_location = get_pip_location_for_pkg("script-languages-container-ci")
    result_build_yaml = render_template("build_buildspec.yaml",
                                        script_languages_ci_location=script_languages_ci_location)

    with open(output_pathname / "build_buildspec.yaml", "w") as output_file:
        output_file.write(result_build_yaml)
