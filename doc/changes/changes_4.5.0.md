# 4.5.0 - 2026-11-19

## Summary

 - #226: Dropped support for Python 3.10, raised the minimum supported version to Python 3.11.5, and regenerated workflows with PTB 12.0.0, including updating SLC workflow templates to action v12 and Python 3.11.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| tornado | CVE-2026-126347 | 6.6 | 6.6.1 |
| soupsieve | CVE-2026-126189 | 2.10 | 4.0.1 |
| soupsieve | CVE-2026-126190 | 2.10 | 4.0.0 |
| soupsieve | CVE-2026-126193 | 2.10 | 3.0 |

## Dependency Updates

### `main`

* Updated dependency `boto3:1.43.125` to `1.44.7`
* Updated dependency `botocore:1.43.125` to `1.44.7`
* Updated dependency `click:8.5.0` to `8.5.1`
* Updated dependency `exasol-script-languages-container-ci:5.3.0` to `5.4.0`
* Updated dependency `exasol-script-languages-container-tool:4.4.0` to `4.5.0`

### `dev`

* Updated dependency `exasol-toolbox:10.5.0` to `12.0.0`
