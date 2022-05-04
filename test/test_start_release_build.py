import os
from unittest.mock import MagicMock

from exasol_script_languages_container_ci_setup.lib.run_start_release_build import run_start_release_build

PROJECT_NAME = "slc"
CODEBUILD_PROJECT_DUMMY_NAME = f"{PROJECT_NAME}CodeBuild-hashvalue"
UPLOAD_URL = "http://deploy-release-artifacts-here.com"
BRANCH = "main"
GITHUB_TOKEN = "gh_secret"


def test_run_release_build():
    """
    Test if invocation of run_start_release_build calls AwsAccess with expected arguments.
    """
    aws_access_mock = MagicMock()
    os.environ["GITHUB_TOKEN"] = GITHUB_TOKEN
    aws_access_mock.get_all_codebuild_projects.return_value = [CODEBUILD_PROJECT_DUMMY_NAME]
    run_start_release_build(aws_access=aws_access_mock, project=PROJECT_NAME,
                            upload_url=UPLOAD_URL, branch=BRANCH, dry_run=False)
    expected_env_variable_overrides = [
        {"name": "UPLOAD_URL", "value": UPLOAD_URL, "type": "PLAINTEXT"},
        {"name": "DRY_RUN", "value": "--no-dry-run", "type": "PLAINTEXT"},
        {"name": "GITHUB_TOKEN", "value": GITHUB_TOKEN, "type": "PLAINTEXT"}
    ]

    aws_access_mock. \
        start_codebuild.assert_called_once_with(CODEBUILD_PROJECT_DUMMY_NAME,
                                                environment_variables_overrides=expected_env_variable_overrides,
                                                branch=BRANCH)
