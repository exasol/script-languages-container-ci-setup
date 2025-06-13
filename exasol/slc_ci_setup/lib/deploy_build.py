import logging
from enum import Enum
from pathlib import Path

from exasol.slc_ci_setup.lib.template_access import (
    list_templates,
    render_template,
)


class BuildType(Enum):
    CI = "slc_ci"
    CD = "slc_cd"
    NIGHTLY = "slc_nightly"


def deploy_build(build_type: BuildType, test_only: bool):
    target_path = Path() / ".github" / "workflows"
    templates = list_templates(build_type.value)

    for template in templates:
        target_file = template.replace(".yml.tmpl", ".yml")
        logging.info("Generating workflow %s", target_file)
        github_workflow = render_template(template, test_only=test_only)
        with open(target_path / target_file, "w", encoding="utf-8") as f:
            f.write(github_workflow)
