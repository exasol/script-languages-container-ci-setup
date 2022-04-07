## Requirements

This package requires:
* Python (>=3.8)
* AWS CLI
* AWS profile

## Installation

You can install the latest wheel package from the [Github Release page](https://github.com/exasol/script-languages-container-ci-setup/releases):
`
pip install https://github.com/exasol/script-languages-container-ci-setup/releases/download/$RELEASE/exasol_script_languages_container_ci-setup-$RELEASE-py3-none-any.whl
`
(Replace $RELEASE with the actual release you are interested in)

## Usage

There are actual 4 commands:
* `health` checks the current environment and setup of your AWS CLI installation
* `deploy-ci-build` deploys the AWS Cloudformation Stack which runs CodeBuild on the given AWS profile
* `deploy-source-credentials` deploys the AWS Cloudformation Stack for the source credentials
* `generate-buildspec` Generates the buildspec files for the given script language flavors.

## Background

In order to accelerate the CI builds of the script language container we want to use AWS CodeBuild batch build, which enables us to run certain steps in parallel. As the number of flavor will change over time, this requires to generate the buildspec again and again in the future. To simplify this process we created this project which automates the generation. Also we expect to have multiple repositories of the script language container in the future, each having it's own Code Build instance. With the automatic generation of the CodeBuild instances via AWS Cloudformation we can simplify this generation of new instances when we have new script language repositories.

### Split of CodeBuild Stack and Source Credentials Stack

We have put the source credentials cloudformation specification in another file because AWS allows to have only one instance of SourceCredential per `ServerType` (GITHUB in our case). See https://thomasstep.com/blog/cloudformation-example-for-codebuild-with-a-webhook for more information.
This means the stack for source credentials needs to be deployed only once, and not per project.


