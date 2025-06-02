import dataclasses
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)

RESOURCE_TYPE = "ResourceType"

PHYSICAL_RESOURCE_ID = "PhysicalResourceId"

STACK_RESOURCE_SUMMARIES = "StackResourceSummaries"

NEXT_TOKEN = "NextToken"


@dataclasses.dataclass(frozen=True)
class NextToken:
    aws_next_token: Any


@dataclasses.dataclass(frozen=True)
class StackResourceSummary:
    physical_resource_id: Optional[PhysicalResourceId]
    resource_type: str

    @classmethod
    def from_boto(
        cls, boto_stack_resource_summary: dict[str, Any]
    ) -> "StackResourceSummary":
        physical_resource_id = cls._extract_physcial_resource_id(
            boto_stack_resource_summary
        )
        resource_type = boto_stack_resource_summary[RESOURCE_TYPE]
        stack_resource_summary = StackResourceSummary(
            physical_resource_id=physical_resource_id, resource_type=resource_type
        )
        return stack_resource_summary

    @classmethod
    def _extract_physcial_resource_id(
        cls, boto_stack_resource_summary: dict[str, Any]
    ) -> PhysicalResourceId:
        physical_resource_id = None
        if cls._has_physical_resource_id(boto_stack_resource_summary):
            physical_resource_id = PhysicalResourceId(
                aws_physical_resource_id=boto_stack_resource_summary[
                    PHYSICAL_RESOURCE_ID
                ]
            )
        return physical_resource_id

    @classmethod
    def _has_physical_resource_id(cls, boto_stack_resource_summary: dict[str, Any]):
        return (
            PHYSICAL_RESOURCE_ID in boto_stack_resource_summary
            and boto_stack_resource_summary[PHYSICAL_RESOURCE_ID] is not None
        )


@dataclasses.dataclass(frozen=True)
class ListStackResourcesResult:
    next_token: Optional[NextToken]
    stack_resource_summaries: list[StackResourceSummary]

    @classmethod
    def from_boto(
        cls, boto_list_stack_resources_result: dict[str, Any]
    ) -> "ListStackResourcesResult":
        next_token = None
        if cls._has_next_token(boto_list_stack_resources_result):
            next_token = NextToken(boto_list_stack_resources_result[NEXT_TOKEN])
        stack_resource_summaries = [
            StackResourceSummary.from_boto(boto_stack_resource_summary)
            for boto_stack_resource_summary in boto_list_stack_resources_result[
                STACK_RESOURCE_SUMMARIES
            ]
        ]
        return ListStackResourcesResult(
            next_token=next_token, stack_resource_summaries=stack_resource_summaries
        )

    @classmethod
    def _has_next_token(cls, boto_list_stack_resources_result):
        return (
            NEXT_TOKEN in boto_list_stack_resources_result
            and boto_list_stack_resources_result[NEXT_TOKEN] is not None
        )


@dataclasses.dataclass(frozen=True)
class ValidationResult:

    @classmethod
    def from_boto(cls, boto_validation_result: dict[str, Any]) -> "ValidationResult":
        return ValidationResult()
