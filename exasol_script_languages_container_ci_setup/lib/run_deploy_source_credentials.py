import exasol_script_languages_container_ci_setup
from exasol_script_languages_container_ci_setup.lib import render_template


def run_deploy_source_credentials(
        aws_profile: str,
        secret_name: str,
        secret_user_key: str,
        secret_token_key: str,
        stack_name: str):
    """
    This command deploys the source credential as cloudformation stack.
    """
    yml = render_template("slc_source_credential.yaml",
                          secret_name=secret_name,
                          secret_user_key=secret_user_key,
                          secret_token_key=secret_token_key)
    exasol_script_languages_container_ci_setup.lib.upload_cloudformation_stack(aws_profile, yml, stack_name)
