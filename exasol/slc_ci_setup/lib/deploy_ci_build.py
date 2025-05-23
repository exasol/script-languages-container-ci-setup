from pathlib import Path

from exasol.slc_ci_setup.lib.template_access import (
    list_templates,
    render_template,
)


def deploy_ci_build():
    target_path = Path() / ".github" / "workflows"
    templates = list_templates("slc_ci")

    for template in templates:
        print(template)
        github_workflow = render_template(template)
        with open(
            target_path / template.replace(".yml.tmpl", ".yml"), "w", encoding="utf-8"
        ) as f:
            f.write(github_workflow)
