# 4.4.2 - 2026-11-06

## Summary

Updated workflow templates. v4.4.1 uses jlumbroso/free-disk-space,
but the action was renamed, causing workflows generated from v4.4.1 to fail.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| anyio | PYSEC-2026-4025 | 4.14.0 | 4.14.2 |
| anyio | PYSEC-2026-4023 | 4.14.0 | 4.14.2 |
| anyio | PYSEC-2026-4024 | 4.14.0 | 4.14.2 |
| black | CVE-2026-114134 | 26.5.1 | 26.10.1 |
| certifi | PYSEC-2026-4320 | 2026.6.17 | 2026.10.18 |
| certifi | PYSEC-2026-4320 | 2026.6.17 | 2026.10.18 |
| cryptography | PYSEC-2026-3552 | 49.0.0 | 50.0.0 |
| cryptography | PYSEC-2026-3552 | 49.0.0 | 50.0.0 |
| filelock | CVE-2026-112940 | 3.29.4 | 4.2.1 |
| filelock | CVE-2026-112913 | 3.29.4 | 4.2.1 |
| filelock | CVE-2026-112907 | 3.29.4 | 4.2.1 |
| filelock | CVE-2026-112936 | 3.29.4 | 4.0.9 |
| filelock | CVE-2026-112910 | 3.29.4 | 4.2.1 |
| filelock | CVE-2026-112909 | 3.29.4 | 4.2.1 |
| filelock | CVE-2026-112939 | 3.29.4 | 4.2.1 |
| filelock | CVE-2026-112915 | 3.29.4 | 4.2.1 |
| filelock | CVE-2026-112935 | 3.29.4 | 4.2.1 |
| gitpython | PYSEC-2026-3947 | 3.1.50 | 3.1.51 |
| gitpython | PYSEC-2026-3984 | 3.1.50 | 3.1.60 |
| gitpython | PYSEC-2026-3982 | 3.1.50 | 3.1.60 |
| gitpython | PYSEC-2026-3981 | 3.1.50 | 3.1.53 |
| gitpython | PYSEC-2026-3836 | 3.1.50 | 3.1.51 |
| gitpython | PYSEC-2026-3995 | 3.1.50 | 3.1.54 |
| gitpython | PYSEC-2026-3981 | 3.1.50 | 3.1.53 |
| gitpython | PYSEC-2026-3951 | 3.1.50 | 3.1.55 |
| gitpython | PYSEC-2026-3783 | 3.1.50 | 3.1.58 |
| gitpython | PYSEC-2026-3984 | 3.1.50 | 3.1.60 |
| gitpython | PYSEC-2026-3785 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3786 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3783 | 3.1.50 | 3.1.58 |
| gitpython | PYSEC-2026-3787 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3788 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3784 | 3.1.50 | 3.1.58 |
| gitpython | PYSEC-2026-3786 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3787 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3788 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3837 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3840 | 3.1.50 | 3.1.58 |
| gitpython | PYSEC-2026-3836 | 3.1.50 | 3.1.51 |
| gitpython | PYSEC-2026-3838 | 3.1.50 | 3.1.58 |
| gitpython | PYSEC-2026-3839 | 3.1.50 | 3.1.51 |
| gitpython | PYSEC-2026-3841 | 3.1.50 | 3.1.58 |
| gitpython | PYSEC-2026-3837 | 3.1.50 | 3.1.59 |
| gitpython | PYSEC-2026-3843 | 3.1.50 | 3.1.58 |
| gitpython | PYSEC-2026-3949 | 3.1.50 | 3.1.57 |
| gitpython | PYSEC-2026-3951 | 3.1.50 | 3.1.55 |
| gitpython | PYSEC-2026-3953 | 3.1.50 | 3.1.54 |
| gitpython | PYSEC-2026-3952 | 3.1.50 | 3.1.54 |
| gitpython | PYSEC-2026-3950 | 3.1.50 | 3.1.56 |
| gitpython | PYSEC-2026-3948 | 3.1.50 | 3.1.57 |
| gitpython | CVE-2026-114145 | 3.1.50 | 3.2.1 |
| gitpython | CVE-2026-110859 | 3.1.50 | 3.2.0 |
| gitpython | CVE-2026-110858 | 3.1.50 | 3.2.0 |
| gitpython | CVE-2026-110856 | 3.1.50 | 3.2.0 |
| gitpython | CVE-2026-110857 | 3.1.50 | 3.2.0 |
| gitpython | CVE-2026-110855 | 3.1.50 | 3.2.0 |
| msgpack | PYSEC-2026-3625 | 1.2.0 | 1.2.1 |
| msgpack | PYSEC-2026-3625 | 1.2.0 | 1.2.1 |
| msgpack | CVE-2026-114613 | 1.2.0 | 1.2.3 |
| pip | PYSEC-2026-3721 | 26.1.2 | 26.2 |
| pip | PYSEC-2026-3721 | 26.1.2 | 26.2.0 |
| pyjwt | PYSEC-2026-4145 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4149 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4152 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4144 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4143 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4148 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4140 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4141 | 2.13.0 | 2.15.0 |
| pyjwt | PYSEC-2026-4147 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4151 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4150 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4142 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4183 | 2.13.0 | 2.15.0 |
| pyjwt | GHSA-pxh4-856f-4h89 | 2.13.0 | 2.14.0 |
| pylint | CVE-2026-114608 | 4.0.6 | 4.0.9 |
| setuptools | PYSEC-2026-3447 | 82.0.1 | 83.0.0 |
| setuptools | PYSEC-2026-3447 | 82.0.1 | 83.0.0 |
| setuptools | GHSA-xmj3-9gf7-h52w | 82.0.1 | 84.1.0 |
| soupsieve | PYSEC-2026-4170 | 2.8.4 | 2.9.0 |
| soupsieve | PYSEC-2026-4171 | 2.8.4 | 2.9.0 |
| tornado | PYSEC-2026-3928 | 6.5.7 | 6.5.8 |
| tornado | GHSA-chx6-46f5-w4vp | 6.5.7 | 6.5.9 |
| tornado | GHSA-c2m8-h5v5-343r | 6.5.7 | 6.5.9 |
| tornado | GHSA-3hv7-mjh2-fv65 | 6.5.7 | 6.5.9 |
| tornado | GHSA-wwv5-g3v4-889x | 6.5.7 | 6.5.8 |
| tornado | GHSA-8423-8fgw-73vq | 6.5.7 | 6.5.8 |
| tornado | CVE-2026-116577 | 6.5.7 | 6.6 |
| tornado | CVE-2026-115927 | 6.5.7 | 6.6 |
| tornado | CVE-2026-116578 | 6.5.7 | 6.6 |
| urllib3 | PYSEC-2026-4177 | 2.7.0 | 2.8.0 |
| urllib3 | PYSEC-2026-4176 | 2.7.0 | 2.8.0 |
| urllib3 | PYSEC-2026-4175 | 2.7.0 | 2.8.0 |
| virtualenv | PYSEC-2026-4011 | 21.5.1 | 21.7.12 |
| virtualenv | PYSEC-2026-4012 | 21.5.1 | 21.7.11 |
| virtualenv | PYSEC-2026-4014 | 21.5.1 | 21.7.12 |
| virtualenv | PYSEC-2026-4013 | 21.5.1 | 21.7.13 |
| virtualenv | PYSEC-2026-4011 | 21.5.1 | 21.7.12 |
| virtualenv | PYSEC-2026-4012 | 21.5.1 | 21.7.11 |
| virtualenv | PYSEC-2026-4013 | 21.5.1 | 21.7.13 |
| virtualenv | PYSEC-2026-4014 | 21.5.1 | 21.7.12 |
| virtualenv | CVE-2026-113726 | 21.5.1 | 21.14.4 |
| virtualenv | CVE-2026-113776 | 21.5.1 | 21.14.2 |
| virtualenv | CVE-2026-113732 | 21.5.1 | 21.14.2 |
| virtualenv | CVE-2026-113725 | 21.5.1 | 21.14.7 |
| virtualenv | CVE-2026-113722 | 21.5.1 | 21.14.9 |
| virtualenv | CVE-2026-113714 | 21.5.1 | 21.14.9 |
| virtualenv | CVE-2026-113723 | 21.5.1 | 21.14.9 |
| virtualenv | CVE-2026-113715 | 21.5.1 | 21.14.9 |
| virtualenv | CVE-2026-113720 | 21.5.1 | 21.14.9 |
| virtualenv | CVE-2026-113717 | 21.5.1 | 21.14.9 |
| virtualenv | CVE-2026-113718 | 21.5.1 | 21.14.9 |

## Refactoring

* #210: Updated to exasol-toolbox 10.2.1

## Security

* #211: Resolved issues found by zizmor

## Dependency Updates

### `main`

* Updated dependency `boto3:1.43.31` to `1.43.125`
* Updated dependency `botocore:1.43.31` to `1.43.125`
* Updated dependency `click:8.4.1` to `8.5.0`
* Updated dependency `exasol-script-languages-container-ci:5.2.1` to `5.3.0`
* Updated dependency `exasol-script-languages-container-tool:4.1.0` to `4.4.0`
* Updated dependency `pygithub:2.9.1` to `2.10.0`

### `dev`

* Updated dependency `actionlint-py:1.7.12.24` to `1.7.12.25`
* Updated dependency `exasol-toolbox:9.0.0` to `10.5.0`
* Updated dependency `pytest:9.1.0` to `9.2.0`
* Updated dependency `pytest-mock:3.15.1` to `3.17.0`
