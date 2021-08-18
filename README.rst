.. image:: https://raw.githubusercontent.com/suisei-entertainment/murasame/development/assets/murasame_full_logo.png
   :target: https://pypi.org/project/murasame
   :width: 1200px
   :alt: Murasame Logo
   :align: center

Murasame is an application framework for Python to simplify the development of
microservice based cloud applications, primarily the backend side of online
games built using Docker containers running in Amazon ECS.

.. image:: https://img.shields.io/pypi/v/murasame.svg
   :target: https://pypi.org/project/murasame

.. image:: https://img.shields.io/pypi/pyversions/murasame.svg
   :target: https://pypi.org/project/murasame

.. image:: https://img.shields.io/travis/suisei-entertainment/murasame/development
   :target: https://travis-ci.com/github/suisei-entertainment/murasame

.. image:: https://img.shields.io/badge/dynamic/json?color=blue&stlye=for-the-badge&label=COVERAGE&query=component.measures%5B0%5D.value&suffix=%20%25&url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dsuisei-entertainment_murasame%26metricKeys%3Dcoverage%26branch%3Ddevelopment
   :target: https://sonarcloud.io/dashboard?branch=development&id=suisei-entertainment_murasame

.. image:: https://sonarcloud.io/api/project_badges/quality_gate?project=suisei-entertainment_murasame&branch=development
   :target: https://sonarcloud.io/dashboard?branch=development&id=suisei-entertainment_murasame

.. image:: https://img.shields.io/github/stars/suisei-entertainment/murasame.svg
   :target: https://github.com/suisei-entertainment/murasame/stargazers

.. image:: https://img.shields.io/github/last-commit/suisei-entertainment/murasame/development
   :target: https://github.com/suisei-entertainment/murasame/commits/development

.. image:: https://img.shields.io/github/license/suisei-entertainment/murasame.svg
   :target: https://github.com/suisei-entertainment/murasame/commits/development

.. image:: https://img.shields.io/github/languages/count/suisei-entertainment/murasame
   :target: https://github.com/suisei-entertainment/murasame/commits/development

.. image:: https://img.shields.io/github/languages/top/suisei-entertainment/murasame
   :target: https://github.com/suisei-entertainment/murasame/commits/development

.. image:: https://img.shields.io/github/repo-size/suisei-entertainment/murasame
   :target: https://github.com/suisei-entertainment/murasame/commits/development

Features
-------------------------------------------------------

On a high level Murasame provides the following features:

* **Application Management**: The framework provides easy to use prototypes to
  implement Linux CLI and daemon applications.
* **Configuration Management**: Configuration management is supported with
  multiple configuration sources and storage formats.
* **Debugging**: The framework provides utilities for debugging applications
  developed using the framework.
* **Events**: The framework provides a simple, subscription based event system.
* **Exceptions**: The framework provides a set of exceptions for error handling
  purposes.
* **License Management**: The framework supports a simple encrypted file based
  licensing model.
* **Localization**: The framework provides support for localizing strings to
  multiple languages, and automatically translate strings through the Google
  Translate API.
* **Logging**: There is support for customized logging mainly based on the
  existing Python logging infrastructure.
* **Platform Abstraction Layer**: The PAL layer offers support for platform
  detection, monitoring and database management.
* **Password Management**: The framework provides utilities for generating and
  validating passwords.
* **Application Utilities**:  There are various utilities to simplify
  application development. Examples:

  * AES and RSA encryption support
  * CLI command processing
  * GeoIP support
  * JSON and YAML file support
  * Product versioning with Semantic Versioning 2.0 support
  * Support for global systems and singletons
  * Certificate support

Requirements
-------------------------------------------------------

Make sure you have the following prerequisites:
* A base install of Ubuntu with Git installed.

Murasame is a framework that requires Python version 3.9 or newer, and it is
not compatible with Python 2.

Applications developed with the framework are primarily meant to be run on a
Linux platform, but the development environment is not restricted to Linux
only. It is recommended to use one of the following:

* Apple Mac OS X 10.13.2 'High Sierra' or later
* Ubuntu 18.04 LTS or later
* Windows 10 or later

In terms of hardware the recommended configuration is at least an 8-core CPU
with 8 GB RAM, and preferably a fast SSD.

Installation
-------------------------------------------------------

There are primarily two ways to install the framework. If you only want to use
the framework without modifying any of its source code, you should simply
install it in your own environment, either in your real environment or inside
a virtualenv.

You can use pip to install the framework:

.. code-block:: shell

    pip install murasame

If you want to have a raw version of the framework and make modifications of it
you should check out the repository of the framework and work with that.

The repository can be found on GitHub:

.. code-block:: shell

    https://github.com/suisei-entertainment/murasame

Murasame comes with an environment setup script that can be invoked in two ways:

* If the base operating system already has make installed, you can execute
  the following command in the command line:

.. code-block:: shell

    make setup

* If the base operating system doesn't have make installed, you have to call
  the setup script manually in the command line:

.. code-block:: shell

    sudo ./scripts/envsetup

The setup script has to be executed with root privileges as it will install
various packages on the host system.

After the development environment has been installed the easiest way to get
started is to build the documentation of the framework. This can be done by
activating the generated virtual environment with the following command:

.. code-block:: shell

    source ~/.murasame/.env/bin/activate

After that you can start the documentation build process by executing the
following command inside the virtual environment:

.. code-block:: shell

    make documentation

Once the documentation has been built, you can open index.html from

.. code-block:: shell

    ~/.murasame/dist/documentation

Alternatively, you can also access the latest released documentation of the
framework on `readthedocs.io`_.

Contributing
-------------------------------------------------------

See the `development documentation`_ about ways you can contribute to the
project.

Code of Conduct
-------------------------------------------------------

Everyone interacting in the Twine project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the
`Code of Conduct`_.

.. _`readthedocs.io`: https://murasame.readthedocs.io
.. _`development documentation`: https://murasame.readthedocs.io
.. _`Code of Conduct`: https://murasame.readthedocs.io/en/latest/code_of_conduct.html