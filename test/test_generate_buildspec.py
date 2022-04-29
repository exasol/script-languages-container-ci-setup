import json

import jsonschema
import pytest

from exasol_script_languages_container_ci_setup.lib import render_template
from exasol_script_languages_container_ci_setup.lib.run_generate_buildspec import run_generate_buildspec, \
    get_config_file_parameter

expected_result_root_buildspec = """
version: 0.2

# ---- AUTOMATICALLY GENERATED FILE --------
# ---- DO NOT EDIT MANUALLY, BUT USE PYTHON MODULE "script-languages-container-ci-setup" TO UPDATE ---

batch:
  fast-fail: false
  build-graph:
    - identifier: build_test_flavor
      env:
        variables:
          FLAVOR: test-flavor
      buildspec: {location}/build_buildspec.yaml
      privileged-mode: true
      type: BUILD_GENERAL1_MEDIUM
"""


def test_buildspec(tmp_path):
    """
    Run run_generate_buildspec() for one flavor and compare result!
    """
    root_path = tmp_path / "flavors"
    test_flavor = root_path / "test-flavor"
    test_flavor.mkdir(parents=True, exist_ok=False)
    out_path = tmp_path / "out"
    out_path.mkdir(parents=False, exist_ok=False)

    script_languages_ci_location = "http://slc-ci"
    run_generate_buildspec((str(root_path),), str(out_path.absolute()), config_file=None)

    with open(out_path / "buildspec.yaml", "r") as res_file:
        res = res_file.read()

        assert res.strip() == expected_result_root_buildspec.strip().format(location=str(out_path))

    with open(out_path / "build_buildspec.yaml", "r") as res_file:
        res = res_file.read()

        # For build_buildspec.yaml we re-use the template for testing
        expected_result_build_buildspec = render_template("build_buildspec.yaml",
                                                          script_languages_ci_location=script_languages_ci_location,
                                                          config_file_parameter="")
        assert res.strip() == expected_result_build_buildspec.strip(). \
            format(script_languages_ci_location=script_languages_ci_location)


def test_buildspec_with_valid_config_file(tmp_path):
    """
    Run run_generate_buildspec() for one flavor with a valid config file and compare result!
    """
    root_path = tmp_path / "flavors"
    test_flavor = root_path / "test-flavor"
    test_flavor.mkdir(parents=True, exist_ok=False)
    out_path = tmp_path / "out"
    out_path.mkdir(parents=False, exist_ok=False)

    a_folder = tmp_path / "a_folder"
    a_folder.mkdir(parents=False, exist_ok=False)

    config_file_path = tmp_path / "build_config.json"
    config = {"build_ignore": {"ignored_paths": [str(a_folder)]}}
    with open(config_file_path, "w") as f:
        json.dump(config, f)

    run_generate_buildspec((str(root_path),), str(out_path.absolute()),
                           config_file=str(config_file_path.absolute()))

    with open(out_path / "buildspec.yaml", "r") as res_file:
        res = res_file.read()

        assert res.strip() == expected_result_root_buildspec.strip().format(location=str(out_path))

    with open(out_path / "build_buildspec.yaml", "r") as res_file:
        res = res_file.read()

        # For build_buildspec.yaml we re-use the template for testing
        expected_result_build_buildspec = render_template("build_buildspec.yaml",
                                                          config_file_parameter=
                                                          get_config_file_parameter(config_file_path))
        assert res.strip() == expected_result_build_buildspec.strip()


def test_buildspec_with_invalid_config_file(tmp_path):
    """
    Run run_generate_buildspec() for one flavor with an invalid config file and check for correct exception!
    """
    root_path = tmp_path / "flavors"
    test_flavor = root_path / "test-flavor"
    test_flavor.mkdir(parents=True, exist_ok=False)
    out_path = tmp_path / "out"
    out_path.mkdir(parents=False, exist_ok=False)

    config_file_path = tmp_path / "build_config.json"
    # Incorrect config ('ignored_path' instead of 'ignored_paths')
    config = {"build_ignore": {"ignored_path": ["a_folder"]}}
    with open(config_file_path, "w") as f:
        json.dump(config, f)

    with pytest.raises(jsonschema.exceptions.ValidationError):
        run_generate_buildspec((str(root_path),), str(out_path.absolute()),
                               config_file=str(config_file_path.absolute()))


def test_buildspec_with_invalid_folder(tmp_path):
    """
    Run run_generate_buildspec() for one flavor with a valid config file, but invalid content and check for correct exception!
    """
    root_path = tmp_path / "flavors"
    test_flavor = root_path / "test-flavor"
    test_flavor.mkdir(parents=True, exist_ok=False)
    out_path = tmp_path / "out"
    out_path.mkdir(parents=False, exist_ok=False)

    config_file_path = tmp_path / "build_config.json"

    a_folder = tmp_path / "a_folder"
    # Incorrect config (tmp_path/a_folder does not exists)
    config = {"build_ignore": {"ignored_paths": [str(a_folder)]}}
    with open(config_file_path, "w") as f:
        json.dump(config, f)

    with pytest.raises(ValueError):
        run_generate_buildspec((str(root_path),), str(out_path.absolute()),
                               config_file=str(config_file_path.absolute()))

