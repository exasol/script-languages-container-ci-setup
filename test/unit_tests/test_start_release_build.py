from pathlib import Path
from typing import Union
from unittest.mock import MagicMock, create_autospec, call

import pytest
from exasol_script_languages_container_ci.lib.config.config_data_model import Build, Ignore, Release, Config

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import StackResourceSummary
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId
from exasol_script_languages_container_ci_setup.lib.run_start_build import run_start_release_build, DEFAULT_TIMEOUT

UPLOAD_URL = "https://uploads.github.com/repos/exasol/script-languages-repo/releases/123/assets{?name,label}"
BRANCH = "main"
GITHUB_TOKEN = "gh_secret"


@pytest.mark.parametrize(
    ("timeout_in_seconds", "config_file_timeout", "expected_result"),
    [
        (None, None, DEFAULT_TIMEOUT),
        (10, None, 10),
        (None, 20, 20),
        (30, 40, 30),
    ]
)
def test_run_release_build(timeout_in_seconds: int, config_file_timeout: int, expected_result: int, tmp_path: Path):
    """
    Test if invocation of run_start_release_build calls AwsAccess with expected arguments.
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
    expected_env_variable_overrides = [
        {"name": "RELEASE_ID", "value": "123", "type": "PLAINTEXT"},
        {"name": "DRY_RUN", "value": "--no-dry-run", "type": "PLAINTEXT"},
        {"name": "GITHUB_TOKEN", "value": GITHUB_TOKEN, "type": "PLAINTEXT"}
    ]

    if config_file_timeout is not None:
        config_file = str(tmp_path / "config.json")
        config = Config(build=Build(base_branch="master", ignore=Ignore(paths=[])),
                        release=Release(timeout_in_minutes=config_file_timeout))
        with open(config_file, "w") as f:
            f.write(config.json())
    else:
        config_file = None

    run_start_release_build(
        aws_access=aws_access_mock,
        project="slc",
        upload_url=UPLOAD_URL,
        branch=BRANCH,
        gh_token=GITHUB_TOKEN,
        timeout_in_seconds=timeout_in_seconds,
        config_file_path=config_file)

    assert call.start_codebuild(physical_resource_id,
                                environment_variables_overrides=expected_env_variable_overrides,
                                branch=BRANCH,
                                timeout_in_seconds=expected_result) \
           in aws_access_mock.mock_calls
