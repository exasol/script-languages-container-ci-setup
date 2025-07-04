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
    res = subprocess.run(["actionlint"], capture_output=True)
    if res.returncode != 0:
        pytest.fail(res.stdout.decode("utf-8"))
