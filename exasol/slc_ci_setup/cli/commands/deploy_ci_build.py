import logging
import sys

from exasol.slc_ci_setup.cli.cli import cli
import exasol.slc_ci_setup.lib.deploy_ci_build as lib_deploy_ci_build


@cli.command()
def deploy_ci_build(
):
    try:
        lib_deploy_ci_build.deploy_ci_build()
    except Exception as e:
        logging.error("run deploy_ci_build failed.")
        sys.exit(1)
