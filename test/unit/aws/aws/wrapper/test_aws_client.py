import dataclasses
from test.mock_cast import mock_cast
from typing import Union
from unittest.mock import (
    MagicMock,
    Mock,
    call,
    create_autospec,
)

from boto3 import Session

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.aws_client import (
    AwsClient,
)


def test_init():
    boto_session_factory = Mock()
    aws_client = AwsClient(
        profile="profile", region="region", boto_session_factory=boto_session_factory
    )
    assert boto_session_factory.mock_calls == []


@dataclasses.dataclass
class CodeBuildServiceTestSetup:
    boto_session: Union[MagicMock, Session] = create_autospec(Session)
    boto_session_factory = Mock(return_value=boto_session)
    aws_client = AwsClient(
        profile="profile", region="region", boto_session_factory=boto_session_factory
    )
    codebuild_service = aws_client.create_codebuild_service()


def test_create_codebuild_service_boto_session_factory():
    setup = CodeBuildServiceTestSetup()
    assert setup.boto_session_factory.mock_calls == [
        call(profile_name="profile", region_name="region"),
    ]


def test_create_codebuild_service_boto_session_client():
    setup = CodeBuildServiceTestSetup()
    assert setup.boto_session.mock_calls == [
        call.client("codebuild"),
    ]


def test_create_codebuild_service_internal_aws_client():
    setup = CodeBuildServiceTestSetup()
    assert (
        setup.codebuild_service.internal_aws_client
        == mock_cast(setup.boto_session.client).return_value
    )


@dataclasses.dataclass
class CloudFormationServiceTestSetup:
    boto_session: Union[MagicMock, Session] = create_autospec(Session)
    boto_session_factory = Mock(return_value=boto_session)
    aws_client = AwsClient(
        profile="profile", region="region", boto_session_factory=boto_session_factory
    )
    cloudformation_service = aws_client.create_cloudformation_service()


def test_create_cloudformation_service_boto_session_factory():
    setup = CloudFormationServiceTestSetup()
    assert setup.boto_session_factory.mock_calls == [
        call(profile_name="profile", region_name="region"),
    ]


def test_create_cloudformation_service_boto_session_client():
    setup = CloudFormationServiceTestSetup()
    assert setup.boto_session.mock_calls == [
        call.client("cloudformation"),
    ]


def test_create_cloudformation_service_internal_aws_client():
    setup = CloudFormationServiceTestSetup()
    assert (
        setup.cloudformation_service.internal_aws_client
        == mock_cast(setup.boto_session.client).return_value
    )


@dataclasses.dataclass
class SecreteManagerServiceTestSetup:
    boto_session: Union[MagicMock, Session] = create_autospec(Session)
    boto_session_factory = Mock(return_value=boto_session)
    aws_client = AwsClient(
        profile="profile", region="region", boto_session_factory=boto_session_factory
    )
    secretsmanager_service = aws_client.create_secretsmanager_service()


def test_create_secretsmanager_service_boto_session_factory():
    setup = SecreteManagerServiceTestSetup()
    assert setup.boto_session_factory.mock_calls == [
        call(profile_name="profile", region_name="region"),
    ]


def test_create_secretsmanager_service_boto_session_client():
    setup = SecreteManagerServiceTestSetup()
    assert setup.boto_session.mock_calls == [
        call.client("secretsmanager"),
    ]


def test_create_secretsmanager_service_internal_aws_client():
    setup = SecreteManagerServiceTestSetup()
    assert (
        setup.secretsmanager_service.internal_aws_client
        == mock_cast(setup.boto_session.client).return_value
    )
