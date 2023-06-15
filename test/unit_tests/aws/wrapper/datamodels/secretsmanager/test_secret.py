import pytest

from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.common import ARN
from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.secretsmanager import Secret


def test_arn_exists():
    expected = Secret(arn=ARN(aws_arn="EXPECTED_ARN"))
    boto_secret = {"ARN": expected.arn.aws_arn}
    actual = Secret.from_boto(boto_secret)
    assert actual.arn == expected.arn


def test_arn_not_exists():
    with pytest.raises(KeyError):
        boto_secret = {}
        secret = Secret.from_boto(boto_secret)


def test_with_extra_keys():
    expected = Secret(arn=ARN(aws_arn="EXPECTED_ARN"))
    boto_secret = {
        "ARN": expected.arn.aws_arn,
        "extra1": None,
        "extra2": 1
    }
    actual = Secret.from_boto(boto_secret)
    assert actual == expected


def test_empty_arn():
    with pytest.raises(ValueError, match="ARN was None"):
        boto_secret = {
            "ARN": None
        }
        secret = Secret.from_boto(boto_secret)
