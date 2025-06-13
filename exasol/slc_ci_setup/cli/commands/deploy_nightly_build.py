import click

import exasol.slc_ci_setup.lib.deploy_build as lib_deploy_build
from exasol.slc_ci_setup.cli.cli import cli


@cli.command()
@click.option("--test/--no-test", default=False)
def deploy_nightly_build(test: bool):
    lib_deploy_build.deploy_build(
        build_type=lib_deploy_build.BuildType.NIGHTLY, test_only=test
    )
