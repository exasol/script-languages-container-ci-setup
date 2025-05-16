# Unreleased

## Internal

 - relocked poetry dependencies to fix CVE-2025-43859 (transitive dependency `h11`)
 - Added python versions for build matrix in file `noxconfig.py`
 - Added GitHub workflow `report.yml`
 - Set Python version for coverage to 3.10 as project does not support Python 3.9

## Refactorings

 - #93: Updated Github workflows from PTB