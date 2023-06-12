import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.codebuild import BuildBatch
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId


def test_id_exists():
    expected_id = PhysicalResourceId("expected_id")
    boto_buildbatch = {"id": expected_id.aws_physical_resource_id}
    build_batch = BuildBatch.from_boto(boto_buildbatch)
    assert build_batch.id == expected_id


def test_id_not_exists():
    boto_buildbatch = {}
    with pytest.raises(KeyError):
        build_batch = BuildBatch.from_boto(boto_buildbatch)


def test_with_extra_keys():
    expected_id = PhysicalResourceId("expected_id")
    boto_buildbatch = {
        "id": expected_id.aws_physical_resource_id,
        "extra1": None,
        "extra2": 1
    }
    build_batch = BuildBatch.from_boto(boto_buildbatch)
    assert build_batch.id == expected_id


def test_empty_id():
    with pytest.raises(ValueError, match="id was None"):
        boto_buildbatch = {"id": None}
        build_batch = BuildBatch.from_boto(boto_buildbatch)
