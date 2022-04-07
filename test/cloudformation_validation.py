import subprocess

import boto3


def validate_using_cfn_lint(tmp_path, cloudformation_yml):
    """
    This test uses cfn-lint to validate the Cloudformation template.
    (See https://github.com/aws-cloudformation/cfn-lint)
    """
    out_file = tmp_path / "slc_source_credential.yaml"
    with open(out_file, "w") as f:
        f.write(cloudformation_yml)

    completed_process = subprocess.run(["cfn-lint", str(out_file.absolute())],
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        completed_process.check_returncode()
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        raise e


def validate_using_aws(cloudformation_yml):
    """
    This test pushes the YAML to AWS Cloudformation for validation
    (see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-validate-template.html)
    Pitfall: Boto3 expects the YAML string as parameter, whereas the AWS CLI expects the file URL as parameter.
    It requires to have the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables set correctly.
    """
    cloud_client = boto3.client('cloudformation')
    cloud_client.validate_template(TemplateBody=cloudformation_yml)
