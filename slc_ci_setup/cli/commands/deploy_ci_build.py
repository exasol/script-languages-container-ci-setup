import click

from slc_ci_setup.cli.cli import cli
from slc_ci_setup.cli.common import add_options
from slc_ci_setup.cli.options import slc_projects
from slc_ci_setup.lib.run_deploy_ci_build import run_deploy_ci_build
from slc_ci_setup.cli.options.aws_options import aws_options


CODE_BUILD_STACK_NAME = "CIBuild"


@cli.command()
@add_options(aws_options)
@click.option('--project', type=click.Choice(slc_projects.get_project_names()), required=True, show_default=True,
                 help="""The project for which the stack will be created.""")
def deploy_ci_build(
        aws_profile: str,
        project: str
        ):
    run_deploy_ci_build(aws_profile, project,
                        slc_projects.get_project_url(project), f"{project}{CODE_BUILD_STACK_NAME}")
