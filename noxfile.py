import nox

# imports all nox task provided by the toolbox
from exasol.toolbox.nox.tasks import *

# default actions to be run if nothing is explicitly specified with the -s option
nox.options.sessions = ["project:fix"]


@nox.session(name="update-integration-test-github-workflows", python=False)
def update_integration_test_github_workflows(session: nox.Session):
    """
    Updates the Github workflows under ".github/workflows" for the dummy SLC in this repository.
    """
    session.run("exaslc-ci-setup", "deploy-ci-build")
    session.run("git", "add", ".github/workflows/slc_ci*.yml")
