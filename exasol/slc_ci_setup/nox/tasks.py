import nox

from exasol.slc_ci_setup.lib.deploy_build import (
    BuildType,
    deploy_build,
)


@nox.session(name="update-ci-github-workflows", python=False)
def update_ci_github_workflows(session: nox.Session):
    """
    Updates the Github workflows for the SLC CI under ".github/workflows/" in this repository.
    """
    deploy_build(build_type=BuildType.CI)
    session.run("git", "add", ".github/workflows/slc_ci*.yml")


@nox.session(name="update-cd-github-workflows", python=False)
def update_cd_github_workflows(session: nox.Session):
    """
    Updates the Github workflows for the SLC CD in directory ".github/workflows/".
    """
    deploy_build(build_type=BuildType.CD)
    session.run("git", "add", ".github/workflows/slc_cd*.yml")
