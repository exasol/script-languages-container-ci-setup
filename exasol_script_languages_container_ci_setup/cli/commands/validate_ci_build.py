import logging

import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.logging import logging_options, set_log_level
from exasol_script_languages_container_ci_setup.lib.ci_build import run_deploy_ci_build, run_validate_ci_build
from exasol_script_languages_container_ci_setup.cli.options.aws_options import aws_options


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option('--project', type=str, required=True,
              help="""The project for which the stack will be created.""")
@click.option('--project-url', type=str, required=True,
              help="""The URL of the project on Github.""")
def validate_ci_build(
        aws_profile: str,
        log_level: str,
        project: str,
        project_url: str):
    set_log_level(log_level)
    run_validate_ci_build(aws_profile, project, project_url)
