import dataclasses
from typing import Any


@dataclasses.dataclass(frozen=True)
class ARN:
    aws_arn: Any


@dataclasses.dataclass(frozen=True)
class PhysicalResourceId:
    aws_physical_resource_id: Any
