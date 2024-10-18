import dataclasses
from abc import abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Protocol,
)

import boto3
from boto3 import Session

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.cloudformation_service import (
    CloudFormationService,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.codebuild_service import (
    CodeBuildService,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.secretsmanager_service import (
    SecretsManagerService,
)


class BotoSessionFactory(Protocol):

    @abstractmethod
    def __call__(
        self, profile_name: Optional[str] = None, region_name: Optional[str] = None
    ) -> Session: ...


class AwsClient:
    def __init__(
        self,
        profile: Optional[str] = None,
        region: Optional[str] = None,
        boto_session_factory: BotoSessionFactory = boto3.session.Session,
    ):
        self._boto_session_factory = boto_session_factory
        self._region = region
        self._profile = profile

    def _create_aws_session(self) -> Session:
        return self._boto_session_factory(
            profile_name=self._profile, region_name=self._region
        )

    def create_codebuild_service(self) -> CodeBuildService:
        session = self._create_aws_session()
        internal_aws_client = session.client("codebuild")
        return CodeBuildService(internal_aws_client=internal_aws_client)

    def create_secretsmanager_service(self) -> SecretsManagerService:
        session = self._create_aws_session()
        client = session.client("secretsmanager")
        return SecretsManagerService(internal_aws_client=client)

    def create_cloudformation_service(self) -> CloudFormationService:
        session = self._create_aws_session()
        client = session.client("cloudformation")
        return CloudFormationService(internal_aws_client=client)


class AwsClientFactory:
    def create(
        self, profile: Optional[str] = None, region: Optional[str] = None
    ) -> AwsClient:
        return AwsClient(profile=profile, region=region)
