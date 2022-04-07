from unittest.mock import patch, MagicMock

from exasol_script_languages_container_ci_setup.lib import render_template
from exasol_script_languages_container_ci_setup.lib.run_generate_buildspec import run_generate_buildspec

expected_result_root_buildspec = """
version: 0.2

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
    with patch("exasol_script_languages_container_ci_setup.lib.run_generate_buildspec.get_pip_location_for_pkg",
               MagicMock(return_value=script_languages_ci_location)):
        run_generate_buildspec((str(root_path),), str(out_path.absolute()))

    with open(out_path / "buildspec.yaml", "r") as res_file:
        res = res_file.read()

        assert res.strip() == expected_result_root_buildspec.strip().format(location=str(out_path))

    with open(out_path / "build_buildspec.yaml", "r") as res_file:
        res = res_file.read()

        #For build_buildspec.yaml we re-use the template for testing
        expected_result_build_buildspec = render_template("build_buildspec.yaml",
                                                          script_languages_ci_location=script_languages_ci_location)
        assert res.strip() == expected_result_build_buildspec.strip(). \
            format(script_languages_ci_location=script_languages_ci_location)
