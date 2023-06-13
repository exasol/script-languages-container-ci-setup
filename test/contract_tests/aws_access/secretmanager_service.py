import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId, ARN
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.secretsmanager import Secret
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.secretsmanager_service import SecretsManagerService


class GetSecretValueArnEqualContract:

    @pytest.fixture(scope="class")
    def secretmanager_service(self) -> SecretsManagerService:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def secret_id(self) -> PhysicalResourceId:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def expected_secret_arn(self) -> ARN:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def secret(self, secretmanager_service, secret_id) -> Secret:
        secret = secretmanager_service.get_secret_value(secret_id)
        return secret

    def test_id(self, secret, expected_secret_arn):
        assert secret.arn == expected_secret_arn
