from test.unit.github.cli.cli_runner import CliRunner
from unittest.mock import (
    MagicMock,
    call,
)

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci_setup.lib.deploy_build as lib_deploy_build
from exasol.slc_ci_setup.cli.commands.deploy_cd_build import (
    deploy_cd_build,
)


@pytest.fixture
def cli():
    return CliRunner(deploy_cd_build)


@pytest.fixture
def mock_deploy_cd_build(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(
        lib_deploy_build,
        "deploy_build",
        mock_function_to_mock,
    )
    return mock_function_to_mock


def test_mock_deploy_ci_build(cli, mock_deploy_cd_build):
    cli.run()
    assert cli.succeeded

    # Validate the exact call using mock_calls and IsInstance matcher
    expected_call = call(
        build_type=lib_deploy_build.BuildType.CD,
    )
    assert mock_deploy_cd_build.mock_calls == [expected_call]
