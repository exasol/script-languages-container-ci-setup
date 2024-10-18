import dataclasses
from typing import Any


@dataclasses.dataclass(frozen=True)
class ARN:
    """
    This class represents a AWS ARN
    We use a dataclass to encapsulate the original value of the ARN, to decouple our abstraction from AWS.
    This way we don't care when AWS should change its datatype.
    """

    aws_arn: Any


@dataclasses.dataclass(frozen=True)
class PhysicalResourceId:
    """
    This class represents a AWS PhysicalResourceId.
    We use a dataclass to encapsulate the original value of the PhysicalResourceId,
    to decouple our abstraction from AWS. This way we don't care when AWS should change its datatype.
    """

    aws_physical_resource_id: Any
