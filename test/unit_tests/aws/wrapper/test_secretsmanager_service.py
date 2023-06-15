import dataclasses
from unittest.mock import Mock, call

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.secretsmanager_service import SecretsManagerService
from test.mock_cast import mock_cast


def test_init():
    internal_aws_client = Mock()
    service = SecretsManagerService(internal_aws_client=internal_aws_client)
    assert service.internal_aws_client == internal_aws_client


@dataclasses.dataclass(frozen=True)
class GetSecretValueTestSetup:
    internal_aws_client = Mock()
    get_secret_value_return_values = Mock()
    mock_cast(internal_aws_client.get_secret_value).return_value = get_secret_value_return_values
    from_boto = Mock()
    from_boto_return_values = Mock()
    from_boto.return_value = from_boto_return_values
    service = SecretsManagerService(internal_aws_client=internal_aws_client)
    secret_id = PhysicalResourceId(aws_physical_resource_id="id")
    secret = service.get_secret_value(secret_id=secret_id, from_boto=from_boto)


def test_get_secret_value_internal_aws_client():
    setup = GetSecretValueTestSetup()
    assert setup.internal_aws_client.mock_calls == [call.get_secret_value(SecretId=setup.secret_id.aws_physical_resource_id)]


def test_get_secret_value_from_boto():
    setup = GetSecretValueTestSetup()
    assert setup.from_boto.mock_calls == [call(setup.get_secret_value_return_values)]


def test_get_secret_value_result():
    setup = GetSecretValueTestSetup()
    assert setup.secret == setup.from_boto_return_values
