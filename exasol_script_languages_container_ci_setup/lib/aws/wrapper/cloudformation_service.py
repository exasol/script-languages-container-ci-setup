from typing import (
    Any,
    Callable,
    Dict,
    Optional,
)

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import (
    ListStackResourcesResult,
    NextToken,
    ValidationResult,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)


class CloudFormationService:
    def __init__(self, internal_aws_client):
        self._internal_aws_client = internal_aws_client

    @property
    def internal_aws_client(self) -> Any:
        return self._internal_aws_client

    def validate_template(
        self,
        template_body: str,
        from_boto: Callable[
            [dict[str, Any]], ValidationResult
        ] = ValidationResult.from_boto,
    ) -> ValidationResult:
        boto_validation_result = self._internal_aws_client.validate_template(
            TemplateBody=template_body
        )
        validation_result = from_boto(boto_validation_result)
        return validation_result

    def list_stack_resources(
        self,
        stack_name: PhysicalResourceId,
        next_token: Optional[NextToken] = None,
        from_boto: Callable[
            [dict[str, Any]], ListStackResourcesResult
        ] = ListStackResourcesResult.from_boto,
    ) -> ListStackResourcesResult:
        if next_token is not None:
            boto_list_stack_resources_result = (
                self._internal_aws_client.list_stack_resources(
                    StackName=stack_name.aws_physical_resource_id,
                    NextToken=next_token.aws_next_token,
                )
            )
        else:
            boto_list_stack_resources_result = (
                self._internal_aws_client.list_stack_resources(
                    StackName=stack_name.aws_physical_resource_id
                )
            )

        list_stack_resources_result = from_boto(boto_list_stack_resources_result)
        return list_stack_resources_result
