import click

from script_languages_container_ci_setup.cli.cli import cli
from script_languages_container_ci_setup.cli.common import add_options
from script_languages_container_ci_setup.lib.run_deploy_source_credentials import run_deploy_source_credentials
from script_languages_container_ci_setup.cli.options.aws_options import aws_options

SOURCE_CREDENTIALS_STACK_NAME = "SLCSourceCredentials"


@cli.command()
@add_options(aws_options)
@click.option('--secret-name', required=True, type=str,
              help="Secret stored in AWS Secret Manager.")
@click.option('--secret-user-key', required=True, type=str,
              help="User key stored as secret in AWS Secret Manager.")
@click.option('--secret-token-key', required=True, type=str,
              help="Token key stored as secret in AWS Secret Manager.")
def deploy_source_credentials(
        aws_profile: str,
        secret_name: str,
        secret_user_key: str,
        secret_token_key: str
):
    run_deploy_source_credentials(aws_profile, secret_name, secret_user_key, secret_token_key,
                                  SOURCE_CREDENTIALS_STACK_NAME)
