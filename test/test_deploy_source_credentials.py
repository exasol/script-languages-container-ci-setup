from unittest.mock import patch, MagicMock

from exasol_script_languages_container_ci_setup.lib import render_template
from exasol_script_languages_container_ci_setup.lib.run_deploy_source_credentials import run_deploy_source_credentials


def test_deploy_ci():
    AWS_PROFILE = "test_aws"
    SECRET_NAME = "test_secret"
    SECRET_USER_KEY = "test_secret_user_key"
    SECRET_TOKEN_KEY = "test_secret_token_key"
    STACK_NAME = "test_stack"
    with patch("exasol_script_languages_container_ci_setup.lib.upload_cloudformation_stack",
               MagicMock()) as patched_upload:
        run_deploy_source_credentials(aws_profile=AWS_PROFILE, secret_name=SECRET_NAME,
                                      secret_user_key=SECRET_USER_KEY, secret_token_key=SECRET_TOKEN_KEY,
                                      stack_name=STACK_NAME)
        expected_cloudformation_template = render_template("slc_source_credential.yaml",
                                                           secret_name=SECRET_NAME,
                                                           secret_user_key=SECRET_USER_KEY,
                                                           secret_token_key=SECRET_TOKEN_KEY)
        patched_upload.assert_called_once_with(AWS_PROFILE, expected_cloudformation_template, STACK_NAME)

