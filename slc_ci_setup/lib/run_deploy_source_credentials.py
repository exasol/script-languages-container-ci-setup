from slc_ci_setup.lib.render_cloudformation import render_cloudformation
from slc_ci_setup.lib.upload_cloudformation import upload_cloudformation_stack


def run_deploy_source_credentials(
        aws_profile: str,
        secret_name: str,
        secret_user_key: str,
        secret_token_key: str,
        stack_name: str):
    """
    This command deploys the source credential as cloudformation stack.
    """
    yml = render_cloudformation("slc_source_credential.yaml", secret_name=secret_name,
                                secret_user_key=secret_user_key, secret_token_key=secret_token_key)
    upload_cloudformation_stack(aws_profile, yml, stack_name)
