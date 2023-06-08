import pytest

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.ci_build import CI_BUILD_WEBHOOK_FILTER_PATTERN
from exasol_script_languages_container_ci_setup.lib.render_template import render_template

PROJECT = "slc"
GH_URL = "https://github.com/slc"
DOCKERHUB_SECRET_ARN = "super_secret_arn"


@pytest.fixture
def ci_code_build_yml():
    return render_template("slc_code_build.yaml", project=PROJECT,
                           dockerhub_secret_arn=DOCKERHUB_SECRET_ARN, github_url=GH_URL,
                           webhook_filter_pattern=CI_BUILD_WEBHOOK_FILTER_PATTERN)


def test_deploy_ci_template(ci_code_build_yml):
    aws_access = AwsAccess(None)
    aws_access.validate_cloudformation_template(ci_code_build_yml)


@pytest.fixture
def release_code_build_yml():
    return render_template("slc_code_release_build.yaml", project=PROJECT,
                           dockerhub_secret_arn=DOCKERHUB_SECRET_ARN, github_url=GH_URL)


def test_deploy_release_template(release_code_build_yml):
    aws_access = AwsAccess(None)
    aws_access.validate_cloudformation_template(release_code_build_yml)
