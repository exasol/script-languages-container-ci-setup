from pathlib import Path
from typing import Tuple

from script_languages_container_ci_setup.lib.render_template import render_template


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


def run_generate_buildspec(
        flavor_root_paths: Tuple[str, ...],
        output_file: str,):
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
                                                 flavor_formatted=flavor.flavor_formatted))

    result_yaml = render_template("buildspec_hull.yaml", batch_entries="\n".join(buildspec_body))
    print(f"Result:\n {result_yaml}")
