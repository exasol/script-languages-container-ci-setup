import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.logging import logging_options, set_log_level
from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.cli.options.aws_options import aws_options
from exasol_script_languages_container_ci_setup.lib.release_build import run_validate_release_build
from exasol_script_languages_container_ci_setup.lib.run_start_release_build import run_start_release_build


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option('--project', type=str, required=True,
              help="""The project for which the stack will be created.""")
@click.option('--upload-url', type=str, required=True,
              help="""The URL of the Github release where artifacts will be stored.""")
@click.option('--branch', type=str, required=True,
              help="""The branch of the repository which will be used.""")
@click.option('--dry-run/--no-dry-run', default=False,
              help="If true, runs release without pushing the container to the docker release repository."
                   "If false, also pushes the container to the docker release repository.")
def start_release_build(
        aws_profile: str,
        log_level: str,
        project: str,
        upload_url: str,
        branch: str,
        dry_run: bool):
    set_log_level(log_level)
    run_start_release_build(AwsAccess(aws_profile), project, upload_url, branch, dry_run)
