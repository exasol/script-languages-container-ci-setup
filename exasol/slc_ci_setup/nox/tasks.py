import nox

from exasol.slc_ci_setup.lib.deploy_ci_build import deploy_ci_build


@nox.session(name="update-github-workflows", python=False)
def update_github_workflows(session: nox.Session):
    """
    Updates the Github workflows for the SLC CI under ".github/workflows/" in this repository.
    """
    deploy_ci_build()
    session.run("git", "add", ".github/workflows/slc_ci*.yml")
