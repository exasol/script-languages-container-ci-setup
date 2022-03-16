import click

from slc_ci_setup.cli.cli import cli
from slc_ci_setup.cli.common import add_options
from slc_ci_setup.lib.run_deploy_ci_build import run_deploy_ci_build
from slc_ci_setup.cli.options.aws_options import aws_options


CODE_BUILD_STACK_NAME = "CIBuild"
SLC_PROJECT = "ScriptLanguages"
SLC_RELEASE_PROJECT = "ScriptLanguagesRelease"

GITHUB_URLS = {
    SLC_PROJECT : "https://github.com/exasol/script-languages",
    SLC_RELEASE_PROJECT : "https://github.com/exasol/script-languages-release"
}


@cli.command()
@add_options(aws_options)
@click.option('--project', type=click.Choice([SLC_PROJECT,  SLC_RELEASE_PROJECT]), default="""ScriptLanguagesRelease""",
                 show_default=True,
                 help="""The project for which the stack will be created.""")
def deploy_ci_build(
        aws_profile: str,
        project: str
        ):
    run_deploy_ci_build(aws_profile, project, GITHUB_URLS[project], f"{project}{CODE_BUILD_STACK_NAME}")
