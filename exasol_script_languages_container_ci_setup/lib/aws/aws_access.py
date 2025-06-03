import logging
import time
from collections.abc import Iterable
from typing import (
    Callable,
    Dict,
    List,
    Optional,
)

from botocore.exceptions import ClientError

from exasol_script_languages_container_ci_setup.lib.aws.deployer import Deployer
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.aws_client import (
    AwsClient,
    AwsClientFactory,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import (
    StackResourceSummary,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.codebuild import (
    BuildBatchStatus,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)

BUILD_STATUS_FAILURES = [
    BuildBatchStatus.FAILED,
    BuildBatchStatus.FAULT,
    BuildBatchStatus.STOPPED,
    BuildBatchStatus.TIMED_OUT,
]


class AwsAccess:
    def __init__(
        self,
        aws_profile: Optional[str],
        aws_client_factory: AwsClientFactory = AwsClientFactory(),
    ):
        self._aws_client_factory = aws_client_factory
        self._aws_profile = aws_profile

    @property
    def aws_profile_for_logging(self) -> str:
        if self._aws_profile is not None:
            return self._aws_profile
        else:
            return "{default}"

    @property
    def aws_profile(self) -> Optional[str]:
        return self._aws_profile

    def _get_aws_client(self) -> AwsClient:
        return self._aws_client_factory.create(profile=self._aws_profile)

    def upload_cloudformation_stack(self, yml: str, stack_name: str):
        """
        Deploy the cloudformation stack.
        """
        logging.debug(
            f"Running upload_cloudformation_stack for aws profile {self.aws_profile_for_logging}"
        )
        client = self._get_aws_client().create_cloudformation_service()
        try:
            cfn_deployer = Deployer(cloudformation_client=client.internal_aws_client)
            result = cfn_deployer.create_and_wait_for_changeset(
                stack_name=stack_name,
                cfn_template=yml,
                parameter_values=[],
                capabilities=("CAPABILITY_IAM",),
                role_arn=None,
                notification_arns=None,
                tags=tuple(),
            )
        except Exception as e:
            logging.error(f"Error creating changeset for cloud formation template: {e}")
            raise e
        try:
            cfn_deployer.execute_changeset(
                changeset_id=result.changeset_id, stack_name=stack_name
            )
            cfn_deployer.wait_for_execute(
                stack_name=stack_name, changeset_type=result.changeset_type
            )
        except Exception as e:
            logging.error(
                f"Error executing changeset for cloud formation template: {e}"
            )
            logging.error(
                f"Run 'aws cloudformation describe-stack-events --stack-name {stack_name}' to get details."
            )
            raise e

    def read_secret_arn(self, secret_name: str):
        """
        Uses Boto3 to retrieve the ARN of a secret.
        """
        logging.debug(
            f"Reading secret for getting ARN, secret name = {secret_name}, "
            f"for aws profile {self.aws_profile_for_logging}"
        )
        client = self._get_aws_client().create_secretsmanager_service()

        try:
            secret = client.get_secret_value(secret_id=PhysicalResourceId(secret_name))
            return secret.arn
        except ClientError as e:
            logging.error("Unable to read secret")
            raise e

    def read_dockerhub_secret_arn(self):
        return self.read_secret_arn("Dockerhub")

    def validate_cloudformation_template(self, cloudformation_yml) -> None:
        """
        This function pushes the YAML to AWS Cloudformation for validation
        (see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-validate-template.html)
        Pitfall: Boto3 expects the YAML string as parameter, whereas the AWS CLI expects the file URL as parameter.
        It requires to have the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables set correctly.
        """
        logging.debug(
            f"Running validate_cloudformation_template for aws profile {self.aws_profile_for_logging}"
        )
        client = self._get_aws_client().create_cloudformation_service()
        client.validate_template(template_body=cloudformation_yml)

    def get_all_stack_resources(self, stack_name: str) -> list[StackResourceSummary]:
        """
        This functions uses Boto3 to get all AWS Cloudformation resources for a specific Cloudformation stack,
        identified by parameter `stack_name`.
        The AWS API truncates at a size of 1MB, and in order to get all chunks the method must be called
        passing the previous retrieved token until no token is returned.
        """
        logging.debug(
            f"Running get_all_codebuild_projects for aws profile {self.aws_profile_for_logging}"
        )
        client = self._get_aws_client().create_cloudformation_service()
        stack_name_id = PhysicalResourceId(stack_name)
        current_result = client.list_stack_resources(stack_name=stack_name_id)
        result = current_result.stack_resource_summaries

        while current_result.next_token is not None:
            current_result = client.list_stack_resources(
                stack_name=stack_name_id, next_token=current_result.next_token
            )
            result.extend(current_result.stack_resource_summaries)
        return result

    def start_codebuild(
        self,
        project: PhysicalResourceId,
        environment_variables_overrides: list[dict[str, str]],
        branch: str,
        timeout_in_seconds: int,
        poll_interval_seconds: int = 30,
        sleep_function: Callable[[float], None] = time.sleep,
    ) -> None:
        """
        This functions uses Boto3 to start a batch build.
        It forwards all variables from parameter env_variables as environment variables to the CodeBuild project.
        If a branch is given, it starts the codebuild for the given branch.
        After the build has triggered it waits until the batch build finished
        :raises
            `RuntimeError` if build fails or AWS Batch build returns unknown status
        """
        client = self._get_aws_client().create_codebuild_service()
        logging.info(
            f"Trigger codebuild for project {project} with branch {branch} "
            f"and env_variables ({environment_variables_overrides})"
        )
        build_batch = client.start_build_batch(
            project_name=project,
            source_version=branch,
            environment_variables_override=list(environment_variables_overrides),
        )

        def wait_for(seconds: int, interval: int) -> Iterable[int]:
            for _ in range(int(seconds / interval)):
                yield interval

        build_id = build_batch.id
        logging.debug(
            f"Codebuild for project {project} with branch {branch} triggered. Id is {build_id}."
        )
        for seconds_to_wait in wait_for(
            seconds=timeout_in_seconds, interval=poll_interval_seconds
        ):
            sleep_function(seconds_to_wait)
            logging.debug(f"Checking status of codebuild id {build_id}.")
            build_batches = client.batch_get_build_batches(build_batch_ids=[build_id])
            logging.debug(
                f"Build response of codebuild id {build_id} is {build_batches}"
            )
            if len(build_batches) != 1:
                logging.error(
                    f"Unexpected return value from 'batch_get_build_batches': {build_batches}"
                )
            build_status = build_batches[0].build_batch_status
            logging.info(f"Build status of codebuild id {build_id} is {build_status}")
            if build_status == BuildBatchStatus.SUCCEEDED:
                break
            elif build_status in BUILD_STATUS_FAILURES:
                raise RuntimeError(
                    f"Build ({build_id}) failed with status: {build_status.name}"
                )
        # if loop does not break early, build wasn't successful
        else:
            raise RuntimeError(f"Batch build {build_id} ran into timeout.")
