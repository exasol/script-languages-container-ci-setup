from pathlib import Path
from typing import Tuple

import click

from script_languages_container_ci_setup.cli.cli import cli
from script_languages_container_ci_setup.lib.run_generate_buildspec import run_generate_buildspec


@cli.command()
@click.option('--flavor-root-path', required=True, multiple=True,
              type=click.Path(file_okay=False, dir_okay=True, exists=True),
              help="Path where script language container flavors are located.")
@click.option('--output-file', type=click.Path(file_okay=True, dir_okay=False, exists=False, writable=True),
              default="./buildspec.yaml",
              help="Path where script language container flavor are located.")
def generate_buildspec(
        flavor_root_path: Tuple[str, ...],
        output_file: str,
        ):
    """
    This command generates the buildspec file for AWS CodeBuild based on the flavors located in path "flavor_root_path".
    """
    run_generate_buildspec(flavor_root_path, output_file)

