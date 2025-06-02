import dataclasses
from enum import (
    Enum,
    auto,
)
from typing import (
    Any,
    Dict,
    Optional,
)

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)

BUILD_BATCH_STATUS = "buildBatchStatus"

ID = "id"


class BuildBatchStatus(Enum):
    SUCCEEDED = auto()
    FAILED = auto()
    FAULT = auto()
    TIMED_OUT = auto()
    IN_PROGRESS = auto()
    STOPPED = auto()


@dataclasses.dataclass(frozen=True)
class BuildBatch:
    id: Optional[PhysicalResourceId]
    build_batch_status: Optional[BuildBatchStatus]

    @classmethod
    def from_boto(self, boto_buildbatch: dict[str, Any]) -> "BuildBatch":
        batch_id = self._extract_build_id(boto_buildbatch)
        build_batch_status = self._extract_build_batch_status(boto_buildbatch)
        build_batch = BuildBatch(id=batch_id, build_batch_status=build_batch_status)
        return build_batch

    @classmethod
    def _extract_build_id(
        cls, boto_buildbatch: dict[str, Any]
    ) -> Optional[PhysicalResourceId]:
        batch_id = None
        if BuildBatch._has_id(boto_buildbatch):
            batch_id = PhysicalResourceId(aws_physical_resource_id=boto_buildbatch[ID])
        return batch_id

    @classmethod
    def _has_id(cls, boto_buildbatch: dict[str, Any]) -> bool:
        return ID in boto_buildbatch and boto_buildbatch[ID] is not None

    @classmethod
    def _extract_build_batch_status(
        cls, boto_buildbatch: dict[str, Any]
    ) -> Optional[BuildBatchStatus]:
        build_batch_status = None
        if BuildBatch._has_build_status(boto_buildbatch):
            build_batch_status = BuildBatchStatus[boto_buildbatch[BUILD_BATCH_STATUS]]
        return build_batch_status

    @classmethod
    def _has_build_status(cls, boto_buildbatch: dict[str, Any]) -> bool:
        return (
            BUILD_BATCH_STATUS in boto_buildbatch
            and boto_buildbatch[BUILD_BATCH_STATUS] is not None
        )
