from exasol_script_languages_container_ci_setup.lib import render_template
import exasol_script_languages_container_ci_setup


def run_deploy_ci_build(aws_profile: str, project: str, github_url: str, stack_name: str):
    """
    This command deploys the ci build cloudformation stack
    1. It get's the dockerhub secret ARN from AWS via AWS CLI
    2. Then it renders the template and uploads the resulting cloudformation YAML file.
    """
    dockerhub_secret_arn = exasol_script_languages_container_ci_setup.lib.read_dockerhub_secret_name(aws_profile)
    yml = render_template("slc_code_build.yaml", project=project,
                                dockerhub_secret_arn=dockerhub_secret_arn, github_url=github_url)
    exasol_script_languages_container_ci_setup.lib.upload_cloudformation_stack(aws_profile, yml, stack_name)

