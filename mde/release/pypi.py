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

    command.append(f'{DIST_PATH}/murasame-{get_version_num()}-py3-none-any.whl')

    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as error:
        logger.error('Failed to upload the release to PyPi.')
        raise SystemExit from error

    logger.debug('Package released on PyPi.')
