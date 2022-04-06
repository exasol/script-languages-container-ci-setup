from pathlib import Path
from typing import Tuple

import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.lib.run_generate_buildspec import run_generate_buildspec


@cli.command()
@click.option('--flavor-root-path', required=True, multiple=True,
              type=click.Path(file_okay=False, dir_okay=True, exists=True),
              help="Path where script language container flavors are located.")
@click.option('--output-path', type=click.Path(file_okay=False, dir_okay=True, exists=True, writable=True),
              default="./aws-code-build/ci",
              help="Path where buildspec files will be deployed.")
def generate_buildspecs(
        flavor_root_path: Tuple[str, ...],
        output_path: str,
        ):
    """
    This command generates the buildspec file(s) for AWS CodeBuild based on the flavors located in path "flavor_root_path".
    """
    run_generate_buildspec(flavor_root_path, output_path)

