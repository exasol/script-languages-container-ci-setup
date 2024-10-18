import logging

from exasol_script_languages_container_ci_setup.lib.aws.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.render_template import (
    render_template,
)

CODE_BUILD_STACK_NAME = "ReleaseBuild"
RELEASE_CODEBUILD_TEMPLATE = "slc_code_release_build.yaml"


def release_stack_name(project: str):
    return f"{project}{CODE_BUILD_STACK_NAME}"


def run_deploy_release_build(aws_access: AwsAccess, project: str, github_url: str):
    """
    This command deploys the ci build cloudformation stack
    1. It get's the dockerhub secret ARN from AWS via Boto3
    2. Then it renders the template and uploads the resulting cloudformation YAML file.
    """
    logging.info(
        f"run_deploy_release_build for aws profile "
        f"{aws_access.aws_profile} for project {project} at {github_url}"
    )
    dockerhub_secret_arn = aws_access.read_dockerhub_secret_arn()
    yml = render_template(
        RELEASE_CODEBUILD_TEMPLATE,
        project=project,
        dockerhub_secret_arn=dockerhub_secret_arn,
        github_url=github_url,
    )
    aws_access.upload_cloudformation_stack(yml, release_stack_name(project))


def run_validate_release_build(aws_access: AwsAccess, project: str, github_url: str):
    """
    This command validates the release build cloudformation stack
    """
    logging.info(
        f"run_validate_release_build for aws profile {aws_access.aws_profile} "
        f"for project {project} at {github_url}"
    )
    dockerhub_secret_arn = "dummy_arn"
    yml = render_template(
        RELEASE_CODEBUILD_TEMPLATE,
        project=project,
        dockerhub_secret_arn=dockerhub_secret_arn,
        github_url=github_url,
    )
    aws_access.validate_cloudformation_template(yml)
