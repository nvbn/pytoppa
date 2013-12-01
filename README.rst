Python package to ppa
=====================

Upload python packages to your ppa with easy yml config.

pytoppa.yml config format
-------------------------

In general it looks like:

.. code-block:: yaml

    section: python  # by default
    dependencies:
      - one-of-deps
    releases:
      - one-of-releases

Examples:
 - `pytoppa <https://github.com/nvbn/pytoppa/blob/develop/pytoppa.yml>`_

Usage
-----

Run in terminal:

.. code-block:: bash

    pytoppa key ppa

For example:

.. code-block:: bash

    pytoppa 'Vladimir Iakovlev <nvbn.rm@gmail.com>' 'ppa:nvbn-rm/ppa'

Installation
------------

In ubuntu:

.. code-block:: bash

    sudo add-apt-repository ppa:nvbn-rm/ppa
    sudo apt-get update
    sudo apt-get install pytoppa

In other:

.. code-block:: bash

    pip install pytoppa
