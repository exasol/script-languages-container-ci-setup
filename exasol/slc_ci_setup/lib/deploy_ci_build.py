import logging
from pathlib import Path

from exasol.slc_ci_setup.lib.template_access import (
    list_templates,
    render_template,
)


def deploy_ci_build():
    target_path = Path() / ".github" / "workflows"
    templates = list_templates("slc_ci")

    for template in templates:
        target_file = template.replace(".yml.tmpl", ".yml")
        logging.info("Generating workflow %s", target_file)
        github_workflow = render_template(template)
        with open(target_path / target_file, "w", encoding="utf-8") as f:
            f.write(github_workflow)
