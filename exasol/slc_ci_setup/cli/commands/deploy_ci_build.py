import exasol.slc_ci_setup.lib.deploy_ci_build as lib_deploy_ci_build
from exasol.slc_ci_setup.cli.cli import cli


@cli.command()
def deploy_ci_build():
    lib_deploy_ci_build.deploy_ci_build()
