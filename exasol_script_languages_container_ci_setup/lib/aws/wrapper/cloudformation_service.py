from typing import Any, Dict, Optional, Callable

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import ValidationResult, \
    ListStackResourcesResult, NextToken
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId


class CloudFormationService:
    def __init__(self, boto_client):
        self._boto_client = boto_client

    @property
    def boto_client(self) -> Any:
        return self._boto_client

    def validate_template(self,
                          template_body: str,
                          from_boto: Callable[[Dict[str, Any]], ValidationResult] =
                          ValidationResult.from_boto) \
            -> ValidationResult:
        boto_validation_result = self._boto_client.validate_template(TemplateBody=template_body)
        validation_result = from_boto(boto_validation_result)
        return validation_result

    def list_stack_resources(self,
                             stack_name: PhysicalResourceId,
                             next_token: Optional[NextToken],
                             from_boto: Callable[[Dict[str, Any]], ListStackResourcesResult] =
                             ListStackResourcesResult.from_boto) \
            -> ListStackResourcesResult:
        aws_next_token = None if next_token is None else next_token.aws_next_token
        boto_list_stack_resources_result = self._boto_client.list_stack_resources(
            StackName=stack_name.aws_physical_resource_id, NextToken=aws_next_token)
        list_stack_resources_result = from_boto(boto_list_stack_resources_result)
        return list_stack_resources_result
