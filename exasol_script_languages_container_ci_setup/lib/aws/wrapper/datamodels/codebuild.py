import dataclasses
from typing import Dict, Any

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId

ID = "id"


@dataclasses.dataclass(frozen=True)
class BuildBatch:
    id: PhysicalResourceId

    @classmethod
    def from_boto(self, boto_buildbatch: Dict[str, Any]) -> "BuildBatch":
        id = boto_buildbatch[ID]
        if id is None:
            raise ValueError("id was None")
        batch_id = PhysicalResourceId(aws_physical_resource_id=id)
        build_batch = BuildBatch(id=batch_id)
        return build_batch
