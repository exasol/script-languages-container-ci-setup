import logging

from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.render_template import render_template

CODE_BUILD_STACK_NAME = "CIBuild"
CI_CODE_BUILD_TEMPLATE = "slc_code_build.yaml"

CI_BUILD_WEBHOOK_FILTER_PATTERN = \
    r"^refs/heads/(((main|master|develop)$)|" \
    r"((rebuild|feature|bug|enhancement|refactoring|ci|security|doc|documentation)/.*))"


def ci_stack_name(project: str):
    return f"{project}{CODE_BUILD_STACK_NAME}"


def run_deploy_ci_build(aws_access: AwsAccess, project: str, github_url: str):
    """
    This command deploys the ci build cloudformation stack
    1. It get's the dockerhub secret ARN from AWS via Boto3
    2. Then it renders the template and uploads the resulting cloudformation YAML file.
    """
    logging.info(f"run_deploy_ci_build for aws profile {aws_access.aws_profile} for project {project} at {github_url}")
    dockerhub_secret_arn = aws_access.read_dockerhub_secret_arn()
    yml = render_template(CI_CODE_BUILD_TEMPLATE, project=project,
                          dockerhub_secret_arn=dockerhub_secret_arn, github_url=github_url,
                          webhook_filter_pattern=CI_BUILD_WEBHOOK_FILTER_PATTERN)
    aws_access.upload_cloudformation_stack(yml, ci_stack_name(project))


def run_validate_ci_build(aws_access: AwsAccess, project: str, github_url: str):
    """
    This command validates the ci build cloudformation stack
    """
    logging.info(f"run_validate_ci_build for aws profile {aws_access.aws_profile} "
                 f"for project {project} at {github_url}")
    dockerhub_secret_arn = "dummy_arn"
    yml = render_template(CI_CODE_BUILD_TEMPLATE, project=project,
                          dockerhub_secret_arn=dockerhub_secret_arn, github_url=github_url,
                          webhook_filter_pattern=CI_BUILD_WEBHOOK_FILTER_PATTERN)
    aws_access.validate_cloudformation_template(yml)
