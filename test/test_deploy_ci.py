from unittest.mock import patch, MagicMock

import pytest

from exasol_script_languages_container_ci_setup.lib import render_template, validate_cloudformation_template
from exasol_script_languages_container_ci_setup.lib.ci_build import run_deploy_ci_build, stack_name
from test.cloudformation_validation import validate_using_cfn_lint

PROJECT = "slc"
GH_URL = "https://github.com/slc"
DOCKERHUB_SECRET_ARN = "super_secret_arn"


@pytest.fixture
def ci_code_build_yml():
    return render_template("slc_code_build.yaml", project=PROJECT,
                           dockerhub_secret_arn=DOCKERHUB_SECRET_ARN, github_url=GH_URL)


@patch("exasol_script_languages_container_ci_setup.lib.read_dockerhub_secret_arn",
       MagicMock(return_value=DOCKERHUB_SECRET_ARN))
def test_deploy_ci_upload_invoked(ci_code_build_yml):
    """"
    Test if function upload_cloudformation_stack() will be invoked
    with expected values when we run run_deploy_ci_build()
    """
    AWS_PROFILE = "test_aws"
    with patch("exasol_script_languages_container_ci_setup.lib.upload_cloudformation_stack",
               MagicMock()) as patched_upload:
        run_deploy_ci_build(aws_profile=AWS_PROFILE, project=PROJECT,
                            github_url=GH_URL)
        patched_upload.assert_called_once_with(AWS_PROFILE, ci_code_build_yml, stack_name(PROJECT))


def test_deploy_ci_template(ci_code_build_yml):
    validate_cloudformation_template(ci_code_build_yml, None)


def test_deploy_ci_template_with_cnf_lint(tmp_path, ci_code_build_yml):
    validate_using_cfn_lint(tmp_path, ci_code_build_yml)
