import exasol.slc_ci_setup.lib.deploy_build as lib_deploy_build
from exasol.slc_ci_setup.cli.cli import cli


@cli.command()
def deploy_cd_build():
    lib_deploy_build.deploy_build(build_type=lib_deploy_build.BuildType.CD)
