Developer Guide
===============

``slc-ci-setup`` contains GitHub workflows for the script language container. This
document is about the preparations to be done for getting the ``slc-ci-setup`` up and running.

Preparations
------------

This project uses `pre-commit <https://pre-commit.com/>`__ to run
certain Githooks for validation. You don’t have to install
``pre-commit`` as it will be installed with the ``exasol-toolbox``. You
can activate the Githooks simply by running:

.. code:: bash

   pre-commit install

However, if you don’t want to run all the checks during every commit,
you can use:

::

   poetry run nox -s check

to run all available checks on the project.
