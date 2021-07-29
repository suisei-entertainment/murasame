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
Contains utility functions used for handling version numbers.
"""

# Runtime Imports
import os
import json
import logging

# MDE Imports
from mde.constants import (
    VERSION_FILE_PATH,
    MDE_LOGGER_NAME,
    VERSION_TEMPLATE_PATH)
from mde.utils.travis import is_travis

def get_version_num() -> str:

    """Returns the version number as stored in the version config file.

    Authors:
        Attila Kovacs
    """

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
        raise SystemExit from error
    except json.JSONDecodeError as error:
        raise SystemExit from error

    try:
        major_version = version_data['major']
    except KeyError as error:
        raise SystemExit from error

    try:
        minor_version = version_data['minor']
    except KeyError as error:
        raise SystemExit from error

    try:
        patch_level = version_data['patch']
    except KeyError as error:
        raise SystemExit from error

    return f'{major_version}.{minor_version}.{patch_level}'

def get_version_string() -> str:

    """Returns the version string as stored in the version config file.

    Authors:
        Attila Kovacs
    """

    return f'v{get_version_num()}'

def bump_version_number() -> None:

    """Loads the version configuration file, increases the build number and
    saves it to be used by the rest of the build script.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug('Increasing build number in version.conf...')

    # Open configuration file
    try:
        with open(VERSION_FILE_PATH, 'r') as config_file:
            version_data = json.load(config_file)
    except FileNotFoundError:
        logger.warning('     - Version.conf doesn\'t exist yet, '
                       'creating it with default parameters.')
        with open(VERSION_TEMPLATE_PATH, 'r') as config_file:
            version_data = json.load(config_file)
    except OSError as error:
        logger.error('     - Failed to read the contents of version.conf.')
        raise SystemExit from error
    except json.JSONDecodeError as error:
        logger.error('     - Failed to parse the content of version.conf.')
        raise SystemExit from error

    # Bump the build number in regular builds, use the Travis build number if
    # the building is running in Travis CI

    if is_travis():
        logger.debug('     - Build is running in Travis, using Travis build number.')
        try:
            build_num = int(os.environ['TRAVIS_BUILD_NUMBER'])
        except KeyError as error:
            logger.error('     - Travis build number cannot be determined.')
            raise SystemExit from error
    else:
        logger.debug('     - Running local build, bumping existing version number.')
        build_num = int(version_data['meta']['build'])
        build_num = build_num + 1

    # Set the new version number in the version configuration
    version_data['meta']['build'] = str(build_num)
    logger.debug(f'     - New build number is {build_num}.')

    # Set the build type in the version configuration
    if is_travis():
        version_data['meta']['build_type'] = 'CI'
    else:
        version_data['meta']['build_type'] = 'local'

    # Save the version configuration
    try:
        with open(VERSION_FILE_PATH, 'w+') as config_file:
            json.dump(version_data,
                      config_file,
                      indent=4,
                      separators=(',', ': '))
    except OSError as error:
        logger.error('     - Failed to update version.conf.')
        raise SystemExit from error

    logger.debug('Build number has been updated.')
