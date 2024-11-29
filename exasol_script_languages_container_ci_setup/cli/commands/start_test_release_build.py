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
from exasol_script_languages_container_ci_setup.lib.github_draft_release_creator import (
    GithubDraftReleaseCreator,
)
from exasol_script_languages_container_ci_setup.lib.run_start_build import (
    run_start_test_release_build,
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
    "--repo-name",
    type=str,
    required=True,
    help="""The repository for which the test release should be created. 
              For example 'exasol/script-languages'.""",
)
@click.option(
    "--branch",
    type=str,
    required=True,
    help="""The branch for which the test release should be created.""",
)
@click.option(
    "--release-title",
    type=str,
    required=True,
    help="""The title of the Github draft release which will be created.""",
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
    help="Configuration file for build (project specific).",
)
def start_test_release_build(
    aws_profile: Optional[str],
    log_level: str,
    repo_name: str,
    project: str,
    branch: str,
    release_title: str,
    timeout_in_seconds: Optional[str],
    config_file: Optional[str],
):
    """
    This command creates a release draft on Github and triggers the AWS release Codebuild to upload the
    release artifacts onto the new Github release.
    """
    set_log_level(log_level)
    run_start_test_release_build(
        aws_access=AwsAccess(aws_profile),
        gh_release_creator=GithubDraftReleaseCreator(),
        repo_name=repo_name,
        project=project,
        branch=branch,
        release_title=release_title,
        gh_token=os.getenv("GITHUB_TOKEN"),
        timeout_in_seconds=timeout_in_seconds,
        config_file_path=config_file,
    )
