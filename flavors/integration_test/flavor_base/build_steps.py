from typing import Dict

from exasol.slc.internal.tasks.build.docker_flavor_image_task import (
    DockerFlavorAnalyzeImageTask,
)


class AnalyzeBaseTestBuildRun(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "base_test_build_run"

    def requires_tasks(self):
        return {}

    def get_additional_build_directories_mapping(self) -> dict[str, str]:
        return {}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeFlavorTestBuildRun(DockerFlavorAnalyzeImageTask):

    def get_build_step(self) -> str:
        return "flavor_test_build_run"

    def requires_tasks(self):
        return {"base_test_build_run": AnalyzeBaseTestBuildRun}

    def get_path_in_flavor(self):
        return "flavor_base"


class AnalyzeRelease(DockerFlavorAnalyzeImageTask):
    def get_build_step(self) -> str:
        return "release"

    def requires_tasks(self):
        return {}

    def get_path_in_flavor(self):
        return "flavor_base"


class SecurityScan(DockerFlavorAnalyzeImageTask):
    def get_build_step(self) -> str:
        return "security_scan"

    def requires_tasks(self):
        return {"release": AnalyzeRelease}

    def get_path_in_flavor(self):
        return "flavor_base"
