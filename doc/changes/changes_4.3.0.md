# 4.3.0 - 2026-03-31

## Summary

This release adds a concurrency group in the GitHub CI workflows to cancel in-progress CI runs. This is supposed to reduce the number of computation time on GitHub.

## Refactorings

 - #191: Added concurrency group to cancel in progress CI runs

## Internal

 - Relocked dependencies to fix vulnerabilities

## Dependency Updates

### `main`
* Updated dependency `boto3:1.42.66` to `1.42.78`
* Updated dependency `botocore:1.42.66` to `1.42.78`
* Updated dependency `exasol-script-languages-container-tool:4.0.2` to `4.0.3`
* Updated dependency `pygithub:2.8.1` to `2.9.0`
