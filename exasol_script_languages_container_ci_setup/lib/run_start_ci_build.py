import logging
from typing import Tuple, Dict

from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.ci_build import ci_stack_name


def get_environment_variable_override(env_variable: Tuple[str, str]) -> Dict[str, str]:
    return {"name": env_variable[0], "value": env_variable[1], "type": "PLAINTEXT"}


def run_start_ci_build(aws_access: AwsAccess, project: str, branch: str, gh_token: str) -> None:
    logging.info(f"run_start_ci_build for aws profile {aws_access.aws_profile_for_logging} for project {project} "
                 f"on branch {branch}")
    """
    This function:
    1. Retrieve resources for the release codebuild stack for that given project
    2. Find the resource with type CodeBuild
    3. Creates the environment variables override
    4. Start and wait for batch build
    :raises:
        `RuntimeError` if build goes wrong or if anything on AWS CodeBuild is not as expected
        `ValueError` if project is not found on AWS CodeBuild or if the upload is not in expected format.
    The upload url is only be used to get the release id.
    """
    resources = aws_access.get_all_stack_resources(ci_stack_name(project))
    matching_project = [resource for resource in resources if resource["ResourceType"] == "AWS::CodeBuild::Project"]
    if len(matching_project) == 0:
        raise ValueError(f"No project deployed for {project}. Found following resources: {resources}")
    if len(matching_project) > 1:
        raise RuntimeError(f"Multiple projects match {project}. Found following matches: {matching_project}")

    if gh_token is None:
        raise RuntimeError("Parameter gh_token must not be None.")

    env_variables = [("GITHUB_TOKEN", gh_token)]
    environment_variables_overrides = list(map(get_environment_variable_override, env_variables))
    aws_access.start_codebuild(matching_project[0]["PhysicalResourceId"],
                               environment_variables_overrides=environment_variables_overrides,
                               branch=branch)
