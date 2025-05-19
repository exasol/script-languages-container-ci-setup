from test.unit.aws.cloudformation_validation import validate_using_cfn_lint
from typing import Union
from unittest.mock import (
    MagicMock,
    call,
    create_autospec,
)

import pytest

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    ARN,
)
from exasol_script_languages_container_ci_setup.lib.ci_build import (
    CI_BUILD_WEBHOOK_FILTER_PATTERN,
    ci_stack_name,
    run_deploy_ci_build,
)
from exasol_script_languages_container_ci_setup.lib.release_build import (
    release_stack_name,
    run_deploy_release_build,
)
from exasol_script_languages_container_ci_setup.lib.render_template import (
    render_template,
)

PROJECT = "slc"
GH_URL = "https://github.com/slc"
DOCKERHUB_SECRET_ARN = "super_secret_arn"


@pytest.fixture
def ci_code_build_yml():
    return render_template(
        "slc_code_build.yaml",
        project=PROJECT,
        dockerhub_secret_arn=DOCKERHUB_SECRET_ARN,
        github_url=GH_URL,
        webhook_filter_pattern=CI_BUILD_WEBHOOK_FILTER_PATTERN,
    )


def test_deploy_ci_upload_invoked(ci_code_build_yml):
    """ "
    Test if function upload_cloudformation_stack() will be invoked
    with expected values when we run run_deploy_ci_build()
    """
    aws_access_mock: Union[MagicMock, AwsAccess] = create_autospec(AwsAccess)
    aws_access_mock.read_dockerhub_secret_arn.return_value = ARN(
        aws_arn=DOCKERHUB_SECRET_ARN
    )
    run_deploy_ci_build(aws_access=aws_access_mock, project=PROJECT, github_url=GH_URL)
    assert (
        call.upload_cloudformation_stack(ci_code_build_yml, ci_stack_name(PROJECT))
        in aws_access_mock.mock_calls
    )


def test_deploy_ci_template_with_cnf_lint(tmp_path, ci_code_build_yml):
    validate_using_cfn_lint(tmp_path, ci_code_build_yml)


@pytest.fixture
def release_code_build_yml():
    return render_template(
        "slc_code_release_build.yaml",
        project=PROJECT,
        dockerhub_secret_arn=DOCKERHUB_SECRET_ARN,
        github_url=GH_URL,
    )


def test_deploy_release_upload_invoked(release_code_build_yml):
    """ "
    Test if function upload_cloudformation_stack() will be invoked
    with expected values when we run run_deploy_release_build()
    """
    aws_access_mock: Union[MagicMock, AwsAccess] = create_autospec(AwsAccess)
    aws_access_mock.read_dockerhub_secret_arn.return_value = DOCKERHUB_SECRET_ARN
    run_deploy_release_build(
        aws_access=aws_access_mock, project=PROJECT, github_url=GH_URL
    )
    assert (
        call.upload_cloudformation_stack(
            release_code_build_yml, release_stack_name(PROJECT)
        )
        in aws_access_mock.mock_calls
    )


def test_deploy_release_template_with_cnf_lint(tmp_path, release_code_build_yml):
    validate_using_cfn_lint(tmp_path, release_code_build_yml)
