import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import StackResourceSummary
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import PhysicalResourceId


def test_valid():
    expected_stack_resource_summary = StackResourceSummary(
        physical_resource_id=PhysicalResourceId("physical_resource_id"),
        resource_type="resource_type")
    boto_stack_resource_summary = {
        "PhysicalResourceId": expected_stack_resource_summary.physical_resource_id.aws_physical_resource_id,
        "ResourceType": expected_stack_resource_summary.resource_type
    }
    stack_resource_summary = StackResourceSummary.from_boto(boto_stack_resource_summary)
    assert stack_resource_summary == expected_stack_resource_summary


def test_without_physical_resource_id():
    expected_stack_resource_summary = StackResourceSummary(
        physical_resource_id=None,
        resource_type="resource_type")

    boto_stack_resource_summary = {
        "ResourceType": "resource_type"
    }
    stack_resource_summary = StackResourceSummary.from_boto(boto_stack_resource_summary)
    assert stack_resource_summary == expected_stack_resource_summary


def test_physical_resource_id_none():
    expected_stack_resource_summary = StackResourceSummary(
        physical_resource_id=None,
        resource_type="resource_type")

    boto_stack_resource_summary = {
        "physical_resource_id": None,
        "ResourceType": "resource_type"
    }
    stack_resource_summary = StackResourceSummary.from_boto(boto_stack_resource_summary)
    assert stack_resource_summary == expected_stack_resource_summary


def test_without_resource_type():
    with pytest.raises(KeyError):
        boto_stack_resource_summary = {
            "PhysicalResourceId": "physical_resource_id",
        }
        stack_resource_summary = StackResourceSummary.from_boto(boto_stack_resource_summary)


def test_with_extra_keys():
    expected_stack_resource_summary = StackResourceSummary(
        physical_resource_id=PhysicalResourceId("physical_resource_id"),
        resource_type="resource_type")
    boto_stack_resource_summary = {
        "PhysicalResourceId": expected_stack_resource_summary.physical_resource_id.aws_physical_resource_id,
        "ResourceType": expected_stack_resource_summary.resource_type,
        "extra1": None,
        "extra2": 1
    }
    stack_resource_summary = StackResourceSummary.from_boto(boto_stack_resource_summary)
    assert stack_resource_summary == expected_stack_resource_summary
