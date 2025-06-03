"""
The health check module provides functionality to check the health of the `slc-ci-setup`
package and also provide help to find potential fixes.
"""

import shlex
import subprocess
import sys
from collections.abc import Iterator
from typing import (
    Optional,
)

from exasol import error

SUPPORTED_PLATFORMS = ["linux", "darwin"]


def check_shell_cmd(cmd: str) -> bool:
    """
    Runs a shell command and returns True if exit code was 0, False otherwise
    :param cmd: shell command to execute
    :return: returns True if exit code was 0, False otherwise
    """
    result = subprocess.run(shlex.split(cmd), capture_output=True)
    return result.returncode == 0


def is_supported_platform(**kwargs) -> Optional[error.ExaError]:
    """
    Checks weather or not the current platform is supported.
    """
    if sys.platform not in SUPPORTED_PLATFORMS:
        return error.ExaError(
            code="E-SLCCS-02",
            message="The platform you are running on is not supported.",
            mitigations=[
                "Make sure you are using one of the following platforms: {{supported_platforms}}."
            ],
            parameters={"supported_platforms": str(SUPPORTED_PLATFORMS)},
        )


def aws_cli_available(**kwargs) -> Optional[error.ExaError]:
    """Checks weather AWS cli is installed"""
    command = "aws --help"
    if not check_shell_cmd(command):
        return error.ExaError(
            code="E-SLCCS-03",
            message="AWS CLI not installed.",
            mitigations=[
                "Install AWS CLI. Goto https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
            ],
            parameters={},
        )


def aws_profile_valid(aws_profile: str) -> Optional[error.ExaError]:
    """Checks weather the given AWS profile is configured properly."""
    command = f"aws --profile {aws_profile} configure list"
    if not check_shell_cmd(command):
        return error.ExaError(
            code="E-SLCCS-04",
            message="AWS Profile invalid.",
            mitigations=[
                "Run 'aws configure --profile $your_profile' or "
                "'aws configure' to configure the default profile."
            ],
            parameters={},
        )


def aws_access_key_valid(aws_profile: str) -> Optional[error.ExaError]:
    """Checks weather AWS access key is configured for the given AWS profile."""
    command = f"aws --profile {aws_profile} iam list-access-keys"
    if not check_shell_cmd(command):
        return error.ExaError(
            code="E-SLCCS-05",
            message="AWS Access Key invalid.",
            mitigations=[
                "Go to the AWS console and create an access key for your user. "
                "Then register the access key with 'aws configure --profile $your_profile' or "
                "'aws configure' for the default profile."
            ],
            parameters={},
        )


def health_checkup(**kwargs) -> Iterator[error.ExaError]:
    """
    Runs all known examinations

    return an iterator of error codes specifying which problems have been identified.
    """
    examinations = [
        is_supported_platform,
        aws_cli_available,
        aws_profile_valid,
        aws_access_key_valid,
    ]
    for examination in examinations:
        res = examination(**kwargs)
        if res is not None:
            yield res
