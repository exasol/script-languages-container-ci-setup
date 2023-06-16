import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.cloudformation_service import CloudFormationService
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import ValidationResult, \
    ListStackResourcesResult
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId


class ValidateContractContract:

    @pytest.fixture(scope="class")
    def cloudformation_service(self) -> CloudFormationService:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def template_body(self) -> str:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def validation_result(self, cloudformation_service, template_body) -> ValidationResult:
        validation_result = cloudformation_service.validate_template(template_body=template_body)
        return validation_result

    def test_validation_result_is_not_none(self, validation_result):
        assert validation_result is not None


class ListStackResourcesContractContract:

    @pytest.fixture(scope="class")
    def cloudformation_service(self) -> CloudFormationService:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def stack_name(self) -> PhysicalResourceId:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def resource_type(self) -> str:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def number_of_resources(self) -> int:
        raise NotImplementedError()

    @pytest.fixture(scope="class")
    def list_stack_resources_result(self, cloudformation_service, stack_name) -> ListStackResourcesResult:
        list_stack_resources_result = cloudformation_service.list_stack_resources(
            stack_name=stack_name,
            next_token=None
        )
        return list_stack_resources_result

    def test_stack_resource_summaries_count(self, list_stack_resources_result, number_of_resources):
        assert len(list_stack_resources_result.stack_resource_summaries) == number_of_resources

    def test_physical_resource_ids_is_not_none(self, list_stack_resources_result):
        resources_with_physical_resource_id = [stack_resource_summary
                                               for stack_resource_summary
                                               in list_stack_resources_result.stack_resource_summaries
                                               if stack_resource_summary.physical_resource_id is not None]
        assert len(resources_with_physical_resource_id) > 0

    def test_resource_type(self, list_stack_resources_result, resource_type):
        resources_with_given_resource_type = [stack_resource_summary.physical_resource_id
                                              for stack_resource_summary
                                              in list_stack_resources_result.stack_resource_summaries
                                              if stack_resource_summary.resource_type == resource_type]
        assert len(resources_with_given_resource_type) > 0
