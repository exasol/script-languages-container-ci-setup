import os
from typing import Optional

import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.logging import logging_options, set_log_level
from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.cli.options.aws_options import aws_options
from exasol_script_languages_container_ci_setup.lib.run_start_ci_build import run_start_ci_build


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option('--project', type=str, required=True,
              help="""The project name. Must be same name as used for the AWS CodeBuild release stack creation.""")
@click.option('--branch', type=str, required=True,
              help="""The branch of the repository which will be used.""")
@click.option('--commit-sha', type=str, required=True,
              help="""The commit sha of the commit.""")
def start_ci_build(
        aws_profile: Optional[str],
        log_level: str,
        project: str,
        branch: str,
        commit_sha: str):
    """
    This command can be used to trigger the AWS CI Codebuilds locally (not by Github Action).
    """
    set_log_level(log_level)
    run_start_ci_build(AwsAccess(aws_profile), project, branch, os.getenv("GITHUB_TOKEN"))
