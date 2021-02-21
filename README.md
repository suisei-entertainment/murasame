<h1 align="center">
    <a name="logo" href="https://www.suiseientertainment.com">
        <img src="https://raw.githubusercontent.com/suisei-entertainment/murasame/development/assets/murasame_full_logo.png"
             alt="Murasame"
             width="1000">
    </a>
    <br>
    <div style="height:80px;font-family:courier;font-size:150%">Murasame Application Development Framework</div>
</h1>

<div align="center">
    <h4>
        <a href="https://travis-ci.org/suisei-entertainment/murasame">
            <img alt="Travis (.org) branch" src="https://img.shields.io/travis/suisei-entertainment/murasame/development?style=for-the-badge">
        </a>
        <a href="https://sonarcloud.io/dashboard?branch=development&id=suisei-entertainment_murasame">
            <img src="https://img.shields.io/badge/dynamic/json?color=blue&stlye=for-the-badge&label=COVERAGE&query=component.measures%5B0%5D.value&suffix=%20%25&url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dsuisei-entertainment_murasame%26metricKeys%3Dcoverage%26branch%3Ddevelopment">
        </a>
        <!--
        <a href="https://sonarcloud.io/dashboard?branch=development&id=suisei-entertainment_murasame">
            <img src="https://sonarcloud.io/api/project_badges/quality_gate?project=suisei-entertainment_murasame&branch=development&style=for-the-badge">
        </a>
        -->
        <a href="https://github.com/suisei-entertainment/murasame/stargazers">
            <img src="https://img.shields.io/github/stars/suisei-entertainment/murasame.svg?style=for-the-badge"/>
        </a>
        <a href="https://github.com/suisei-entertainment/murasame/commits/development">
            <img alt="GitHub last commit (branch)" src="https://img.shields.io/github/last-commit/suisei-entertainment/murasame/development?style=for-the-badge">
        </a>
        <a href="https://github.com/suisei-entertainment/murasame/commits/development">
            <img src="https://img.shields.io/github/license/suisei-entertainment/murasame.svg?style=for-the-badge"/>
        </a>
        <a href="https://github.com/suisei-entertainment/murasame/commits/development">
            <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/suisei-entertainment/murasame?style=for-the-badge">
        </a>
        <a href="https://github.com/suisei-entertainment/murasame/commits/development">
            <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/suisei-entertainment/murasame?style=for-the-badge">
        </a>
        <a href="https://github.com/suisei-entertainment/murasame/commits/development">
            <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/suisei-entertainment/murasame?style=for-the-badge">
        </a>
    </h4>
</div>

Murasame is an application framework for Python to simplify the development of
microservice based cloud applications, primarily the backend side of online
games running inside Docker containers in AWS.

# Features

# Directory Structure

+ **assets**: Contains common binary assets.
+ **doc**: Contains the documentation of the framework.
+ **murasame**: Contains the source code of the framework.
+ **scripts**: Contains various utility scripts used during development.
+ **test**: Contains the tests of the framework.

# Getting Started

## Requirements

Make sure you have the following prerequisites:
+ A base install of Ubuntu with Git installed.

## Installation

Murasame comes with an environment setup script that can be invoked in two ways:
+ If the base operating system already has make installed, you can execute
  the following command in the command line:
    `make setup`
+ If the base operating system doesn't have make installed, you have to call
  the setup script manually in the command line:
    `sudo ./scripts/envsetup`

The setup script has to be executed with root privileges as it will install
various packages on the host system.

After the development environment has been installed the easiest way to get
started is to build the documentation of the framework. This can be done by
activating the generated virtual environment with the following command:
    `source ~/.murasame/.env/bin/activate`

After that you can start the documentation build process by executing the
following command inside the virtual environment:
    `make documentation`

Once the documentation has been built, you can open index.html from
`~/.murasame/dist/documentation`.

Read the **Getting Started** section in the documentation to know how to
continue.
