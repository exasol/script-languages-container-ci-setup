import dataclasses
from test.mock_cast import mock_cast
from typing import Optional
from unittest.mock import (
    Mock,
    call,
)

import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.cloudformation_service import (
    CloudFormationService,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import (
    NextToken,
)
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import (
    PhysicalResourceId,
)


def test_init():
    internal_aws_client = Mock()
    service = CloudFormationService(internal_aws_client=internal_aws_client)
    assert service.internal_aws_client == internal_aws_client


@dataclasses.dataclass(frozen=True)
class ValidateTemplateSetup:
    internal_aws_client = Mock()
    from_boto = Mock()
    service = CloudFormationService(internal_aws_client=internal_aws_client)
    template_body = "TemplateBody"
    validation_result = service.validate_template(
        template_body=template_body, from_boto=from_boto
    )
    internal_aws_client_validate_template_return_value = mock_cast(
        internal_aws_client.validate_template
    ).return_value


def test_validate_template_internal_aws_client():
    setup = ValidateTemplateSetup()
    assert (
        setup.internal_aws_client.mock_calls
        == [call.validate_template(TemplateBody=setup.template_body)]
        and setup.from_boto.mock_calls
        == [call(setup.internal_aws_client_validate_template_return_value)]
        and setup.validation_result == setup.from_boto.return_value
    )


def test_validate_template_from_boto():
    setup = ValidateTemplateSetup()
    assert setup.from_boto.mock_calls == [
        call(setup.internal_aws_client_validate_template_return_value)
    ]


def test_validate_template_result():
    setup = ValidateTemplateSetup()
    assert setup.validation_result == setup.from_boto.return_value


class ListStackResourcesTestSetup:
    def __init__(self, next_token: Optional[NextToken]):
        self.next_token = next_token
        self.internal_aws_client = Mock()
        self.from_boto = Mock()
        self.service = CloudFormationService(
            internal_aws_client=self.internal_aws_client
        )
        self.physical_resource_id = PhysicalResourceId(
            aws_physical_resource_id="stack_name"
        )
        self.list_stack_resources_result = self.service.list_stack_resources(
            stack_name=self.physical_resource_id,
            next_token=next_token,
            from_boto=self.from_boto,
        )
        self.aws_next_token = None if next_token is None else next_token.aws_next_token
        self.internal_aws_client_list_stack_resources_return_value = mock_cast(
            self.internal_aws_client.list_stack_resources
        ).return_value


def test_list_stack_resources_internal_aws_client_next_token_is_none():
    setup = ListStackResourcesTestSetup(None)
    assert setup.internal_aws_client.mock_calls == [
        call.list_stack_resources(
            StackName=setup.physical_resource_id.aws_physical_resource_id
        )
    ]


def test_list_stack_resources_internal_aws_client_next_token_is_not_none():
    next_token = NextToken("next_token")
    setup = ListStackResourcesTestSetup(next_token)
    assert setup.internal_aws_client.mock_calls == [
        call.list_stack_resources(
            StackName=setup.physical_resource_id.aws_physical_resource_id,
            NextToken=next_token.aws_next_token,
        )
    ]


list_stack_resources_parameters = pytest.mark.parametrize(
    "next_token", [NextToken(aws_next_token="next_token"), None]
)


@list_stack_resources_parameters
def test_list_stack_resources_from_boto(next_token):
    setup = ListStackResourcesTestSetup(next_token)
    assert setup.from_boto.mock_calls == [
        call(setup.internal_aws_client_list_stack_resources_return_value)
    ]


@list_stack_resources_parameters
def test_list_stack_resources_result(next_token):
    setup = ListStackResourcesTestSetup(next_token)
    assert setup.list_stack_resources_result == setup.from_boto.return_value
