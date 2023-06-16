from exasol_script_languages_container_ci_setup.lib.aws.wrapper.datamodels.cloudformation import ValidationResult


def test_empyt_dict():
    boto_validation_result = {}
    validation_result = ValidationResult.from_boto(boto_validation_result)
    assert validation_result == ValidationResult()


def test_with_extra_keys():
    boto_validation_result = {
        "extra1": None,
        "extra2": 1
    }
    validation_result = ValidationResult.from_boto(boto_validation_result)
    assert validation_result == ValidationResult()
