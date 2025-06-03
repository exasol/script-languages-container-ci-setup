import dataclasses
from typing import (
    Any,
    Callable,
    Dict,
)

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    ARN,
    PhysicalResourceId,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.secretsmanager import (
    Secret,
)


class SecretsManagerService:
    def __init__(self, internal_aws_client):
        self._internal_aws_client = internal_aws_client

    @property
    def internal_aws_client(self) -> Any:
        return self._internal_aws_client

    def get_secret_value(
        self,
        secret_id: PhysicalResourceId,
        from_boto: Callable[[dict[str, Any]], Secret] = Secret.from_boto,
    ) -> Secret:
        boto_secret = self._internal_aws_client.get_secret_value(
            SecretId=secret_id.aws_physical_resource_id
        )
        secret = from_boto(boto_secret)
        return secret
