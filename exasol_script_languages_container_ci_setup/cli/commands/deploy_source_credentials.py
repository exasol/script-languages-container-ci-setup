import logging
import sys
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
from exasol_script_languages_container_ci_setup.lib.source_credentials import (
    run_deploy_source_credentials,
)


@cli.command()
@add_options(aws_options)
@add_options(logging_options)
@click.option(
    "--secret-name",
    required=True,
    type=str,
    help="Secret stored in AWS Secret Manager.",
)
@click.option(
    "--secret-user-key",
    required=True,
    type=str,
    help="User key stored as secret in AWS Secret Manager.",
)
@click.option(
    "--secret-token-key",
    required=True,
    type=str,
    help="Token key stored as secret in AWS Secret Manager.",
)
def deploy_source_credentials(
    aws_profile: Optional[str],
    log_level: str,
    secret_name: str,
    secret_user_key: str,
    secret_token_key: str,
):
    set_log_level(log_level)
    try:
        run_deploy_source_credentials(
            AwsAccess(aws_profile), secret_name, secret_user_key, secret_token_key
        )
    except Exception:
        logging.error("deploy_source_credentials failed.")
        sys.exit(1)
