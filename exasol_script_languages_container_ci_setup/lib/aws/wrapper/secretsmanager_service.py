import dataclasses
from typing import Any, Dict, Callable

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import ARN, PhysicalResourceId
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.secretsmanager import Secret


class SecretsManagerService:
    def __init__(self, boto_client):
        self._boto_client = boto_client

    @property
    def boto_client(self) -> Any:
        return self._boto_client

    def get_secret_value(self,
                         secret_id: PhysicalResourceId,
                         from_boto: Callable[[Dict[str, Any]], Secret]) \
            -> Secret:
        boto_secret = self._boto_client.get_secret_value(SecretId=secret_id.aws_physical_resource_id)
        secret = from_boto(boto_secret)
        return secret
