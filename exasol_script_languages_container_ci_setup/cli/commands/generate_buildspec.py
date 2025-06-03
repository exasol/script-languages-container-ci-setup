from pathlib import Path
from typing import (
    Optional,
    Tuple,
)

import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.logging import (
    logging_options,
    set_log_level,
)
from exasol_script_languages_container_ci_setup.lib.run_generate_buildspec import (
    run_generate_buildspec,
)


@cli.command()
@add_options(logging_options)
@click.option(
    "--flavor-root-path",
    required=True,
    multiple=True,
    type=click.Path(file_okay=False, dir_okay=True, exists=True),
    help="Path where script language container flavors are located.",
)
@click.option(
    "--output-path",
    type=click.Path(file_okay=False, dir_okay=True, exists=True, writable=True),
    default="./aws-code-build/ci",
    show_default=True,
    help="Path where buildspec files will be deployed.",
)
@click.option(
    "--config-file",
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    help="Configuration file for build (project specific).",
)
def generate_buildspecs(
    flavor_root_path: tuple[str, ...],
    log_level: str,
    output_path: str,
    config_file: Optional[str],
):
    """
    This command generates the buildspec file(s) for AWS CodeBuild based on the flavors located in path "flavor_root_path".
    """
    set_log_level(log_level)
    run_generate_buildspec(flavor_root_path, output_path, config_file)
