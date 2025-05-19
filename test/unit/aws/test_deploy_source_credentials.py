from test.unit.aws.cloudformation_validation import validate_using_cfn_lint
from typing import Union
from unittest.mock import (
    MagicMock,
    call,
    create_autospec,
)

import pytest

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.render_template import (
    render_template,
)
from exasol_script_languages_container_ci_setup.lib.source_credentials import (
    SOURCE_CREDENTIALS_STACK_NAME,
    run_deploy_source_credentials,
)

SECRET_NAME = "test_secret"
SECRET_USER_KEY = "test_secret_user_key"
SECRET_TOKEN_KEY = "test_secret_token_key"


@pytest.fixture
def source_credentials_yml():
    return render_template(
        "slc_source_credential.yaml",
        secret_name=SECRET_NAME,
        secret_user_key=SECRET_USER_KEY,
        secret_token_key=SECRET_TOKEN_KEY,
    )


def test_deploy_source_credentials_upload_invoked(source_credentials_yml):
    """
    Test if function upload_cloudformation_stack() will be invoked with expected values
    when we run run_deploy_source_credentials()
    """
    aws_access_mock: Union[MagicMock, AwsAccess] = create_autospec(AwsAccess)
    run_deploy_source_credentials(
        aws_access=aws_access_mock,
        secret_name=SECRET_NAME,
        secret_user_key=SECRET_USER_KEY,
        secret_token_key=SECRET_TOKEN_KEY,
    )
    assert (
        call.upload_cloudformation_stack(
            source_credentials_yml, SOURCE_CREDENTIALS_STACK_NAME
        )
        in aws_access_mock.mock_calls
    )


def test_deploy_source_credentials_template_with_cnf_lint(
    tmp_path, source_credentials_yml
):
    validate_using_cfn_lint(tmp_path, source_credentials_yml)
