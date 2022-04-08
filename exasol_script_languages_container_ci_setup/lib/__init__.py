import logging
import shlex
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import boto3
import jinja2
from botocore.exceptions import ClientError


def upload_cloudformation_stack(aws_profile: str, yml: str, stack_name: str):
    """
    Use the AWS CLI to deploy a stack. (Note we don't use Boto3 here
    because it looks much more complicated than the CLI variant and there is not really good documentation for it.
    """
    logging.info(f"Deploy stack with name='{stack_name}' for aws profile {aws_profile}")
    with TemporaryDirectory() as yml_dir:
        yml_file_path = Path(yml_dir) / "cloudformation.yaml"
        with open(yml_file_path, "w") as yml_file:
            yml_file.write(yml)
        command = f"aws cloudformation deploy --stack-name {stack_name} " \
                  f"--profile {aws_profile} --template-file {yml_file_path} " \
                  f"--capabilities CAPABILITY_IAM"
        logging.info(f"Invoking command: {command}")
        completed_process = subprocess.run(shlex.split(command))
        try:
            completed_process.check_returncode()
        except subprocess.CalledProcessError as e:
            sys.exit(1)


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


def render_template(template: str, **kwargs):
    env = jinja2.Environment(loader=jinja2.PackageLoader("exasol_script_languages_container_ci_setup"),
                             autoescape=jinja2.select_autoescape())
    t = env.get_template(template)
    return t.render(**kwargs)


def validate_cloudformation_template(cloudformation_yml, aws_profile: Optional[str]):
    """
    This function pushes the YAML to AWS Cloudformation for validation
    (see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-validate-template.html)
    Pitfall: Boto3 expects the YAML string as parameter, whereas the AWS CLI expects the file URL as parameter.
    It requires to have the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables set correctly.
    """
    if aws_profile is not None:
        logging.debug(f"validate_cloudformation_template for aws profile {aws_profile}")
        aws_session = boto3.session.Session(profile_name=aws_profile)
        cloud_client = aws_session.client('cloudformation')
        cloud_client.validate_template(TemplateBody=cloudformation_yml)
    else:
        logging.debug(f"validate_cloudformation_template for default aws profile.")
        cloud_client = boto3.client('cloudformation')
        cloud_client.validate_template(TemplateBody=cloudformation_yml)
