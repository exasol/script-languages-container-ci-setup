from unittest.mock import patch, MagicMock

import pytest

from exasol_script_languages_container_ci_setup.lib import render_template
from exasol_script_languages_container_ci_setup.lib.run_deploy_ci_build import run_deploy_ci_build
from test.cloudformation_validation import validate_using_cfn_lint, validate_using_aws

PROJECT = "slc"
GH_URL = "https://github.com/slc"
DOCKERHUB_SECRET_ARN = "super_secret_arn"


@pytest.fixture
def ci_code_build_yml():
    return render_template("slc_code_build.yaml", project=PROJECT,
                           dockerhub_secret_arn=DOCKERHUB_SECRET_ARN, github_url=GH_URL)


@patch("exasol_script_languages_container_ci_setup.lib.read_dockerhub_secret_name",
       MagicMock(return_value=DOCKERHUB_SECRET_ARN))
def test_deploy_ci_upload_invoked(ci_code_build_yml):
    """"
    Test if function upload_cloudformation_stack() will be invoked
    with expected values when we run run_deploy_ci_build()
    """
    AWS_PROFILE = "test_aws"
    STACK_NAME = "test_stack"
    with patch("exasol_script_languages_container_ci_setup.lib.upload_cloudformation_stack",
               MagicMock()) as patched_upload:
        run_deploy_ci_build(aws_profile=AWS_PROFILE, project=PROJECT,
                            github_url=GH_URL, stack_name=STACK_NAME)
        patched_upload.assert_called_once_with(AWS_PROFILE, ci_code_build_yml, STACK_NAME)


def test_deploy_ci_template(ci_code_build_yml):
    validate_using_aws(ci_code_build_yml)


def test_deploy_ci_template_with_cnf_lint(tmp_path, ci_code_build_yml):
    validate_using_cfn_lint(tmp_path, ci_code_build_yml)
