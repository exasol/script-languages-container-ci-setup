import json
import shlex
import subprocess


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
