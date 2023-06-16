import os
from typing import Optional

import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.logging import logging_options, set_log_level
from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.cli.options.aws_options import aws_options
from exasol_script_languages_container_ci_setup.lib.run_start_build import run_start_release_build


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option('--project', type=str, required=True,
              help="""The project name. Must be same name as used for the AWS CodeBuild release stack creation.""")
@click.option('--upload-url', type=str, required=False,
              help="""The URL of the Github release where artifacts will be stored.""")
@click.option('--branch', type=str, required=True,
              help="""The branch of the repository which will be used.""")
def start_release_build(
        aws_profile: Optional[str],
        log_level: str,
        project: str,
        upload_url: str,
        branch: str):
    """
    This command  triggers the AWS release Codebuild to upload the
    release artifacts onto the given Github release, indicated by parameter 'upload_url'.
    """
    set_log_level(log_level)
    run_start_release_build(AwsAccess(aws_profile), project, upload_url, branch, os.getenv("GITHUB_TOKEN"))
