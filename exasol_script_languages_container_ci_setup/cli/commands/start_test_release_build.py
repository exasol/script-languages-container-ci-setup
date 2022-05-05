from typing import Optional

import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.logging import logging_options, set_log_level
from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.cli.options.aws_options import aws_options
from exasol_script_languages_container_ci_setup.lib.run_start_release_build import run_start_test_release_build


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option('--project', type=str, required=True,
              help="""The project name. Must be same name as used for the AWS CodeBuild release stack creation.""")
@click.option('--release-tag', type=str, required=False,
              help="""The tag of the release for which the artifacts will be stored.""")
def start_release_build(
        aws_profile: Optional[str],
        log_level: str,
        project: str,
        release_tag: str,
):
    set_log_level(log_level)
    run_start_test_release_build(AwsAccess(aws_profile), project, release_tag)
