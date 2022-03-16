import shlex
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


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
