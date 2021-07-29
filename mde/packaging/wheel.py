## ============================================================================
##             **** Murasame Application Development Framework ****
##                Copyright (C) 2019-2021, Suisei Entertainment
## ============================================================================
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
## ============================================================================

"""
Contains utility functions used for building Python wheels.
"""

# Runtime Imports
import os
import logging
import json
import subprocess

from string import Template

# MDE Imports
from mde.constants import (
    MDE_LOGGER_NAME,
    VERSION_FILE_PATH,
    SETUP_SCRIPT_TEMPLATE_PATH,
    DIST_PATH)

def collect_packages() -> list:

    """Collects the packages of the framework to be added to the wheel.

    Returns:
        A list with all packages within the framework.

    Authors:
        Attila Kovacs
    """

    result = ['murasame']

    objects = os.scandir('./murasame')

    for obj in objects:
        if obj.is_dir() and obj.name != '__pycache__':
            result.append(f'murasame.{obj.name}')
            subdirs = os.scandir(f'./murasame/{obj.name}')
            for subdir in subdirs:
                if subdir.is_dir() and subdir.name != '__pycache__':
                    result.append(f'murasame.{obj.name}.{subdir.name}')

    return result

def collect_dependencies() -> list:

    """Collects the dependencies of the framework to be added to the setup
    script.

    Dependencies are identified by analyzing the requirements.txt file in the
    framework's repository.

    Returns:
        A list with all required dependencies.

    Authors:
        Attila Kovacs
    """

    result = []
    lines = None

    logger = logging.getLogger(MDE_LOGGER_NAME)

    try:
        with open('./requirements.txt', 'r') as requirements:
            lines = requirements.readlines()
    except OSError as error:
        logger.error('     - Failed to read the contents of requirements.txt')
        raise SystemExit from error

    for line in lines:
        if not line.startswith('#') and not line.startswith('\n'):
            # Remove potential comments at the end of the line
            if '#' in line:
                line, dummy = str.split(line, '#', 1)
            result.append(line.strip().replace('\n', ''))

    return result

def create_wheel() -> None:

    """Creates the Python wheel.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug(' Creating Python wheel...')

    logger.debug('     - Creating setup.py...')

    template = None

    # Retrieving version data
    version_data = None
    major_version = None
    minor_version = None
    patch_level = None

    # Open configuration file
    try:
        with open(VERSION_FILE_PATH, 'r') as config_file:
            version_data = json.load(config_file)
    except OSError as error:
        logger.error('     - Failed to read the contents of version.conf.')
        raise SystemExit from error
    except json.JSONDecodeError as error:
        logger.error('     - Failed to parse the content of version.conf.')
        raise SystemExit from error

    try:
        major_version = version_data['major']
        logger.debug(f'     - Major version: {major_version}')
    except KeyError as error:
        logger.error('     - No major version was found in version.conf')
        raise SystemExit from error

    try:
        minor_version = version_data['minor']
        logger.debug(f'     - Minor version: {minor_version}')
    except KeyError as error:
        logger.error('     - No minor version was found in version.conf')
        raise SystemExit from error

    try:
        patch_level = version_data['patch']
        logger.debug(f'     - Patch level: {patch_level}')
    except KeyError as error:
        logger.error('     - No patch level was found in version.conf')
        raise SystemExit from error

    # Load setup.py template
    try:
        with open(SETUP_SCRIPT_TEMPLATE_PATH, 'r') as setup_template:
            template = setup_template.read()
    except OSError as error:
        logger.error(f'     - Failed to load the setup script '
                     f'template from {SETUP_SCRIPT_TEMPLATE_PATH}')
        raise SystemExit from error


    # Create file content
    template = Template(template)
    setup_string = template.safe_substitute(
        major_version=major_version,
        minor_version=minor_version,
        patch_level=patch_level,
        packages=collect_packages(),
        install_requires=collect_dependencies())

    # Write the file
    with open('./setup.py', 'w+') as setup_file:
        setup_file.write(setup_string)

    logger.debug('     - Running setup.py...')
    try:
        subprocess.check_call(
            [\
                'python',
                'setup.py',
                'bdist_wheel',
                '--dist-dir', DIST_PATH,
                'clean'])
    except subprocess.CalledProcessError as error:
        logger.error('Failed to create wheel.')
        raise SystemExit from error

    logger.debug(' Python wheel created.')