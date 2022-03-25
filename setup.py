# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['script_languages_container_ci_setup',
 'script_languages_container_ci_setup.cli',
 'script_languages_container_ci_setup.cli.commands',
 'script_languages_container_ci_setup.cli.options',
 'script_languages_container_ci_setup.lib']

package_data = \
{'': ['*'], 'script_languages_container_ci_setup': ['templates/*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'exasol_error_reporting_python @ '
 'git+https://github.com/exasol/error-reporting-python.git@main',
 'jinja2>=3.0.0',
 'script-languages-container-ci @ '
 'git+https://github.com/exasol/script-languages-container-ci.git@feature/1_add_initial_implementation_of_slc_ci_project']

setup_kwargs = {
    'name': 'script-languages-container-ci-setup',
    'version': '0.1.0',
    'description': 'Manages AWS cloud CI build infrastructure.',
    'long_description': None,
    'author': 'Thomas Uebensee',
    'author_email': 'ext.thomas.uebensee@exasol.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
