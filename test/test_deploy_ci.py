from unittest.mock import patch, MagicMock

from exasol_script_languages_container_ci_setup.lib import render_template
from exasol_script_languages_container_ci_setup.lib.run_deploy_ci_build import run_deploy_ci_build


@patch("exasol_script_languages_container_ci_setup.lib.read_dockerhub_secret_name", MagicMock(return_value="hello"))
def test_deploy_ci():
    AWS_PROFILE = "test_aws"
    GH_URL = "https://github.com/slc"
    PROJECT = "slc"
    STACK_NAME = "test_stack"
    with patch("exasol_script_languages_container_ci_setup.lib.upload_cloudformation_stack",
               MagicMock()) as patched_upload:
        run_deploy_ci_build(aws_profile=AWS_PROFILE, project=PROJECT,
                            github_url=GH_URL, stack_name=STACK_NAME)
        expected_cloudformation_template = render_template("slc_code_build.yaml", project=PROJECT,
                                                           dockerhub_secret_arn="hello", github_url=GH_URL)
        patched_upload.assert_called_once_with(AWS_PROFILE, expected_cloudformation_template, STACK_NAME)
