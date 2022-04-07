import shlex
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import jinja2


def upload_cloudformation_stack(aws_profile: str, yml: str, stack_name: str):
    with TemporaryDirectory() as yml_dir:
        yml_file_path = Path(yml_dir) / "cloudformation.yaml"
        with open(yml_file_path, "w") as yml_file:
            yml_file.write(yml)
        command = f"aws cloudformation deploy --stack-name {stack_name} " \
                  f"--profile {aws_profile} --template-file {yml_file_path} " \
                  f"--capabilities CAPABILITY_IAM"
        print(f"Invoking command: {command}")
        completed_process = subprocess.run(shlex.split(command))
        try:
            completed_process.check_returncode()
        except subprocess.CalledProcessError as e:
            sys.exit(1)


def get_secret_arn_from_json(json_txt: str, secret_name: str):
    secret_result = json.loads(json_txt)
    secret_list = secret_result["SecretList"]
    interesting_secrets = [s for s in secret_list if s["Name"] == secret_name]
    if len(interesting_secrets) == 0:
        print("Dockerhub secret not registered in SecretManager!")
        exit(1)
    elif len(interesting_secrets) > 1:
        print("More than one Dockerhub secret registered in SecretManager!")
        exit(1)
    return interesting_secrets[0]["ARN"]


def read_secret_name(aws_profile: str, secret_name: str):
    command = f"aws --profile {aws_profile} secretsmanager list-secrets"
    completed_process = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        completed_process.check_returncode()
    except subprocess.CalledProcessError as e:
        print(f"Error getting the ARN of the Dockerhub secret from AWS Secret Manager:\n{e.stdout.decode('UTF-8')}")
        exit(1)
    return get_secret_arn_from_json(completed_process.stdout.decode("utf-8"), secret_name)


def read_dockerhub_secret_name(aws_profile: str):
    return read_secret_name(aws_profile, "Dockerhub")


def render_template(template: str, **kwargs):
    env = jinja2.Environment(loader=jinja2.PackageLoader("exasol_script_languages_container_ci_setup"),
                             autoescape=jinja2.select_autoescape())
    t = env.get_template(template)
    return t.render(**kwargs)
