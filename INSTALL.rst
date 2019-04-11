Installing Data Catalog CLI
===========================

Local Checkout
--------------

.. code-block:: shell

    $ git clone https://github.com/SD2E/dc-cli.git
    $ cd dc_cli
    $ git checkout master
    $ pip install --user -r requirements.txt
    $ pip install --user  -e .

Using PipEnv
------------

.. code-block:: shell

    $ pip install pipenv
    $ pipenv install "git+https://github.com/SD2E/dc-cli.git@master#egg=dc_cli"

Bash Completion
----------------

You can install bash command line completion to get command hints by tabbing:

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
