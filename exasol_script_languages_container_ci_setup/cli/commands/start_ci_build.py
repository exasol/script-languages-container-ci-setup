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
from exasol_script_languages_container_ci_setup.lib.run_start_build import (
    run_start_ci_build,
)


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option(
    "--project",
    type=str,
    required=True,
    help="""The project name. Must be same name as used for the AWS CodeBuild release stack creation.""",
)
@click.option(
    "--branch",
    type=str,
    required=True,
    help="""The branch of the repository which will be used(e.g. refs/heads/master).""",
)
@click.option(
    "--timeout-in-seconds",
    type=int,
    required=False,
    default=180,
    help="""Time we wait for the build to finish.""",
)
def start_ci_build(
    aws_profile: Optional[str],
    log_level: str,
    project: str,
    branch: str,
    timeout_in_seconds: int,
):
    """
    This command can be used to trigger the AWS CI CodeBuild locally (not by Github Webhook).
    """
    set_log_level(log_level)
    run_start_ci_build(
        aws_access=AwsAccess(aws_profile),
        project=project,
        branch=branch,
        timeout_in_seconds=timeout_in_seconds,
    )
