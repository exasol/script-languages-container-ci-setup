import dataclasses
from typing import (
    Any,
    Dict,
)

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    ARN,
)

ARN_KEY = "ARN"


@dataclasses.dataclass(frozen=True)
class Secret:
    arn: ARN

    @classmethod
    def from_boto(cls, boto_secret: dict[str, Any]) -> "Secret":
        aws_arn = boto_secret[ARN_KEY]
        if aws_arn is None:
            raise ValueError("ARN was None")
        arn = ARN(aws_arn=aws_arn)
        secret = Secret(arn=arn)
        return secret
