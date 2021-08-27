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
Contains utility functions related to PyPi releases.
"""

# Runtime Imports
import os
import logging
import subprocess

# MDE Imports
from mde.constants import MDE_LOGGER_NAME, DIST_PATH
from mde.utils.version import get_version_num

def do_pypi_release(arguments: 'argparse.Namespace') -> None:

    """Creates a new release on PyPi.

    Args:
        arguments (argparse.Namespace): The parsed command line arguments.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug('Releasing package on PyPi...')

    # Retrieve username and password
    pypi_username = None
    pypi_password = None
    try:
        pypi_username = os.environ['PYPI_USERNAME']
        logger.debug('PyPi username retrieved from the environment.')

        pypi_password = os.environ['PYPI_PASSWORD']

    except KeyError:
        logger.debug('PyPi username or password is not configured in the '
                     'environment.')

    command = \
    [
        'twine',
        'upload'
    ]

    if arguments.debug_mode:
        command.append('--verbose')

    if arguments.release_draft:
        command.append('-r')
        command.append('testpypi')

    if pypi_username is not None and pypi_password is not None:
        command.append('-u')
        command.append(f'{pypi_username}')
        command.append('-p')
        command.append(f'{pypi_password}')

    command.append(f'{DIST_PATH}/murasame-{get_version_num()}-py3-none-any.whl')

    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as error:
        logger.error('Failed to upload the release to PyPi.')
        raise SystemExit from error

    logger.debug('Package released on PyPi.')
