from typing import Optional

import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.aws_options import (
    aws_options,
)
from exasol_script_languages_container_ci_setup.cli.options.logging import (
    logging_options,
    set_log_level,
)
from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.release_build import (
    run_validate_release_build,
)


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option(
    "--project",
    type=str,
    required=True,
    help="""The project for which the stack will be created.""",
)
@click.option(
    "--project-url",
    type=str,
    required=True,
    help="""The URL of the project on Github.""",
)
def validate_release_build(
    aws_profile: Optional[str], log_level: str, project: str, project_url: str
):
    set_log_level(log_level)
    run_validate_release_build(AwsAccess(aws_profile), project, project_url)
