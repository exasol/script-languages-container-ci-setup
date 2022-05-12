import logging
import time
from typing import Optional, List, Dict, Any, Iterable

import boto3
from botocore.exceptions import ClientError

from exasol_script_languages_container_ci_setup.lib.deployer import Deployer


class AwsAccess(object):
    def __init__(self, aws_profile: Optional[str]):
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

    def upload_cloudformation_stack(self, yml: str, stack_name: str):
        """
        Deploy the cloudformation stack.
        """
        logging.debug(f"Running upload_cloudformation_stack for aws profile {self.aws_profile_for_logging}")
        cloud_client = self._get_aws_client("cloudformation")
        try:
            cfn_deployer = Deployer(cloudformation_client=cloud_client)
            result = cfn_deployer.create_and_wait_for_changeset(stack_name=stack_name, cfn_template=yml,
                                                                parameter_values=[],
                                                                capabilities=("CAPABILITY_IAM",), role_arn=None,
                                                                notification_arns=None, tags=tuple())
        except Exception as e:
            logging.error(f"Error creating changeset for cloud formation template: {e}")
            raise e
        try:
            cfn_deployer.execute_changeset(changeset_id=result.changeset_id, stack_name=stack_name)
            cfn_deployer.wait_for_execute(stack_name=stack_name, changeset_type=result.changeset_type)
        except Exception as e:
            logging.error(f"Error executing changeset for cloud formation template: {e}")
            logging.error(f"Run 'aws cloudformation describe-stack-events --stack-name {stack_name}' to get details.")
            raise e

    def read_secret_arn(self, secret_name: str):
        """"
        Uses Boto3 to retrieve the ARN of a secret.
        """
        logging.debug(f"Reading secret for getting ARN, secret name = {secret_name}, "
                      f"for aws profile {self.aws_profile_for_logging}")
        client = self._get_aws_client(service_name='secretsmanager')

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            return get_secret_value_response["ARN"]
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
        logging.debug(f"Running validate_cloudformation_template for aws profile {self.aws_profile_for_logging}")
        cloud_client = self._get_aws_client("cloudformation")
        cloud_client.validate_template(TemplateBody=cloudformation_yml)

    def _get_aws_client(self, service_name: str) -> Any:
        if self._aws_profile is None:
            return boto3.client(service_name)
        aws_session = boto3.session.Session(profile_name=self._aws_profile)
        return aws_session.client(service_name)

    def get_all_stack_resources(self, stack_name: str) -> List[Dict[str, str]]:
        """
        This functions uses Boto3 to get all AWS Cloudformation resources for a specific Cloudformation stack,
        identified by parameter `stack_name`.
        The AWS API truncates at a size of 1MB, and in order to get all chunks the method must be called
        passing the previous retrieved token until no token is returned.
        """
        logging.debug(f"Running get_all_codebuild_projects for aws profile {self.aws_profile_for_logging}")
        cf_client = self._get_aws_client('cloudformation')
        current_result = cf_client.list_stack_resources(StackName=stack_name)
        result = current_result["StackResourceSummaries"]

        while "nextToken" in current_result:
            current_result = cf_client.list_projects(StackName=stack_name, nextToken=current_result["nextToken"])
            result.extend(current_result["StackResourceSummaries"])
        return result

    def start_codebuild(self, project: str, environment_variables_overrides: List[Dict[str, str]], branch: str) -> None:
        """
        This functions uses Boto3 to start a batch build.
        It forwards all variables from parameter env_variables as environment variables to the CodeBuild project.
        If a branch is given, it starts the codebuild for the given branch.
        After the build has triggered it waits until the batch build finished
        :raises
            `RuntimeError` if build fails or AWS Batch build returns unknown status
        """
        codebuild_client = self._get_aws_client("codebuild")
        logging.info(f"Trigger codebuild for project {project} with branch {branch} "
                     f"and env_variables ({environment_variables_overrides})")
        ret_val = codebuild_client.start_build_batch(projectName=project,
                                                     sourceVersion=branch,
                                                     environmentVariablesOverride=list(
                                                         environment_variables_overrides))

        def wait_for(seconds: int, interval: int) -> Iterable[int]:
            for _ in range(int(seconds / interval)):
                yield interval

        build_id = ret_val['buildBatch']['id']
        logging.debug(f"Codebuild for project {project} with branch {branch} triggered. Id is {build_id}.")
        interval = 30
        timeout_time_in_seconds = 60 * 60 * 2  # We wait for maximal 2h + (something)
        for seconds_to_wait in wait_for(seconds=timeout_time_in_seconds, interval=interval):
            time.sleep(seconds_to_wait)
            logging.debug(f"Checking status of codebuild id {build_id}.")
            build_response = codebuild_client.batch_get_build_batches(ids=[build_id])
            logging.debug(f"Build response of codebuild id {build_id} is {build_response}")
            if len(build_response['buildBatches']) != 1:
                logging.error(f"Unexpected return value from 'batch_get_build_batches': {build_response}")
            build_status = build_response['buildBatches'][0]['buildBatchStatus']
            logging.info(f"Build status of codebuild id {build_id} is {build_status}")
            if build_status == 'SUCCEEDED':
                break
            elif build_status in ['FAILED', 'FAULT', 'STOPPED', 'TIMED_OUT']:
                raise RuntimeError(f"Build ({build_id}) failed with status: {build_status}")
            elif build_status != "IN_PROGRESS":
                raise RuntimeError(f"Batch build {build_id} has unknown build status: {build_status}")
        # if loop does not break early, build wasn't successful
        else:
            raise RuntimeError(f"Batch build {build_id} ran into timeout.")
