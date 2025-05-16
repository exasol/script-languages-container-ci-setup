from typing import Union
from unittest.mock import (
    MagicMock,
    call,
    create_autospec,
)

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import (
    StackResourceSummary,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)
from exasol_script_languages_container_ci_setup.lib.run_start_build import (
    run_start_ci_build,
)

REPO_NAME = "script-languages-repo"
BRANCH = "feature-branch"


def test_run_ci_build():
    """
    Test if invocation of run_start_ci_build calls AwsAccess with expected arguments.
    """
    aws_access_mock: Union[MagicMock, AwsAccess] = create_autospec(AwsAccess)
    physical_resource_id = PhysicalResourceId(aws_physical_resource_id="id")
    aws_access_mock.get_all_stack_resources.return_value = [
        StackResourceSummary(physical_resource_id=None, resource_type="SomethingElse"),
        StackResourceSummary(
            physical_resource_id=physical_resource_id,
            resource_type="AWS::CodeBuild::Project",
        ),
        StackResourceSummary(physical_resource_id=None, resource_type="SomethingElse"),
    ]
    timeout_in_seconds = 30
    expected_env_variable_overrides = [
        {"name": "CUSTOM_BRANCH", "value": BRANCH, "type": "PLAINTEXT"}
    ]
    run_start_ci_build(
        aws_access=aws_access_mock,
        project="slc",
        branch=BRANCH,
        timeout_in_seconds=timeout_in_seconds,
    )

    assert (
        call.start_codebuild(
            physical_resource_id,
            environment_variables_overrides=expected_env_variable_overrides,
            branch=BRANCH,
            timeout_in_seconds=timeout_in_seconds,
        )
        in aws_access_mock.mock_calls
    )
