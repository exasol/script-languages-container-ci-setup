import datetime
from typing import Union
from unittest.mock import MagicMock, create_autospec, call

from dateutil.tz import tzutc

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import StackResourceSummary
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId
from exasol_script_languages_container_ci_setup.lib.github_draft_release_creator import GithubDraftReleaseCreator
from exasol_script_languages_container_ci_setup.lib.run_start_build import run_start_test_release_build
from test.mock_cast import mock_cast

REPO_NAME = "script-languages-repo"
BRANCH = "main"
GITHUB_TOKEN = "gh_secret"
RELEASE_TITLE = "test-release"


def test_run_test_release_build():
    """
    Test if invocation of run_start_test_release_build calls AwsAccess with expected arguments.
    """
    aws_access_mock: Union[MagicMock, AwsAccess] = create_autospec(AwsAccess)
    physical_resource_id = PhysicalResourceId(aws_physical_resource_id="id")
    aws_access_mock.get_all_stack_resources.return_value = [
        StackResourceSummary(physical_resource_id=None,
                             resource_type="SomethingElse"),
        StackResourceSummary(physical_resource_id=physical_resource_id,
                             resource_type="AWS::CodeBuild::Project"),
        StackResourceSummary(physical_resource_id=None,
                             resource_type="SomethingElse")
    ]
    timeout_time_in_seconds = 30
    github_release_creator_mock: Union[MagicMock, GithubDraftReleaseCreator] = \
        create_autospec(GithubDraftReleaseCreator)
    mock_cast(github_release_creator_mock.create_release).return_value = 123
    expected_env_variable_overrides = [
        {"name": "RELEASE_ID", "value": "123", "type": "PLAINTEXT"},
        {"name": "DRY_RUN", "value": "--dry-run", "type": "PLAINTEXT"},
        {"name": "GITHUB_TOKEN", "value": GITHUB_TOKEN, "type": "PLAINTEXT"}
    ]

    run_start_test_release_build(aws_access=aws_access_mock, gh_release_creator=github_release_creator_mock,
                                 project="slc", repo_name=REPO_NAME, branch=BRANCH,
                                 release_title=RELEASE_TITLE, gh_token=GITHUB_TOKEN)

    assert call.start_codebuild(physical_resource_id,
                                environment_variables_overrides=expected_env_variable_overrides,
                                branch=BRANCH) \
           in aws_access_mock.mock_calls
