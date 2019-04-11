
Data Catalog CLI
================

.. image:: https://badge.fury.io/gh/SD2E%2Fdc-cli.svg
   :target: https://badge.fury.io/gh/SD2E%2Fdc-cli
   :alt: GitHub repository

The Data Catalog CLI is a command-line client written in Python (based on OpenStack's `cliff <https://github.com/openstack/cliff>`_ framework) for the SD2E Data Catalog, a schema-driven metadata store and data integration
service.

- `Documentation <https://dc-cli.readthedocs.io/en/latest/>`_
- `Bugs/Issues <https://github.com/SD2E/dc-cli/issues>`_

Installation
------------

The Data Catalog CLI cannot currently be installed from PyPI. The preferred installation
path while it is in active development is to install from GitHub source. Because of
reliance on Python modules that are not yet in PyPi, it is recommended to use the
(relatively) new ``pipenv`` Python packaging manager to install ``dc-cli``.

.. code-block:: shell

    $ pip install pipenv
    $ pipenv install "git+https://github.com/SD2E/dc-cli.git@master#egg=dc_cli"

More extensive installation documentation `is available <./INSTALL.rst>`_.

Getting Started
---------------

The CLI features extensive contextual help, which should help you learn to use
it. For instance, a listing of supported commands and global options can be \
shown with ``--help``:

.. code-block:: shell

    $ dcat --help

There is also a ``help`` command that can be used to get help for specific commands:

.. code-block:: shell

    $ dcat help challenges list
    $ dcat challenges list --help

(Optional) You can install bash command line completion to get command hints
by tabbing.

.. code-block:: shell

    $ dcat complete >> ~/.bash_aliases
    $ . ~/.bash_aliases  # add to ~/.bashrc or ~/.bash_profile to always load (Ubuntu distros already load it)
    $ dcat <tab>
    challenge    experiment   id           pipeline     version
    complete     file         job          sample
    design       help         measurement  token

.. note::

    **Mac OS X Users**: You may need to install autocomplete support before
    this works. We recommend using Homebrew: ``brew install bash-completion``.

Configuration
-------------

The Data Catalog CLI can be configured with environment variables, an .env file,
or via command-line options.

There are two essential variables:
    * ``MONGODB_USERNAME``: A username for the current Data Catalog
    * ``MONGODB_PASSWORD``: A password for the current Data Catalog

The corresponding command-line options are:

.. code-block:: shell

    --username USERNAME   MongoDB username
    --password PASSWORD   MongoDB password

Values for these variables are available to all program members from the SD2E **user support** team.

Additional variables enable administrative tasks such as loading and deleting metadata or managing job states:
    * ``ADMIN_TOKEN_KEY``
    * ``JOB_MANAGER_NONCE``

The corresponding command-line options are:

.. code-block:: shell

    --key <adminKey>    Key for generating an admin token
    --job-manager-nonce <actorNonce>    Jobs Manager authorization nonce

These values are available to authorized users from the SD2E **data management** team.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

Variable names can be set interactively in the shell like so:

.. code-block:: shell

    export MONGODB_USERNAME="bigdata"
    export MONGODB_PASSWORD="IsJustLargerThanYouAreAccustomedTo"

They can also be included in an ``.env`` file that can reside either in the
current working directory or in the user's ``$HOME``. A sample ``.env`` file
is included with this repository.

License
-------

See LICENSE.txt for license information.

Authors
-------

- Matthew Vaughn <opensource@tacc.cloud>
