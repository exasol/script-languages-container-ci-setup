# 3.3.1 - 2025-08-05

This release updates the poetry lock file. Especially, the Exasol Python Toolbox was updated to version 1.7.3. The generated GH workflow files now will use the Python Setup GH Action from PTB 1.7.3. This fixes issues with installing pipx on newer pip versions in the CI.

## Refactorings

 - #161: Migrated to PTB 1.7.3
 - #164: Migrated to PTB 1.7.4

## Dependency Updates

### `main`
* Updated dependency `boto3:1.39.3` to `1.40.1`
* Updated dependency `botocore:1.39.3` to `1.40.1`
* Updated dependency `exasol-script-languages-container-tool:3.3.0` to `3.4.1`
* Updated dependency `jsonschema:4.24.0` to `4.25.0`
* Updated dependency `pygithub:2.6.1` to `2.7.0`

### `dev`
* Updated dependency `exasol-toolbox:1.6.0` to `1.7.3`
