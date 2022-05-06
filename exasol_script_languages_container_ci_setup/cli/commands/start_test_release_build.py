from typing import Optional

import click

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.logging import logging_options, set_log_level
from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.cli.options.aws_options import aws_options
from exasol_script_languages_container_ci_setup.lib.github_release_creator import GithubReleaseCreator
from exasol_script_languages_container_ci_setup.lib.run_start_release_build import run_start_test_release_build


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option('--project', type=str, required=True,
              help="""The project name. Must be same name as used for the AWS CodeBuild release stack creation.""")
@click.option('--repo-id', type=str, required=True,
              help="""The repository for which the test release should be created.""", )
@click.option('--branch', type=str, required=True,
              help="""The branch for which the test release should be created.""")
@click.option('--release-title', type=str, required=True,
              help="""The title of the Github draft release which will be created.""")
def start_test_release_build(
        aws_profile: Optional[str],
        log_level: str,
        repo_id: str,
        project: str,
        branch: str,
        release_title: str
):
    """
    This command creates a release draft on Github and triggers the AWS release Codebuild to upload the
    release artifacts onto the new Github release.
    """
    set_log_level(log_level)
    run_start_test_release_build(AwsAccess(aws_profile), GithubReleaseCreator(), repo_id, project, branch, release_title)
