import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.codebuild import (
    BuildBatch,
    BuildBatchStatus,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)


def test_with_id():
    expected_build_batch = BuildBatch(
        id=PhysicalResourceId("expected_id"), build_batch_status=None
    )
    boto_buildbatch = {
        "id": expected_build_batch.id.aws_physical_resource_id,
    }
    build_batch = BuildBatch.from_boto(boto_buildbatch)
    assert build_batch == expected_build_batch


@pytest.mark.parametrize("status", BuildBatchStatus)
def test_with_build_batch_status(status):
    expected_build_batch = BuildBatch(
        id=None, build_batch_status=BuildBatchStatus.SUCCEEDED
    )
    boto_buildbatch = {"buildBatchStatus": expected_build_batch.build_batch_status.name}
    build_batch = BuildBatch.from_boto(boto_buildbatch)
    assert build_batch == expected_build_batch


def test_with_unknown_build_batch_status():
    boto_buildbatch = {"buildBatchStatus": "MY_UNKNOWN_BUILD_STATUS"}
    with pytest.raises(KeyError):
        build_batch = BuildBatch.from_boto(boto_buildbatch)


def test_empty():
    expected_build_batch = BuildBatch(id=None, build_batch_status=None)
    boto_buildbatch = {}
    build_batch = BuildBatch.from_boto(boto_buildbatch)
    assert build_batch == expected_build_batch


def test_with_extra_keys():
    expected_build_batch = BuildBatch(
        id=PhysicalResourceId("expected_id"),
        build_batch_status=BuildBatchStatus.SUCCEEDED,
    )
    boto_buildbatch = {
        "id": expected_build_batch.id.aws_physical_resource_id,
        "buildBatchStatus": expected_build_batch.build_batch_status.name,
        "extra1": None,
        "extra2": 1,
    }
    build_batch = BuildBatch.from_boto(boto_buildbatch)
    assert build_batch == expected_build_batch


def test_id_is_None():
    expected_build_batch = BuildBatch(id=None, build_batch_status=None)
    boto_buildbatch = {"id": None}
    build_batch = BuildBatch.from_boto(boto_buildbatch)
    assert build_batch == expected_build_batch


def test_build_batch_status_is_None():
    expected_build_batch = BuildBatch(id=None, build_batch_status=None)
    boto_buildbatch = {"buildBatchStatus": None}
    build_batch = BuildBatch.from_boto(boto_buildbatch)
    assert build_batch == expected_build_batch
