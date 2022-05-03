from unittest.mock import MagicMock

import pytest

from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.render_template import render_template
from exasol_script_languages_container_ci_setup.lib.source_credentials import (
    run_deploy_source_credentials,
    SOURCE_CREDENTIALS_STACK_NAME
)

from test.cloudformation_validation import validate_using_cfn_lint

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
    aws_access_mock = MagicMock()
    run_deploy_source_credentials(aws_access=aws_access_mock, secret_name=SECRET_NAME,
                                  secret_user_key=SECRET_USER_KEY, secret_token_key=SECRET_TOKEN_KEY)
    aws_access_mock.upload_cloudformation_stack.assert_called_once_with(source_credentials_yml, SOURCE_CREDENTIALS_STACK_NAME)


def test_deploy_source_credentials_template(source_credentials_yml):
    aws_access = AwsAccess(aws_profile=None)
    aws_access.validate_cloudformation_template(source_credentials_yml)


def test_deploy_source_credentials_template_with_cnf_lint(tmp_path, source_credentials_yml):
    validate_using_cfn_lint(tmp_path, source_credentials_yml)
