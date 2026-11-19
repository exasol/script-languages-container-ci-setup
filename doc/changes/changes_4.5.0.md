# 4.5.0 - 2026-11-19

## Summary

 - #226: Dropped support for Python 3.10, raised the minimum supported version to Python 3.11.5, and regenerated workflows with PTB 12.0.0, including updating SLC workflow templates to action v12.

## Security Issues

This release fixes vulnerabilities by updating the locked SoupSieve dependency:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| soupsieve | CVE-2026-126189 | 2.10 | 4.0.1 |
| soupsieve | CVE-2026-126190 | 2.10 | 4.0.0 |
| soupsieve | CVE-2026-126193 | 2.10 | 3.0 |

## Dependency Updates

### `dev`

* Updated dependency `exasol-toolbox:10.5.0` to `12.0.0`
