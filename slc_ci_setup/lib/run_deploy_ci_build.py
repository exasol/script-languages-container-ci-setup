from slc_ci_setup.lib.render_cloudformation import render_cloudformation
from slc_ci_setup.lib.secret_name_reader import read_dockerhub_secret_name
from slc_ci_setup.lib.upload_cloudformation import upload_cloudformation_stack


def run_deploy_ci_build(aws_profile: str, project: str, github_url: str, stack_name: str):
    """
    This command deploys the ci build cloudformation stack
    1. It get's the dockerhub secret ARN from AWS via AWS CLI
    2. Then it renders the template and uploads the resulting cloudformation YAML file.
    """
    dockerhub_secret_arn = read_dockerhub_secret_name(aws_profile)
    yml = render_cloudformation("slc_code_build.yaml", project=project,
                                dockerhub_secret_arn=dockerhub_secret_arn, github_url=github_url)
    upload_cloudformation_stack(aws_profile, yml, stack_name)

