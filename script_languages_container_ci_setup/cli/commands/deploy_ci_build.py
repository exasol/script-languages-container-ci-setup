import click

from script_languages_container_ci_setup.cli.cli import cli
from script_languages_container_ci_setup.cli.common import add_options
from script_languages_container_ci_setup.lib.run_deploy_ci_build import run_deploy_ci_build
from script_languages_container_ci_setup.cli.options.aws_options import aws_options


CODE_BUILD_STACK_NAME = "CIBuild"


@cli.command()
@add_options(aws_options)
@click.option('--project', type=str, required=True,
                 help="""The project for which the stack will be created.""")
@click.option('--project-url', type=str, required=True,
                 help="""The URL of the project on Github.""")
def deploy_ci_build(
        aws_profile: str,
        project: str,
        project_url: str
        ):
    run_deploy_ci_build(aws_profile, project,
                        project_url, f"{project}{CODE_BUILD_STACK_NAME}")
