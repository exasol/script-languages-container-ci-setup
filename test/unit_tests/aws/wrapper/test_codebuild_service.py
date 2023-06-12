import dataclasses
from unittest.mock import Mock, call

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.codebuild_service import CodeBuildService
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId
from test.mock_cast import mock_cast


def test_init():
    boto_client = Mock()
    service = CodeBuildService(boto_client=boto_client)
    assert service.boto_client == boto_client


@dataclasses.dataclass(frozen=True)
class BatchGetBuildBatchesTestSetup:
    boto_client = Mock()
    batch_get_build_batches_return_values = [Mock(), Mock()]
    mock_cast(boto_client.batch_get_build_batches).return_value = {
        'buildBatches': batch_get_build_batches_return_values
    }
    from_boto = Mock()
    from_boto_return_values = [Mock(), Mock()]
    from_boto.side_effect = from_boto_return_values
    service = CodeBuildService(boto_client=boto_client)
    build_batch_ids = [PhysicalResourceId(aws_physical_resource_id="1"),
                       PhysicalResourceId(aws_physical_resource_id="2")]
    build_batches = service.batch_get_build_batches(build_batch_ids=build_batch_ids, from_boto=from_boto)
    ids = [id.aws_physical_resource_id for id in build_batch_ids]


def test_batch_get_build_batches_boto_client():
    setup = BatchGetBuildBatchesTestSetup()
    assert setup.boto_client.mock_calls == [call.batch_get_build_batches(ids=setup.ids)]


def test_batch_get_build_batches_from_boto():
    setup = BatchGetBuildBatchesTestSetup()
    assert setup.from_boto.mock_calls == [call(return_value) for return_value in
                                          setup.batch_get_build_batches_return_values]


def test_batch_get_build_batches_result():
    setup = BatchGetBuildBatchesTestSetup()
    assert setup.build_batches == setup.from_boto_return_values


@dataclasses.dataclass(frozen=True)
class StartBuildBatchTestSetup:
    boto_client = Mock()
    from_boto_input = Mock()
    start_build_batch_return_values = {"buildBatch": from_boto_input}
    mock_cast(boto_client.start_build_batch).return_value = start_build_batch_return_values
    from_boto = Mock()
    from_boto.return_value = Mock()
    service = CodeBuildService(boto_client=boto_client)
    projectName = PhysicalResourceId(aws_physical_resource_id="id")
    sourceVersion = Mock()
    environmentVariablesOverride = Mock()
    build_batch = service.start_build_batch(project_name=projectName,
                                            source_version=sourceVersion,
                                            environment_variables_override=environmentVariablesOverride,
                                            from_boto=from_boto)


def test_start_build_batch_boto_client():
    setup = StartBuildBatchTestSetup()
    assert setup.boto_client.mock_calls == [
        call.start_build_batch(projectName=setup.projectName.aws_physical_resource_id,
                               sourceVersion=setup.sourceVersion,
                               environmentVariablesOverride=setup.environmentVariablesOverride)]


def test_start_build_batch_from_boto():
    setup = StartBuildBatchTestSetup()
    assert setup.from_boto.mock_calls == [call(setup.from_boto_input)]


def test_start_build_batch_result():
    setup = StartBuildBatchTestSetup()
    assert setup.build_batch == setup.from_boto.return_value
