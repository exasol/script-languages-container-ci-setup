import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import \
    ListStackResourcesResult, NextToken, StackResourceSummary
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId


def test_with_next_token():
    expected_list_stack_resources_result = \
        ListStackResourcesResult(
            next_token=NextToken(aws_next_token="aws_next_token"),
            stack_resource_summaries=[]
        )
    boto_list_stack_resources_result = {
        "NextToken": expected_list_stack_resources_result.next_token.aws_next_token,
        "StackResourceSummaries": []
    }
    list_stack_resources_result = ListStackResourcesResult.from_boto(boto_list_stack_resources_result)
    assert list_stack_resources_result == expected_list_stack_resources_result


def test_with_next_token_none():
    expected_list_stack_resources_result = \
        ListStackResourcesResult(
            next_token=None,
            stack_resource_summaries=[]
        )
    boto_list_stack_resources_result = {
        "NextToken": None,
        "StackResourceSummaries": []
    }
    list_stack_resources_result = ListStackResourcesResult.from_boto(boto_list_stack_resources_result)
    assert list_stack_resources_result == expected_list_stack_resources_result


def test_without_next_token_none():
    expected_list_stack_resources_result = \
        ListStackResourcesResult(
            next_token=None,
            stack_resource_summaries=[]
        )
    boto_list_stack_resources_result = {
        "StackResourceSummaries": []
    }
    list_stack_resources_result = ListStackResourcesResult.from_boto(boto_list_stack_resources_result)
    assert list_stack_resources_result == expected_list_stack_resources_result


@pytest.mark.parametrize("count", range(3))
def test_with_multiple_stack_resource_summary(count: int):
    expected_list_stack_resources_result = \
        ListStackResourcesResult(
            next_token=None,
            stack_resource_summaries=[
                StackResourceSummary(
                    physical_resource_id=PhysicalResourceId(f"physical_resource_id_{i}"),
                    resource_type=f"resource_type_{i}"
                )
                for i in range(count)
            ]
        )
    boto_list_stack_resources_result = {
        "StackResourceSummaries": [
            {
                "PhysicalResourceId": summary.physical_resource_id.aws_physical_resource_id,
                "ResourceType": summary.resource_type
            }
            for summary in expected_list_stack_resources_result.stack_resource_summaries
        ]
    }
    list_stack_resources_result = ListStackResourcesResult.from_boto(boto_list_stack_resources_result)
    assert list_stack_resources_result == expected_list_stack_resources_result


def test_without_stack_resource_summaries():
    boto_list_stack_resources_result = {}
    with pytest.raises(KeyError):
        list_stack_resources_result = ListStackResourcesResult.from_boto(boto_list_stack_resources_result)


def test_with_extra_keys():
    expected_list_stack_resources_result = \
        ListStackResourcesResult(
            next_token=None,
            stack_resource_summaries=[]
        )
    boto_list_stack_resources_result = {
        "NextToken": None,
        "StackResourceSummaries": [],
        "extra1": None,
        "extra2": 1
    }
    list_stack_resources_result = ListStackResourcesResult.from_boto(boto_list_stack_resources_result)
    assert list_stack_resources_result == expected_list_stack_resources_result
