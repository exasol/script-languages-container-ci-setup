from pathlib import Path

from exasol.slc_ci_setup.lib.render_template import render_template


def deploy_ci_build():
    target_path = Path() / ".github" / "workflows"
    templates = [
        "slc_ci.yml.tmpl",
        "slc_ci_self_check.yml.tmpl",
        "slc_ci_build_slc.yml.tmpl",
        "slc_ci_check_for_build.yml.tmpl",
        "slc_ci_flavor.yml.tmpl",
        "slc_ci_prepare_test_container.yml.tmpl",
        "slc_ci_test_slc.yml.tmpl",
    ]
    heading = render_template("heading.tmpl")
    for template in templates:
        github_workflow = render_template(template, heading=heading)
        with open(
            target_path / template.replace(".yml.tmpl", ".yml"), "w", encoding="utf-8"
        ) as f:
            f.write(github_workflow)
