"""Implements the health checks for this project"""

import sys
from inspect import cleandoc

from exasol_script_languages_container_ci_setup.cli.cli import cli
from exasol_script_languages_container_ci_setup.cli.common import add_options
from exasol_script_languages_container_ci_setup.cli.options.aws_options import (
    aws_options,
)
from exasol_script_languages_container_ci_setup.health_check import health_checkup


@cli.command()
@add_options(aws_options)
def health(aws_profile: str):
    """
    Check the health of the execution environment.

    If no issues have been found, using the library or executing
    the test should work just fine.
    For all found issues there will be a proposed fix/solution.

    If the environment was found to be healthy the exit code will be 0.
    """
    success, failure = 0, -1

    problems = set(health_checkup(aws_profile=aws_profile))
    if not problems:
        sys.exit(success)

    message = cleandoc(
        """
        {count} problem(s) have been identified.
        
        {problems}
        """
    ).format(
        count=len(problems),
        problems="\n".join(str(p) for p in problems),
    )
    print(message)
    sys.exit(failure)
