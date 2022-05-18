# script-languages-container-ci-setup 0.1.0, released 2022-05-18

Code name: Initial release

## Summary

This is the first release of script-languages-container-ci-setup. It supports 3 different command groups:
1. Generation of AWS buildspec yaml file for script-languages project which will be used on AWS Codebuild builds
2. Deployment of AWS Cloudformation stacks which will be used for the CI builds
3. Triggering of AWS Codebuilds (for example to create a release, manually start a CI build)


## Bug Fixes
 
 - #7: Fix ci build for commits which only contain changes in build_config -> ignore-paths 

## Features / Enhancements

 - #1: Implement codebuild deployment and buildspec generation
 - #3: Added release code build
 - #4: Added run-ci command

## Documentation

n/a

## Refactoring

 - #10: Updated dependencies and prepared release
