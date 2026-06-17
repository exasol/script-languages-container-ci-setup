# 4.4.0 - 2026-06-17

## Summary

This release contains some internal improvements.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| cryptography | PYSEC-2026-36 | 46.0.6 | 46.0.7 |
| cryptography | PYSEC-2026-36 | 46.0.6 | 46.0.7 |
| cryptography | GHSA-537c-gmf6-5ccf | 46.0.6 | 48.0.1 |
| gitpython | CVE-2026-42215 | 3.1.46 | 3.1.47 |
| gitpython | CVE-2026-42284 | 3.1.46 | 3.1.47 |
| gitpython | CVE-2026-44244 | 3.1.46 | 3.1.49 |
| gitpython | GHSA-mv93-w799-cj2w | 3.1.46 | 3.1.50 |
| idna | PYSEC-2026-215 | 3.11 | 3.15 |
| pip | PYSEC-2026-196 | 26.0.1 | 26.1.2 |
| pip | CVE-2026-3219 | 26.0.1 | 26.1 |
| pip | CVE-2026-6357 | 26.0.1 | 26.1 |
| pyjwt | PYSEC-2026-179 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-175 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-177 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-178 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-177 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-179 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-176 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-178 | 2.12.1 | 2.13.0 |
| pytest | CVE-2025-71176 | 9.0.2 | 9.0.3 |
| tornado | CVE-2026-49854 | 6.5.5 | 6.5.6 |
| tornado | CVE-2026-49853 | 6.5.5 | 6.5.6 |
| tornado | CVE-2026-49855 | 6.5.5 | 6.5.6 |
| tornado | GHSA-pw6j-qg29-8w7f | 6.5.5 | 6.5.7 |
| urllib3 | PYSEC-2026-142 | 2.6.3 | 2.7.0 |
| urllib3 | PYSEC-2026-142 | 2.6.3 | 2.7.0 |
| urllib3 | PYSEC-2026-141 | 2.6.3 | 2.7.0 |

## Internal

 - #202: Resolved vulnerabilities and updated PTB
 - #197: Removed explicit dependency to "requests"
 - #204: Updated PTB to 9.0.0

## Dependency Updates

### `main`

* Updated dependency `boto3:1.42.80` to `1.43.31`
* Updated dependency `botocore:1.42.80` to `1.43.31`
* Updated dependency `click:8.3.1` to `8.4.1`
* Updated dependency `exasol-script-languages-container-ci:5.1.1` to `5.2.0`
* Updated dependency `exasol-script-languages-container-tool:4.0.3` to `4.1.0`
* Updated dependency `pygithub:2.9.0` to `2.9.1`
* Removed dependency `requests:2.33.1`

### `dev`

* Updated dependency `exasol-toolbox:6.1.1` to `9.0.0`
* Updated dependency `pytest:9.0.2` to `9.1.0`
