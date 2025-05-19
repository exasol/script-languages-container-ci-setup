import nox


@nox.session(name="update-github-workflows", python=False)
def update_github_workflows(session: nox.Session):
    """
    Updates the Github workflows for the SLC CI under ".github/workflows/" in this repository.
    """
    session.run("exaslc-ci-setup", "deploy-ci-build")
    session.run("git", "add", ".github/workflows/slc_ci*.yml")
