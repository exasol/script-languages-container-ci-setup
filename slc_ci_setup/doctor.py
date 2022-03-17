"""
The doctor module provides functionality to check the health of the `slc-ci-setup`
package and also provide help to find potential fixes.
"""
import shlex
import subprocess
import sys
from enum import Enum
from typing import Iterator

import exasol_error_reporting_python.error_message_builder
from exasol_error_reporting_python.exa_error import ExaError


SUPPORTED_PLATFORMS = ["linux", "darwin"]


def check_shell_cmd(cmd: str) -> bool:
    """
    Runs a shell command and returns True if exit code was 0, False otherwise 
    :param cmd: shell command to execute
    :return: returns True if exit code was 0, False otherwise
    """
    ret_val = True
    completed_process = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        completed_process.check_returncode()
    except subprocess.CalledProcessError as e:
        ret_val = False
    return ret_val


class ErrorCodes(Enum):
    """The equivalent of ICD-10 codes this doctor is using"""

    Unknown = ExaError.message_builder('E-SLCCS-01').message("Unknown issue")
    TargetPlatformNotSupported = ExaError.message_builder('E-SLCCS-02')\
        .message("The platform you are running on is not supported.")\
        .mitigation("Make sure you are using one of the following platforms: {SUPPORTED_PLATFORMS}.")
    AWSNotInstalled = ExaError.message_builder('E-SLCCS-03').message("AWS CLI not installed.")\
        .mitigation("Install AWS CLI. Goto https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html")
    AWSProfileInvalid = ExaError.message_builder('E-SLCCS-04').message("AWS Profile invalid.")\
        .mitigation("Run 'aws configure --profile $your_profile' or 'aws configure' to configure the default profile.")
    AWSAccessKeyInvalid = ExaError.message_builder('E-SLCCS-05').message("AWS Access Key invalid.")\
        .mitigation("Go to the AWS console and create an access key for your user. Then register the access key with 'aws configure --profile $your_profile' or 'aws configure' for the default profile.")


def is_supported_platform(**kwargs) -> bool:
    """
    Checks weather or not the current platform is supported.
    """
    return sys.platform in SUPPORTED_PLATFORMS


def aws_cli_available(**kwargs) -> bool:
    """Checks weather AWS cli is installed"""
    command = "aws --help"
    return check_shell_cmd(command)


def aws_profile_valid(aws_profile: str) -> bool:
    """Checks weather AWS cli is installed"""
    command = f"aws --profile {aws_profile} configure list"
    return check_shell_cmd(command)


def aws_access_key_valid(aws_profile: str) -> bool:
    """Checks weather AWS cli is installed"""
    command = f"aws --profile {aws_profile} iam list-access-keys"
    return check_shell_cmd(command)


def health_checkup(**kwargs) -> Iterator[ErrorCodes]:
    """
    Runs all known examinations

    return an iterator of error codes specifying which problems have been identified.
    """
    examinations = [
        (is_supported_platform, lambda: [ErrorCodes.TargetPlatformNotSupported]),
        (aws_cli_available, lambda: [ErrorCodes.AWSNotInstalled]),
        (aws_profile_valid, lambda: [ErrorCodes.AWSProfileInvalid]),
        (aws_access_key_valid, lambda: [ErrorCodes.AWSAccessKeyInvalid])
    ]
    for is_fine, diagnosis in examinations:
        if not is_fine(**kwargs):
            for error_code in diagnosis():
                yield error_code
