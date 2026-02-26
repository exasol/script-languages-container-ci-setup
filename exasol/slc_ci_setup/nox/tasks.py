import os
import platform
from argparse import ArgumentParser

import nox

from exasol.slc_ci_setup.lib.deploy_build import (
    BuildType,
    deploy_build,
)


def _is_test_only(session: nox.Session) -> bool:
    parser = ArgumentParser(usage=f"nox -s {session.name} -- [--test-only]")
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Docker Repository name",
    )
    args = parser.parse_args(session.posargs)
    return args.test_only


@nox.session(name="update-ci-github-workflows", python=False)
def update_ci_github_workflows(session: nox.Session):
    """
    Updates the GitHub workflows for the SLC CI under ".github/workflows/" in this repository.
    """
    deploy_build(build_type=BuildType.CI, test_only=_is_test_only(session))
    session.run("git", "add", ".github/workflows/slc_ci*.yml")


@nox.session(name="update-cd-github-workflows", python=False)
def update_cd_github_workflows(session: nox.Session):
    """
    Updates the GitHub workflows for the SLC CD in directory ".github/workflows/".
    """
    deploy_build(build_type=BuildType.CD, test_only=_is_test_only(session))
    session.run("git", "add", ".github/workflows/slc_cd*.yml")


@nox.session(name="update-nightly-github-workflows", python=False)
def update_nightly_github_workflows(session: nox.Session):
    """
    Updates the GitHub workflows for the SLC Nightly builds in directory ".github/workflows/".
    """
    deploy_build(build_type=BuildType.NIGHTLY, test_only=_is_test_only(session))
    session.run("git", "add", ".github/workflows/slc_nightly*.yml")


@nox.session(name="set-github-output-platform", python=False)
def set_github_output_platform(session: nox.Session):
    """
    Detect the platform of the current runner and set the same to GitHub.
    """
    system = platform.system().lower()
    if system == "darwin":
        platform_name = "macos"
    else:
        platform_name = system

    session.log(f"Detected platform: {platform_name}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"platform={platform_name}\n")
    else:
        # Fallback for local testing or old GitHub
        print(f"::set-output name=platform::{platform_name}")
