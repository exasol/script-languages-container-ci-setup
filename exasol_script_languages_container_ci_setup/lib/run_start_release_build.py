import logging
import re
from typing import Tuple, Dict

from exasol_script_languages_container_ci_setup.lib.aws_access import AwsAccess
from exasol_script_languages_container_ci_setup.lib.github_release_creator import GithubReleaseCreator
from exasol_script_languages_container_ci_setup.lib.release_build import release_stack_name


def get_environment_variable_override(env_variable: Tuple[str, str]) -> Dict[str, str]:
    return {"name": env_variable[0], "value": env_variable[1], "type": "PLAINTEXT"}


def _parse_upload_url(upload_url: str) -> int:
    """
    upload_url is expected to have the following format: `https://uploads.github.com/repos/exasol/script-languages-repo/releases/123/assets{?name,label}`
    where `exasol/script-languages-repo` is the repository for which the release will be created and 123 is the id of the release.
    This method return release id as integer.
    """
    res = re.search(r"^https://uploads.github.com/repos/([a-zA-Z0-9\-_/]+)/releases/([\d]+)/assets", upload_url)
    if res is None:
        raise ValueError("Parameter upload_url is in unexpected format.")
    return int(res.groups()[1])


def _execute_release_build(aws_access: AwsAccess, project: str, branch: str,
                           release_id: int, is_dry_run: bool, gh_token: str) -> None:
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
    resources = aws_access.get_all_stack_resources(release_stack_name(project))
    matching_project = [resource for resource in resources if resource["ResourceType"] == "AWS::CodeBuild::Project"]
    if len(matching_project) == 0:
        raise ValueError(f"No project deployed for {project}. Found following resources: {resources}")
    if len(matching_project) > 1:
        raise RuntimeError(f"Multiple projects match {project}. Found following matches: {matching_project}")

    if is_dry_run:
        dry_run_value = "--dry-run"
    else:
        dry_run_value = "--no-dry-run"

    if gh_token is None:
        raise RuntimeError("Parameter gh_token must not be None.")

    env_variables = [("RELEASE_ID", f"{release_id}"),
                     ("DRY_RUN", dry_run_value),
                     ("GITHUB_TOKEN", gh_token)]
    environment_variables_overrides = list(map(get_environment_variable_override, env_variables))
    aws_access.start_codebuild(matching_project[0]["PhysicalResourceId"],
                               environment_variables_overrides=environment_variables_overrides,
                               branch=branch)


def run_start_release_build(aws_access: AwsAccess, project: str, upload_url: str, branch: str, gh_token: str) -> None:
    logging.info(f"run_start_release_build for aws profile {aws_access.aws_profile_for_logging} for project {project} "
                 f"with upload url: {upload_url}")
    _execute_release_build(aws_access, project, branch, _parse_upload_url(upload_url=upload_url), False, gh_token)


def run_start_test_release_build(aws_access: AwsAccess, gh_release_creator: GithubReleaseCreator, repo_name: str,
                                 project: str, branch: str, release_title: str, gh_token: str) -> None:
    logging.info(f"run_start_test_release_build for aws profile {aws_access.aws_profile_for_logging} "
                 f"for project {project} for branch: {branch} with title: {release_title}")
    release_id = gh_release_creator.create_release(repo_name, branch, release_title)
    _execute_release_build(aws_access, project, branch, release_id, True, gh_token)
