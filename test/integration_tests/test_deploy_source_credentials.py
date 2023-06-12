import pytest

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.render_template import render_template

SECRET_NAME = "test_secret"
SECRET_USER_KEY = "test_secret_user_key"
SECRET_TOKEN_KEY = "test_secret_token_key"


@pytest.fixture
def source_credentials_yml():
    return render_template("slc_source_credential.yaml",
                           secret_name=SECRET_NAME,
                           secret_user_key=SECRET_USER_KEY,
                           secret_token_key=SECRET_TOKEN_KEY)


def test_deploy_source_credentials_template(source_credentials_yml):
    aws_access = AwsAccess(aws_profile=None)
    aws_access.validate_cloudformation_template(source_credentials_yml)
