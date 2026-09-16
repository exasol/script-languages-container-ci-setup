import subprocess

import pytest
from git import Repo

from exasol.slc_ci_setup.lib.deploy_build import (
    BuildType,
    deploy_build,
)


@pytest.fixture()
def change_test_dir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture()
def prepare_github_folder(change_test_dir):
    path = change_test_dir / ".github" / "workflows"
    path.mkdir(parents=True, exist_ok=False)
    return change_test_dir


@pytest.fixture()
def prepare_git_repo(change_test_dir):
    Repo.init()


def test_workflow_files(prepare_github_folder, prepare_git_repo):
    deploy_build(BuildType.CI, False)
    deploy_build(BuildType.CD, False)
    deploy_build(BuildType.NIGHTLY, False)

    # The generated workflows use "$/.github" so zizmor does not treat local
    # reusable workflows as unpinned external dependencies.  actionlint checks
    # the GitHub syntax itself, where the equivalent local path is "./.github".
    for workflow_file in prepare_github_folder.glob(".github/workflows/*.yml"):
        workflow_content = workflow_file.read_text(encoding="utf-8")
        workflow_file.write_text(
            workflow_content.replace("$/.github", "./.github"),
            encoding="utf-8",
        )

    res = subprocess.run(["actionlint"], capture_output=True)
    if res.returncode != 0:
        pytest.fail(res.stdout.decode("utf-8"))
