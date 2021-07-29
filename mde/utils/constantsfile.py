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
Contains utility functions for generating the constants file.
"""

# Runtime Imports
import os
import logging
import json
from string import Template

# MDE Imports
from mde.constants import (
    MDE_LOGGER_NAME,
    VERSION_FILE_PATH,
    VERSION_CONSTANTS_PATH,
    VERSION_CONSTANTS_TEMPLATE_PATH)
from mde.git.commit import get_git_commit_hash

def create_constants_file() -> None:

    """Creates the version constants file to be included in the framework.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug('Creating version constants file...')

    # Retrieving version data
    version_data = None
    major_version = None
    minor_version = None
    patch_level = None
    build_num = None
    build_type = None
    release_level = None
    release_codename = None
    scm_id = None

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

    try:
        build_num = version_data['meta']['build']
        logger.debug(f'     - Build: {build_num}')
    except KeyError as error:
        logger.error('     - No build number was found in version.conf')
        raise SystemExit from error

    try:
        build_type = version_data['meta']['build_type']
        logger.debug(f'     - Build type: {build_type}')
    except KeyError as error:
        logger.error('     - No build type was found in version.conf')
        raise SystemExit from error

    try:
        release_level = version_data['release']
        logger.debug(f'     - Release level: {release_level}')
    except KeyError as error:
        logger.error('     - No release level was found in version.conf')
        raise SystemExit from error

    try:
        release_codename = version_data['meta']['codename']
        logger.debug(f'     - Release codename: {release_codename}')
    except KeyError as error:
        logger.error('     - No release codename was found in version.conf')
        raise SystemExit from error

    # Retrieving SCM version
    commit_hash = get_git_commit_hash()
    if commit_hash is None:
        logger.error('Failed to determine the git commit hash.')
        raise SystemExit from error

    logger.debug(f'     - Git commit hash: {scm_id}')

    # Load the constants file template
    template_content = None
    try:
        with open(VERSION_CONSTANTS_TEMPLATE_PATH, 'r') as template_file:
            template_content = template_file.read()
    except OSError as error:
        logger.error('     - Failed to read the contents of version.py.in')
        raise SystemExit from error

    # Create file content
    template = Template(template_content)
    version_content_string = template.safe_substitute(
        major_version=major_version,
        minor_version=minor_version,
        patch_level=patch_level,
        build_num=build_num,
        build_type=build_type,
        release_level=release_level,
        release_codename=release_codename,
        scm_id=scm_id)

    # Write the file
    with open(VERSION_CONSTANTS_PATH, 'w+') as version_file:
        version_file.write(version_content_string)

    logger.debug(' Version constants are added to the framework.')