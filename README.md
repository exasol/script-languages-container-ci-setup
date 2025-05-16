
# Overview

This project is used to deploy the CI scripts for Exasol's Script-Languages-Container.

## Github

Provides an CLI to install the Github workflow files to a Script-Languages-Container repository.

## AWS (deprecated)
This project contains the AWS Cloudformation YAML files to deploy the AWS infrastructure for the ScriptLanguages-Container CI jobs.
Those YAML files are not static, but generated, based on the provided Script-Languages container flavors.

Also it contains a command to create the Buildspec for AWS Code Build, based on the list of flavors.

## Links

* [User Guide](./user_guide/user_guide.md)