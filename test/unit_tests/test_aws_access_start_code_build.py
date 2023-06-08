from typing import Any, Dict, List
from unittest.mock import Mock, call

import pytest

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.run_start_build import get_environment_variable_override
from test.mock_cast import mock_cast

ID = "id"

BRANCH = 'branch'

PROJECT = 'project'


class AwsAccessWithMockedAWSClient(AwsAccess):
    def __init__(self, aws_client: Any):
        super().__init__(None)
        self._aws_client = aws_client

    def _get_aws_client(self, service_name: str) -> Any:
        return self._aws_client


def create_aws_client_mock(batch_get_build_batches_return_values: List[Dict[str, List[Dict[str, Any]]]]) -> Mock:
    start_build_batch_return_value = create_start_build_batch_return_value()
    aws_client_mock = Mock()
    mock_cast(aws_client_mock.start_build_batch).return_value = start_build_batch_return_value
    mock_cast(aws_client_mock.batch_get_build_batches).side_effect = batch_get_build_batches_return_values
    return aws_client_mock


def create_start_build_batch_return_value() -> Dict[str, Dict[str, Any]]:
    start_build_batch_return_value = {
        "buildBatch": {
            "id": ID
        },
    }
    return start_build_batch_return_value


def create_batch_get_build_batches_return_value(value: str) -> Dict[str, List[Dict[str, Any]]]:
    return {
        "buildBatches": [
            {
                "buildBatchStatus": value
            }
        ]
    }


def test_success():
    batch_get_build_batches_return_values = [
        create_batch_get_build_batches_return_value("IN_PROGRESS"),
        create_batch_get_build_batches_return_value("SUCCEEDED")
    ]
    aws_client_mock = create_aws_client_mock(batch_get_build_batches_return_values)
    aws_access = AwsAccessWithMockedAWSClient(aws_client_mock)
    environment_variables_overrides = create_environment_variables_overrides()

    aws_access.start_codebuild(
        project=("%s" % PROJECT),
        branch="branch",
        environment_variables_overrides=environment_variables_overrides,
        timeout_time_in_seconds=10,
        poll_interval_seconds=1
    )
    assert aws_client_mock.mock_calls == [
        call.start_build_batch(projectName=('%s' % PROJECT),
                               sourceVersion=BRANCH,
                               environmentVariablesOverride=environment_variables_overrides),
        call.batch_get_build_batches(ids=[ID]),
        call.batch_get_build_batches(ids=[ID]),
    ]


def test_timeout():
    batch_get_build_batches_return_values = [
        create_batch_get_build_batches_return_value("IN_PROGRESS") for i in range(10)
    ]
    aws_client_mock = create_aws_client_mock(batch_get_build_batches_return_values)
    aws_access = AwsAccessWithMockedAWSClient(aws_client_mock)
    environment_variables_overrides = create_environment_variables_overrides()

    with pytest.raises(RuntimeError, match="Batch build id ran into timeout."):
        aws_access.start_codebuild(
            project=("%s" % PROJECT),
            branch="branch",
            environment_variables_overrides=environment_variables_overrides,
            timeout_time_in_seconds=3,
            poll_interval_seconds=1
        )

    assert aws_client_mock.mock_calls == [
        call.start_build_batch(projectName=('%s' % PROJECT),
                               sourceVersion=BRANCH,
                               environmentVariablesOverride=environment_variables_overrides),
        call.batch_get_build_batches(ids=[ID]),
        call.batch_get_build_batches(ids=[ID]),
        call.batch_get_build_batches(ids=[ID]),
    ]


def create_environment_variables_overrides():
    env_variables = [("RELEASE_ID", "release_id"),
                     ("DRY_RUN", "dry_run_value"),
                     ("GITHUB_TOKEN", "gh_token")]
    environment_variables_overrides = list(map(get_environment_variable_override, env_variables))
    return environment_variables_overrides
