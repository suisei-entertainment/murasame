.. image:: ./../assets/murasame_full_logo_white.png
  :width: 1000
  :align: center
  :alt: Murasame Logo

Introduction
=========================================

Welcome to the documentation of the Murasame Application Development Framework.
This document is generated from the current version of the framework, and
contains up-to-date information about this version.

Murasame is meant to be an application framework to implement the server side
of online games. Primarily it is not a generic application framework as it's
main purpose is to act as a foundation for the SEED platform.

Features
-----------------------------------------

On a high level Murasame provides the following features:

* **Application Management**: The framework provides easy to use prototypes to
  implement Linux CLI and daemon applications.
* **Configuration Management**: Configuration management is supported with
  multiple configuration sources and storage formats.
* **Debugging**: The framework provides utilities for debugging applications
  developed using the framework.
* **Entity-Component System**: There is a simple entity-component system to
  represent and update the state of a virtual world.
* **Exceptions**: The framework provides a set of exceptions for error handling
  purposes.
* **License Management**: The framework supports a simple encrypted file based
  licensing model.
* **Logging**: There is support for customized logging mainly based on the
  exising Python logging infrastructure.
* **OSI System Management**: The framework contains an implementation of the
  OSI System Management recommendations to allow remove management of
  applications implemented with the framework.
* **Platform Abstraction Layer**: The PAL layer offers support for platform
  detection, monitoring and database management.
* **Password Management**: The framework provides utilities for generating and
  validating passwords.
* **Service Management**: The framework provides support for running
  microservice based applications in a cloud environment.
* **Application Utilities**:  There are various utilities to simplify
  application development. Examples:

  * AES and RSA encryption support
  * CLI command processing
  * GeoIP support
  * JSON and YAML file support
  * Product versioning with Semantic Versioning 2.0 support
  * Support for global systems and singletons
  * Certificate support

Getting Started
=========================================

Requirements
-----------------------------------------

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
-----------------------------------------

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
https://github.com/suisei-entertainment/murasame

To work with the repository you should read the Development and Testing
sections of this guide.

Directory Structure
-----------------------------------------

The top level directory structure of the Murasame repository is the following:

* **.git**: The directory containing Git internals. Do not touch, unless you
  absolutely know what you are doing.
* **assets**: Contains all binary assets, typically images and other media.
* **doc**: Contains the documentation of the framework.
* **examples**: Contains various example applications demonstrating the
  features of the framework.
* **murasame**: Contains the Python source code of the various components of
  the framework.
* **scripts**: Contains various utility scripts mainly utilized by CI.
* **test**: Contains all tests of the framework.

Each subdirectory contains additional README.md files with a description of
the content of that subdirectory.

Recommended Editors and Tools
-----------------------------------------

The repository comes with a
`Sublime Text 3 <https://www.sublimetext.com/>`_ project file, as our preferred
editor is Sublime Text 3. On top of Sublime Text 3 you might find the following
Sublime packages useful:

* `Package Control <https://packagecontrol.io/>`_: The basic package manager
  plugin for Sublime Text 3.
* `Anaconda <http://damnwidget.github.io/anaconda/>`_: A quite good Python
  development environment for Sublime Text 3.
* `Sublime Linter <https://github.com/SublimeLinter/SublimeLinter>`_: A code
  linting framework for Sublime Text 3.
* `Sublime Linter - pylint <https://github.com/SublimeLinter/SublimeLinter-pylint>`_:
  A linter plugin for Sublime Linter that executes pylint.
* `SublimeCodeIntel <https://packagecontrol.io/packages/SublimeCodeIntel>`_: An
  interface plugin for CodeIntel.
* `A File Icon <https://github.com/sublimetext/afileicon>`_: Adds file type
  specific icons to Sublime Text 3.
* `Bracket Highlighter <https://github.com/facelessuser/BracketHighlighter>`_:
  Utility package that helps matching opening and closing brackets of various
  types.
* `Git <https://github.com/kemayo/sublime-text-git>`_: Adds Git interaction
  to Sublime Text 3.
* `GitGutter <https://github.com/jisaacks/GitGutter>`_: Adds Git diff support
  to Sublime Text 3.
* `Log Highlight <https://packagecontrol.io/packages/Log%20Highlight>`_: Adds
  the option to specify syntax highlighting for log files.
* `Trailing Spaces <https://github.com/SublimeText/TrailingSpaces>`_:
  Highlights and automatically removes unnecessary whitespaces from the end of
  source code lines.
* `INI <https://packagecontrol.io/packages/INI>`_: Provides syntax
  highlighting for INI files.
* `Markdown Extended <https://github.com/jonschlinkert/sublime-markdown-extended>`_:
  Provides additional syntax highlighting for markdown files.
* `Protobuf Syntax Highlighting <https://packagecontrol.io/packages/Protobuf%20Syntax%20Hightlighting>`_:
  Provides syntax highlighting for Google Protocol Buffer files.
* `SideBar Enchancements <https://github.com/SideBarEnhancements-org/SideBarEnhancements>`_:
  Provides various sidebar enhancements to the default Sublime Text 3 sidebar.
* `TTCNComplete <https://packagecontrol.io/packages/TtcnComplete>`_: Provides
  syntax highlighting and code completion for TTCN.
* `AutoDocstring <https://packagecontrol.io/packages/AutoDocstring>`_: Provides
  support to automatically generate Python docstring skeletons.
* `Dockerfile Syntax Highlight <https://packagecontrol.io/packages/Dockerfile%20Syntax%20Highlight>`_: Provides
  syntax highlighting for Dockerfile.
* `Color Highlighter <https://packagecontrol.io/packages/Color%20Highlighter>`_: Underlays
  selected hexadecimal colorcodes.

Development
-----------------------------------------

Testing
-----------------------------------------

Coding Style
-----------------------------------------

Table of Contents
=========================================

.. toctree::
    :maxdepth: 2

    architecture
    tutorials
    code_documentation
    references
    glossary

Table of Indices
=========================================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
