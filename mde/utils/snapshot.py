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
Contains utility functions used for creating snapshots of the repository.
"""

# Runtime Imports
import os
import tarfile
import logging

from typing import Union

# MDE Imports
from mde.constants import DIST_PATH, MDE_LOGGER_NAME
from mde.utils.version import get_version_num

def create_snapshot() -> Union[str, None]:

    """Creates a snapshot of the repository and saves it as a tar.gz archive.

    Returns:
        str: Path to the archive.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug('Creating snapshot of current repository state...')

    root_path = os.getcwd()
    archive_path = f'{DIST_PATH}/murasame-{get_version_num()}.tar.gz'

    with tarfile.open(archive_path, 'w:gz') as tar:
        tar.add(root_path)

    if not os.path.isfile(archive_path):
        logger.error(
            f'Failed to create repository snapshot in {archive_path}.')
        return None

    logger.debug(f'Snapshot created as {archive_path}.')

    return archive_path