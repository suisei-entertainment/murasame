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
Contains various utility functions used for documentation building.
"""

# Runtime Imports
import os
import tarfile
import logging
import subprocess
from typing import Union

# MDE Imports
from mde.constants import (
    MDE_LOGGER_NAME, DOCUMENTATION_SOURCE, DOCUMENTATION_TARGET, DIST_PATH)
from mde.utils.version import get_version_num

def build_documentation() -> None:

    """
    Builds the HTML version of the documentation.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug('Creating documentation...')

    command = \
    [
        'sphinx-build',
        '-E',
        '-a',
        '-b html',
        f'{DOCUMENTATION_SOURCE}',
        f'{DOCUMENTATION_TARGET}'
    ]

    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as error:
        logger.error(f'Failed to create documentation. Reason: {error}')

    logger.debug('Documentation has been created.')

def package_documentation() -> Union[str, None]:

    """
    Creates an archive out of the generated documentation.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug('Packaging documentation...')

    package_path = f'{DIST_PATH}/murasame-{get_version_num()}-documentation.tar.gz'

    with tarfile.open(package_path, 'w:gz') as tar:
        tar.add(DOCUMENTATION_TARGET)

    if not os.path.isfile(package_path):
        logger.error('Failed create archive from documentation.')
        return None

    logger.debug('Documentation packaged.')
    return  package_path