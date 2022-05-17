import datetime
from unittest.mock import MagicMock

from dateutil.tz import tzutc

from exasol_script_languages_container_ci_setup.lib.run_start_build import run_start_ci_build

REPO_NAME = "script-languages-repo"
BRANCH = "feature-branch"

#Original resources extracted from a ScriptLanguage cloudformation stack
DUMMY_RESOURCES = [
    {'LogicalResourceId': 'ArtifactsBucket',
     'PhysicalResourceId': 'scriptlanguagesreleasebuil-artifactsbucket-6ikq8b0bojhj',
     'ResourceType': 'AWS::S3::Bucket',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 38, 36, 391000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE',
     'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     },
    {'LogicalResourceId': 'BatchBuildRole',
     'PhysicalResourceId': 'ScriptLanguagesReleaseBuild-BatchBuildRole-18RVZAPWKW3ZB',
     'ResourceType': 'AWS::IAM::Role',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 38, 35, 103000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE',
     'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     },
    {'LogicalResourceId': 'BuildLogGroup',
     'PhysicalResourceId': '/aws/codebuild/ScriptLanguagesCodeB-FTGeeZLjmjX7',
     'ResourceType': 'AWS::Logs::LogGroup',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 39, 11, 935000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE', 'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     },
    {'LogicalResourceId': 'CodeBuildRole',
     'PhysicalResourceId': 'ScriptLanguagesBuild-CodeBuildRole-1WPN324U80IRE',
     'ResourceType': 'AWS::IAM::Role',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 39, 1, 806000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE', 'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     },
    {'LogicalResourceId': 'ScriptLanguagesCodeBuild',
     'PhysicalResourceId': 'ScriptLanguagesCodeB-FTGeeZLjmjX7',
     'ResourceType': 'AWS::CodeBuild::Project',
     'LastUpdatedTimestamp': datetime.datetime(2022, 5, 4, 18, 39, 7, 850000, tzinfo=tzutc()),
     'ResourceStatus': 'CREATE_COMPLETE', 'DriftInformation': {'StackResourceDriftStatus': 'NOT_CHECKED'}
     }
]


def test_run_ci_build():
    """
    Test if invocation of run_start_ci_build calls AwsAccess with expected arguments.
    """
    aws_access_mock = MagicMock()
    aws_access_mock.get_all_stack_resources.return_value = DUMMY_RESOURCES
    run_start_ci_build(aws_access=aws_access_mock, project="slc", branch=BRANCH)
    expected_env_variable_overrides = list()

    aws_access_mock. \
        start_codebuild.assert_called_once_with("ScriptLanguagesCodeB-FTGeeZLjmjX7",
                                                environment_variables_overrides=expected_env_variable_overrides,
                                                branch=BRANCH)
