import logging
import os
from typing import Tuple, Dict

from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.release_build import release_stack_name


def get_environment_variable_override(env_variable: Tuple[str, str]) -> Dict[str, str]:
    return {"name": env_variable[0], "value": env_variable[1], "type": "PLAINTEXT"}


def run_start_release_build(aws_access: AwsAccess, project: str, upload_url: str, branch: str, dry_run: bool) -> None:
    """
    This command executes
    1. Retrieve resources for the release codebuild stack for that given project
    2. Find the resource with type CodeBuild
    3. Creates the environment variables override
    4. Start and wait for batch build
    :raises:
        `RuntimeError` if build goes wrong or if anything on AWS CodeBuild is not as expected
        `ValueError` if project is not found on AWS CodeBuild.
    """
    logging.info(f"run_start_release_build for aws profile {aws_access.aws_profile} for project {project} "
                 f"with upload url: {upload_url}")
    resources = aws_access.get_all_stack_resources(release_stack_name(project))
    matching_project = [resource for resource in resources if resource["ResourceType"] == "AWS::CodeBuild::Project"]
    if len(matching_project) == 0:
        raise ValueError(f"No project deployed for {project}. Found following resources: {resources}")
    if len(matching_project) > 1:
        raise RuntimeError(f"Multiple projects match {project}. Found following matches: {matching_project}")
    if dry_run:
        dry_run_value = "--dry-run"
    else:
        dry_run_value = "--no-dry-run"

    gh_token = os.getenv("GITHUB_TOKEN")
    if gh_token is None:
        raise RuntimeError("Environment variable GITHUB_TOKEN needs to be declared.")
    env_variables = [("UPLOAD_URL", upload_url),
                     ("DRY_RUN", dry_run_value),
                     ("GITHUB_TOKEN", gh_token)]
    environment_variables_overrides = list(map(get_environment_variable_override, env_variables))
    aws_access.start_codebuild(matching_project[0]["PhysicalResourceId"],
                               environment_variables_overrides=environment_variables_overrides,
                               branch=branch)
