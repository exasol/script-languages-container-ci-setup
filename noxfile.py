from pathlib import Path

import nox

# imports all nox task provided by the toolbox
from exasol.toolbox.nox.tasks import *

from exasol.slc_ci_setup.nox.tasks import *

# default actions to be run if nothing is explicitly specified with the -s option
nox.options.sessions = ["project:fix"]


@nox.session(name="update-integration-test-github-workflows", python=False)
def update_integration_test_github_workflows(session: nox.Session):
    """
    Updates the Github workflows under ".github/workflows" for the dummy SLC in this repository.
    """
    update_ci_github_workflows(session)
    update_cd_github_workflows(session)
    _check_workflows(session, "slc_ci*.yml")
    _check_workflows(session, "slc_cd*.yml")


def _check_workflows(session, pattern: str):
    session.log(f"Checking github workflows for {pattern}")
    slc_ci_yml_files = Path(".github/workflows").glob(pattern)
    for slc_ci_yml_file in slc_ci_yml_files:
        session.log(f"Checking {slc_ci_yml_file}")
        session.run("actionlint", str(slc_ci_yml_file))
