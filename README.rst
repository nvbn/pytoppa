Python package to ppa
=====================

.. image:: https://travis-ci.org/nvbn/pytoppa.png?branch=develop 
    :target: https://travis-ci.org/nvbn/pytoppa


Upload python packages to your ppa with easy yml config.

Features
---------

- simple configuration file in yaml
- history from git
- adding essential dependencies automatically

.pytoppa.yml config format
-------------------------

In general it looks like:

.. code-block:: yaml

    name: package-name  # optional, by default from setup.py
    section: python  # optional, by default python
    build-dependencies:  # optional
      - one-of-build-deps
    dependencies:  # optional
      - one-of-deps
    releases:
      - one-of-releases

Examples:

- `pytoppa <https://github.com/nvbn/pytoppa/blob/develop/.pytoppa.yml>`_
- `series_list <https://github.com/nvbn/series_list/blob/develop/.pytoppa.yml>`_
- `subliminal <https://github.com/nvbn/subliminal/blob/packaging/.pytoppa.yml>`_

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

.. code-block:: bash

    pip install pytoppa
