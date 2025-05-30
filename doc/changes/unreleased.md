# Unreleased

## Internal

 - relocked poetry dependencies to fix CVE-2025-43859 (transitive dependency `h11`)
 - Added python versions for build matrix in file `noxconfig.py`
 - Added GitHub workflow `report.yml`
 - Set Python version for coverage to 3.10 as project does not support Python 3.9

## Refactorings

 - #93: Updated Github workflows from PTB
 - #105: Update script-languages-container-ci
 - #110: Removed build output preparation and updated exaslc-ci to 2.1.0

## Features

 - #91: Create new templates for Github Workflows - prepare testcontainer
 - #108: Create new templates for Github Workflows - export and scan vulnerabilities
 - #111: Create new templates for Github Workflows - tests
 - #114: Addeed command for deploying cd workflows
