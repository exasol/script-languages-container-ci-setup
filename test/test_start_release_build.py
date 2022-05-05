import datetime
import os
from unittest.mock import MagicMock

from dateutil.tz import tzutc

from exasol_script_languages_container_ci_setup.lib.run_start_release_build import run_start_release_build

UPLOAD_URL = "http://deploy-release-artifacts-here.com"
BRANCH = "main"
GITHUB_TOKEN = "gh_secret"

#Original resources extracted from a ScriptLanguage cloudformation stack
DUMMY_RESOURCES = [
    {'LogicalResourceId': 'ReleaseArtifactsBucket',
     'PhysicalResourceId': 'scriptlanguagesreleasebuil-releaseartifactsbucket-6ikq8b0bojhj',
     'ResourceType': 'AWS::S3::Bucket',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 38, 36, 391000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE',
     'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     },
    {'LogicalResourceId': 'ReleaseBatchBuildRole',
     'PhysicalResourceId': 'ScriptLanguagesReleaseBuild-ReleaseBatchBuildRole-18RVZAPWKW3ZB',
     'ResourceType': 'AWS::IAM::Role',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 38, 35, 103000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE',
     'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     },
    {'LogicalResourceId': 'ReleaseCodeBuildLogGroup',
     'PhysicalResourceId': '/aws/codebuild/ScriptLanguagesReleaseCodeB-FTGeeZLjmjX7',
     'ResourceType': 'AWS::Logs::LogGroup',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 39, 11, 935000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE', 'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     },
    {'LogicalResourceId': 'ReleaseCodeBuildRole',
     'PhysicalResourceId': 'ScriptLanguagesReleaseBuild-ReleaseCodeBuildRole-1WPN324U80IRE',
     'ResourceType': 'AWS::IAM::Role',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 39, 1, 806000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE', 'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     },
    {'LogicalResourceId': 'ScriptLanguagesReleaseCodeBuild',
     'PhysicalResourceId': 'ScriptLanguagesReleaseCodeB-FTGeeZLjmjX7',
     'ResourceType': 'AWS::CodeBuild::Project',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 39, 7, 850000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE', 'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     }
]


def test_run_release_build():
    """
    Test if invocation of run_start_release_build calls AwsAccess with expected arguments.
    """
    aws_access_mock = MagicMock()
    os.environ["GITHUB_TOKEN"] = GITHUB_TOKEN
    aws_access_mock.get_all_stack_resources.return_value = DUMMY_RESOURCES
    run_start_release_build(aws_access=aws_access_mock, project="slc",
                            upload_url=UPLOAD_URL, branch=BRANCH, dry_run=False)
    expected_env_variable_overrides = [
        {"name": "UPLOAD_URL", "value": UPLOAD_URL, "type": "PLAINTEXT"},
        {"name": "DRY_RUN", "value": "--no-dry-run", "type": "PLAINTEXT"},
        {"name": "GITHUB_TOKEN", "value": GITHUB_TOKEN, "type": "PLAINTEXT"}
    ]

    aws_access_mock. \
        start_codebuild.assert_called_once_with("ScriptLanguagesReleaseCodeB-FTGeeZLjmjX7",
                                                environment_variables_overrides=expected_env_variable_overrides,
                                                branch=BRANCH)
