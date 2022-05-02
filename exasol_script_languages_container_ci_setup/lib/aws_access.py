import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from exasol_script_languages_container_ci_setup.lib.deployer import Deployer


def upload_cloudformation_stack(aws_profile: str, yml: str, stack_name: str):
    """
    Deploy the cloudformation stack.
    """
    if aws_profile is not None:
        logging.debug(f"Running upload_cloudformation_stack for aws profile {aws_profile}")
        aws_session = boto3.session.Session(profile_name=aws_profile)
        cloud_client = aws_session.client('cloudformation')
    else:
        logging.debug(f"Running  upload_cloudformation_stack for default aws profile.")
        cloud_client = boto3.client('cloudformation')
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


def read_secret_arn(aws_profile: str, secret_name: str):
    """"
    Uses Boto3 to retrieve the ARN of a secret.
    """
    logging.debug(f"Reading secret for getting ARN, secret name = {secret_name}, for aws profile {aws_profile}")
    session = boto3.session.Session(profile_name=aws_profile)
    client = session.client(service_name='secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response["ARN"]
    except ClientError as e:
        logging.error("Unable to read secret")
        raise e


def read_dockerhub_secret_arn(aws_profile: str):
    return read_secret_arn(aws_profile, "Dockerhub")


def validate_cloudformation_template(cloudformation_yml, aws_profile: Optional[str]):
    """
    This function pushes the YAML to AWS Cloudformation for validation
    (see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-validate-template.html)
    Pitfall: Boto3 expects the YAML string as parameter, whereas the AWS CLI expects the file URL as parameter.
    It requires to have the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables set correctly.
    """
    if aws_profile is not None:
        logging.debug(f"Running validate_cloudformation_template for aws profile {aws_profile}")
        aws_session = boto3.session.Session(profile_name=aws_profile)
        cloud_client = aws_session.client('cloudformation')
        cloud_client.validate_template(TemplateBody=cloudformation_yml)
    else:
        logging.debug(f"Running validate_cloudformation_template for default aws profile.")
        cloud_client = boto3.client('cloudformation')
        cloud_client.validate_template(TemplateBody=cloudformation_yml)