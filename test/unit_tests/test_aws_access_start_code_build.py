from contextlib import suppress
from typing import Any, Dict, List, Union
from unittest.mock import Mock, call, MagicMock, create_autospec

import pytest

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.aws_client import AwsClient, AwsClientFactory
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.codebuild_service import CodeBuildService
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.codebuild import BuildBatch, BuildBatchStatus
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId
from exasol_script_languages_container_ci_setup.lib.run_start_build import get_environment_variable_override
from test.mock_cast import mock_cast

ID = "id"

BRANCH = 'branch'

PROJECT = 'project'


class TestSetup:
    def __init__(self, batch_get_build_batches_return_values: List[List[BuildBatch]]):
        self.batch_get_build_batches_return_values = batch_get_build_batches_return_values
        self.code_build_service: Union[MagicMock, CodeBuildService] = create_autospec(CodeBuildService)
        mock_cast(self.code_build_service.batch_get_build_batches).side_effect = \
            self.batch_get_build_batches_return_values
        self.started_build_batch = BuildBatch(id=PhysicalResourceId("id"), build_batch_status=None)
        mock_cast(self.code_build_service.start_build_batch).side_effect = [
            self.started_build_batch
        ]

        self.aws_client_mock: Union[MagicMock, AwsClient] = create_autospec(AwsClient)
        mock_cast(self.aws_client_mock.create_codebuild_service).side_effect = [self.code_build_service]

        self.aws_client_factory_mock: Union[MagicMock, AwsClientFactory] = create_autospec(AwsClientFactory)
        mock_cast(self.aws_client_factory_mock.create).side_effect = [self.aws_client_mock]

        self.profile = "profile"
        self.aws_access = AwsAccess(aws_profile=self.profile, aws_client_factory=self.aws_client_factory_mock)
        self.environment_variables_overrides = self._create_environment_variables_overrides()
        self.sleep_function_mock = Mock()
        self.timeout_time_in_seconds = 5
        self.poll_interval_seconds = 1

    def run_start_codebuild(self):
        self.aws_access.start_codebuild(
            project=PROJECT,
            branch=BRANCH,
            environment_variables_overrides=self.environment_variables_overrides,
            timeout_time_in_seconds=self.timeout_time_in_seconds,
            poll_interval_seconds=self.poll_interval_seconds,
            sleep_function=self.sleep_function_mock
        )

    def _create_environment_variables_overrides(self):
        env_variables = [("RELEASE_ID", "release_id"),
                         ("DRY_RUN", "dry_run_value"),
                         ("GITHUB_TOKEN", "gh_token")]
        environment_variables_overrides = list(map(get_environment_variable_override, env_variables))
        return environment_variables_overrides


def create_batch_get_build_batches_return_values_for_success() -> List[List[BuildBatch]]:
    batch_get_build_batches_return_values = [
        [
            BuildBatch(build_batch_status=BuildBatchStatus.IN_PROGRESS, id=None)
        ],
        [
            BuildBatch(build_batch_status=BuildBatchStatus.SUCCEEDED, id=None)
        ],
    ]
    return batch_get_build_batches_return_values


def test_success_aws_client_mock_call():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_success())
    setup.run_start_codebuild()
    assert setup.aws_client_mock.mock_calls == [call.create_codebuild_service()]


def test_success_aws_client_factory_mock_call():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_success())
    setup.run_start_codebuild()
    assert setup.aws_client_factory_mock.mock_calls == [call.create(profile=setup.profile)]


def test_success_code_build_service_mock_call():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_success())
    setup.run_start_codebuild()
    assert setup.code_build_service.mock_calls == [
        call.start_build_batch(
            project_name=PhysicalResourceId(aws_physical_resource_id=PROJECT),
            source_version=BRANCH,
            environment_variables_override=setup.environment_variables_overrides),
        call.batch_get_build_batches(build_batch_ids=[setup.started_build_batch.id]),
        call.batch_get_build_batches(build_batch_ids=[setup.started_build_batch.id])
    ]


def test_success_sleep_function_mock_call():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_success())
    setup.run_start_codebuild()
    assert setup.sleep_function_mock.mock_calls == [
        call(1), call(1)
    ]


def create_batch_get_build_batches_return_values_for_timeout() -> List[List[BuildBatch]]:
    batch_get_build_batches_return_values = [
        [
            BuildBatch(build_batch_status=BuildBatchStatus.IN_PROGRESS, id=None)
        ]
        for i in range(5)
    ]
    return batch_get_build_batches_return_values


def test_timeout_raises():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_timeout())
    with pytest.raises(RuntimeError, match=f"Batch build .* ran into timeout."):
        setup.run_start_codebuild()


def test_timeout_aws_client_mock_call():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_timeout())
    with suppress(Exception):
        setup.run_start_codebuild()
    assert setup.aws_client_mock.mock_calls == [call.create_codebuild_service()]


def test_timeout_aws_client_factory_mock_call():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_timeout())
    with suppress(Exception):
        setup.run_start_codebuild()
    assert setup.aws_client_factory_mock.mock_calls == [call.create(profile=setup.profile)]


def test_timeout_code_build_service_mock_call():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_timeout())
    with suppress(Exception):
        setup.run_start_codebuild()
    assert setup.code_build_service.mock_calls == [
        call.start_build_batch(
            project_name=PhysicalResourceId(aws_physical_resource_id=PROJECT),
            source_version=BRANCH,
            environment_variables_override=setup.environment_variables_overrides)
    ] + [
               call.batch_get_build_batches(build_batch_ids=[setup.started_build_batch.id])
               for _ in setup.batch_get_build_batches_return_values
           ]


def test_timeout_sleep_function_mock_call():
    setup = TestSetup(create_batch_get_build_batches_return_values_for_timeout())
    with suppress(Exception):
        setup.run_start_codebuild()
    assert setup.sleep_function_mock.mock_calls == [
        call(1) for _ in range(len(setup.batch_get_build_batches_return_values))
    ]
