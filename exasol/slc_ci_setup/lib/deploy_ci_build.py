from pathlib import Path

from exasol.slc_ci_setup.lib.render_template import render_template


def deploy_ci_build():
    target_path = Path() / ".github" / "workflows"
    templates = ["slc_ci.yml"]
    for template in templates:
        github_workflow = render_template(template)
        with open(target_path / template, "w", encoding="utf-8") as f:
            f.write(github_workflow)
