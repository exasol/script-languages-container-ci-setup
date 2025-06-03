from typing import (
    Any,
    Callable,
    Dict,
    List,
)

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.codebuild import (
    BuildBatch,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)


class CodeBuildService:
    def __init__(self, internal_aws_client):
        self._internal_aws_client = internal_aws_client

    @property
    def internal_aws_client(self) -> Any:
        return self._internal_aws_client

    def start_build_batch(
        self,
        project_name: PhysicalResourceId,
        source_version: str,
        environment_variables_override: list[dict[str, str]],
        from_boto: Callable[[dict[str, Any]], BuildBatch] = BuildBatch.from_boto,
    ) -> BuildBatch:
        boto_build_batch = self._internal_aws_client.start_build_batch(
            projectName=project_name.aws_physical_resource_id,
            sourceVersion=source_version,
            environmentVariablesOverride=environment_variables_override,
        )
        build_batch = from_boto(boto_build_batch["buildBatch"])
        return build_batch

    def batch_get_build_batches(
        self,
        build_batch_ids: list[PhysicalResourceId],
        from_boto: Callable[[dict[str, Any]], BuildBatch] = BuildBatch.from_boto,
    ) -> list[BuildBatch]:
        aws_ids = [
            build_batch_id.aws_physical_resource_id
            for build_batch_id in build_batch_ids
        ]
        boto_build_batches = self._internal_aws_client.batch_get_build_batches(
            ids=aws_ids
        )
        print(boto_build_batches)
        build_batches = [
            from_boto(boto_build_batch)
            for boto_build_batch in boto_build_batches["buildBatches"]
        ]
        return build_batches
