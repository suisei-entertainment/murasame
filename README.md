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
        <a href="https://github.com/suisei-entertainment/murasame/stargazers">
            <img src="https://img.shields.io/github/stars/suisei-entertainment/murasame.svg?style=plasticr"/>
        </a>
        <a href="https://github.com/suisei-entertainment/murasame/commits/development">
            <img src="https://img.shields.io/github/last-commit/suisei-entertainment/murasame.svg?style=plasticr"/>
        </a>
        <a href="https://github.com/suisei-entertainment/murasame/commits/development">
            <img src="https://img.shields.io/github/license/suisei-entertainment/murasame.svg?style=plasticr"/>
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
