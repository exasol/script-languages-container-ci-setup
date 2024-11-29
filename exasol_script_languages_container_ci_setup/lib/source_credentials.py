import logging

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.render_template import (
    render_template,
)

SOURCE_CREDENTIALS_STACK_NAME = "SLCSourceCredentials"


def run_deploy_source_credentials(
    aws_access: AwsAccess, secret_name: str, secret_user_key: str, secret_token_key: str
):
    """
    This command deploys the source credential as cloudformation stack.
    """
    logging.info(
        f"run_deploy_source_credentials for aws profile {aws_access.aws_profile}"
    )
    yml = render_template(
        "slc_source_credential.yaml",
        secret_name=secret_name,
        secret_user_key=secret_user_key,
        secret_token_key=secret_token_key,
    )
    aws_access.upload_cloudformation_stack(yml, SOURCE_CREDENTIALS_STACK_NAME)


def run_validate_source_credentials(
    aws_access: AwsAccess, secret_name: str, secret_user_key: str, secret_token_key: str
):
    """
    This command deploys the source credential as cloudformation stack.
    """
    logging.info(
        f"run_validate_source_credentials for aws profile {aws_access.aws_profile}"
    )
    yml = render_template(
        "slc_source_credential.yaml",
        secret_name=secret_name,
        secret_user_key=secret_user_key,
        secret_token_key=secret_token_key,
    )
    aws_access.validate_cloudformation_template(yml)
