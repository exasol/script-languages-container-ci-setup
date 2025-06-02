from typing import (
    Dict,
    List,
    Tuple,
)

import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.codebuild_service import (
    CodeBuildService,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.codebuild import (
    BuildBatch,
    BuildBatchStatus,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)


class StartCodeBuildContract:

    @pytest.fixture(scope="class")
    def codebuild_service(self) -> CodeBuildService:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def project_name(self) -> PhysicalResourceId:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def source_version(self) -> str:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def environment_variables_override(self) -> list[dict[str, str]]:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def build_batch(
        self,
        codebuild_service,
        project_name,
        source_version,
        environment_variables_override,
    ) -> BuildBatch:
        build_batch = codebuild_service.start_build_batch(
            project_name=project_name,
            source_version=source_version,
            environment_variables_override=environment_variables_override,
        )
        return build_batch

    def test_build_batch_status(self, build_batch):
        assert build_batch.build_batch_status in set(BuildBatchStatus)


class BatchGetBuildBatchesWithBatchIdFromStartBuildCode:

    @pytest.fixture(scope="class")
    def codebuild_service(self) -> CodeBuildService:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def project_name(self) -> PhysicalResourceId:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def source_version(self) -> str:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def environment_variables_override(self) -> list[dict[str, str]]:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def build_batches(
        self,
        codebuild_service,
        project_name,
        source_version,
        environment_variables_override,
    ) -> tuple[BuildBatch, BuildBatch]:
        build_batch_from_start = codebuild_service.start_build_batch(
            project_name=project_name,
            source_version=source_version,
            environment_variables_override=environment_variables_override,
        )
        build_batches_from_get = codebuild_service.batch_get_build_batches(
            build_batch_ids=[build_batch_from_start.id]
        )
        return build_batch_from_start, build_batches_from_get[0]

    def test_build_batch_id(self, build_batches):
        assert build_batches[0].id == build_batches[1].id

    def test_build_batch_status_from_start(self, build_batches):
        assert build_batches[0].build_batch_status in set(BuildBatchStatus)

    def test_build_batch_status_from_get(self, build_batches):
        assert build_batches[1].build_batch_status in set(BuildBatchStatus)


class BatchGetBuildBatchesSingleBuildIdContract:

    @pytest.fixture(scope="class")
    def codebuild_service(self) -> CodeBuildService:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def build_batch_id(self, codebuild_service) -> PhysicalResourceId:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def build_batches(self, codebuild_service, build_batch_id) -> list[BuildBatch]:
        build_batches = codebuild_service.batch_get_build_batches(
            build_batch_ids=[build_batch_id]
        )
        return build_batches

    @pytest.fixture
    def expected_build_batch_status(self) -> BuildBatchStatus:
        raise NotImplementedError()

    def test_length(self, build_batches):
        assert len(build_batches) == 1

    def test_same_id(self, build_batch_id, build_batches):
        assert build_batches[0].id == build_batch_id

    def test_build_batch_status(self, build_batches, expected_build_batch_status):
        assert build_batches[0].build_batch_status == expected_build_batch_status


class BatchGetBuildBatchesSingleBuildIdInProgressContract(
    BatchGetBuildBatchesSingleBuildIdContract
):

    def expected_build_batch_status(self) -> BuildBatchStatus:
        return BuildBatchStatus.IN_PROGRESS


class BatchGetBuildBatchesSingleBuildIdSucceededContract(
    BatchGetBuildBatchesSingleBuildIdContract
):

    def expected_build_batch_status(self) -> BuildBatchStatus:
        return BuildBatchStatus.SUCCEEDED


class BatchGetBuildBatchesSingleBuildIdFailedContract(
    BatchGetBuildBatchesSingleBuildIdContract
):

    def expected_build_batch_status(self) -> BuildBatchStatus:
        return BuildBatchStatus.FAILED


class BatchGetBuildBatchesSingleBuildIdStoppedContract(
    BatchGetBuildBatchesSingleBuildIdContract
):

    def expected_build_batch_status(self) -> BuildBatchStatus:
        return BuildBatchStatus.STOPPED
