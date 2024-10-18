import os
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
    run_start_release_build,
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
    "--upload-url",
    type=str,
    required=False,
    help="""The URL of the Github release where artifacts will be stored.""",
)
@click.option(
    "--branch",
    type=str,
    required=True,
    help="""The branch of the repository which will be used.""",
)
@click.option(
    "--timeout-in-seconds",
    type=int,
    required=False,
    help="""Time to wait for the release, anymore.""",
)
@click.option(
    "--config-file",
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    required=False,
    help="Configuration file for build (project specific).",
)
def start_release_build(
    aws_profile: Optional[str],
    log_level: str,
    project: str,
    upload_url: str,
    branch: str,
    timeout_in_seconds: Optional[int],
    config_file: Optional[str],
):
    """
    This command  triggers the AWS release Codebuild to upload the
    release artifacts onto the given Github release, indicated by parameter 'upload_url'.
    """
    set_log_level(log_level)
    run_start_release_build(
        aws_access=AwsAccess(aws_profile),
        project=project,
        upload_url=upload_url,
        branch=branch,
        gh_token=os.getenv("GITHUB_TOKEN"),
        timeout_in_seconds=timeout_in_seconds,
        config_file_path=config_file,
    )
