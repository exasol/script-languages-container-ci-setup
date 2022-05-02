import logging

import exasol_script_languages_container_ci_setup
from exasol_script_languages_container_ci_setup.lib.aws_access import validate_cloudformation_template
from exasol_script_languages_container_ci_setup.lib.render_template import render_template

CODE_BUILD_STACK_NAME = "CIBuild"


def stack_name(project: str):
    return f"{project}{CODE_BUILD_STACK_NAME}"


def run_deploy_ci_build(aws_profile: str, project: str, github_url: str):
    """
    This command deploys the ci build cloudformation stack
    1. It get's the dockerhub secret ARN from AWS via Boto3
    2. Then it renders the template and uploads the resulting cloudformation YAML file.
    """
    logging.info(f"run_deploy_ci_build for aws profile {aws_profile} for project {project} at {github_url}")
    dockerhub_secret_arn = exasol_script_languages_container_ci_setup.lib.aws_access.read_dockerhub_secret_arn(aws_profile)
    yml = render_template("slc_code_build.yaml", project=project,
                          dockerhub_secret_arn=dockerhub_secret_arn, github_url=github_url)
    exasol_script_languages_container_ci_setup.lib.aws_access.upload_cloudformation_stack(aws_profile, yml,
                                                                               stack_name(project))


def run_validate_ci_build(aws_profile: str, project: str, github_url: str):
    """
    This command validates the ci build cloudformation stack
    """
    logging.info(f"run_validate_ci_build for aws profile {aws_profile} for project {project} at {github_url}")
    dockerhub_secret_arn = "dummy_arn"
    yml = render_template("slc_code_build.yaml", project=project,
                          dockerhub_secret_arn=dockerhub_secret_arn, github_url=github_url)
    validate_cloudformation_template(yml, aws_profile)
