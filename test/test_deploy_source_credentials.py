from unittest.mock import patch, MagicMock

import pytest

from exasol_script_languages_container_ci_setup.lib import render_template
from exasol_script_languages_container_ci_setup.lib.run_deploy_source_credentials import run_deploy_source_credentials

from test.cloudformation_validation import validate_using_cfn_lint, validate_using_aws

SECRET_NAME = "test_secret"
SECRET_USER_KEY = "test_secret_user_key"
SECRET_TOKEN_KEY = "test_secret_token_key"


@pytest.fixture
def source_credentials_yml():
    return render_template("slc_source_credential.yaml",
                           secret_name=SECRET_NAME,
                           secret_user_key=SECRET_USER_KEY,
                           secret_token_key=SECRET_TOKEN_KEY)


def test_deploy_source_credentials_upload_invoked(source_credentials_yml):
    """
    Test if function upload_cloudformation_stack() will be invoked with expected values
    when we run run_deploy_source_credentials()
    """
    AWS_PROFILE = "test_aws"
    STACK_NAME = "test_stack"
    with patch("exasol_script_languages_container_ci_setup.lib.upload_cloudformation_stack",
               MagicMock()) as patched_upload:
        run_deploy_source_credentials(aws_profile=AWS_PROFILE, secret_name=SECRET_NAME,
                                      secret_user_key=SECRET_USER_KEY, secret_token_key=SECRET_TOKEN_KEY,
                                      stack_name=STACK_NAME)
        patched_upload.assert_called_once_with(AWS_PROFILE, source_credentials_yml, STACK_NAME)


def test_deploy_source_credentials_template(source_credentials_yml):
    validate_using_aws(source_credentials_yml)


def test_deploy_source_credentials_template_with_cnf_lint(tmp_path, source_credentials_yml):
    validate_using_cfn_lint(tmp_path, source_credentials_yml)
