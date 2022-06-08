from unittest.mock import MagicMock

import pytest

from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.ci_build import run_deploy_ci_build, ci_stack_name, \
    CI_BUILD_WEBHOOK_FILTER_PATTERN
from exasol_script_languages_container_ci_setup.lib.release_build import run_deploy_release_build, release_stack_name
from exasol_script_languages_container_ci_setup.lib.render_template import render_template
from test.cloudformation_validation import validate_using_cfn_lint

PROJECT = "slc"
GH_URL = "https://github.com/slc"
DOCKERHUB_SECRET_ARN = "super_secret_arn"


@pytest.fixture
def ci_code_build_yml():
    return render_template("slc_code_build.yaml", project=PROJECT,
                           dockerhub_secret_arn=DOCKERHUB_SECRET_ARN, github_url=GH_URL,
                           webhook_filter_pattern=CI_BUILD_WEBHOOK_FILTER_PATTERN)


def test_deploy_ci_upload_invoked(ci_code_build_yml):
    """"
    Test if function upload_cloudformation_stack() will be invoked
    with expected values when we run run_deploy_ci_build()
    """
    aws_access_mock = MagicMock()
    aws_access_mock.read_dockerhub_secret_arn.return_value = DOCKERHUB_SECRET_ARN
    run_deploy_ci_build(aws_access=aws_access_mock, project=PROJECT,
                        github_url=GH_URL)
    aws_access_mock.upload_cloudformation_stack.assert_called_once_with(ci_code_build_yml, ci_stack_name(PROJECT))


def test_deploy_ci_template(ci_code_build_yml):
    aws_access = AwsAccess(None)
    aws_access.validate_cloudformation_template(ci_code_build_yml)


def test_deploy_ci_template_with_cnf_lint(tmp_path, ci_code_build_yml):
    validate_using_cfn_lint(tmp_path, ci_code_build_yml)


@pytest.fixture
def release_code_build_yml():
    return render_template("slc_code_release_build.yaml", project=PROJECT,
                           dockerhub_secret_arn=DOCKERHUB_SECRET_ARN, github_url=GH_URL)


def test_deploy_release_upload_invoked(release_code_build_yml):
    """"
    Test if function upload_cloudformation_stack() will be invoked
    with expected values when we run run_deploy_release_build()
    """
    aws_access_mock = MagicMock()
    aws_access_mock.read_dockerhub_secret_arn.return_value = DOCKERHUB_SECRET_ARN
    run_deploy_release_build(aws_access=aws_access_mock, project=PROJECT,
                             github_url=GH_URL)
    aws_access_mock.upload_cloudformation_stack.assert_called_once_with(release_code_build_yml,
                                                                        release_stack_name(PROJECT))


def test_deploy_release_template(release_code_build_yml):
    aws_access = AwsAccess(None)
    aws_access.validate_cloudformation_template(release_code_build_yml)


def test_deploy_release_template_with_cnf_lint(tmp_path, release_code_build_yml):
    validate_using_cfn_lint(tmp_path, release_code_build_yml)
