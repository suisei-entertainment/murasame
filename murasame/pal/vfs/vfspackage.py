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
Contains the implementation of the VFSPackage class.
"""

# Runtime Imports
import os

# Dependency Imports
import magic

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.logging import LogWriter

class VFSPackage(LogWriter):

    """
    Represents a single VFS resource package.

    Authors:
        Attila Kovacs
    """

    @property
    def Path(self) -> str:

        """
        Path to the resource package in the file system.

        Authors:
            Attila Kovacs
        """

        return  self._path

    @property
    def Content(self) -> 'VFSNode':

        """
        Provides access to the content of the package.

        Authors:
            Attila Kovacs
        """

        return self._content

    def __init__(self, path: str) -> None:

        """
        Creates a new VFSPackage instance.

        Args:
            path:       Path to the resource package in the file system.

        Raises:
            InvalidInputError:      Raised when the package file doesn't exist.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name='murasame.pal.vfs', cache_entries=True)

        if not os.path.isfile(path):
            raise InvalidInputError(f'Resource package {path} doesn\'t exist.')

        self._path = os.path.abspath(os.path.expanduser(path))
        """
        Path to the resource package in the file system.
        """

        self._content = None
        """
        The content of the resource package.
        """

        self._load()

    def _load(self) -> None:

        """
        Loads the resource package.

        Authors:
            Attila Kovacs
        """

        # Check the content type of the file
        content_type = magic.from_file(self._path, mime=True)

        if content_type != 'application/x-tar':
            raise InvalidInputError(f'Resource package {self._path} is not a '
                                    f'gzip compressed archive.')

