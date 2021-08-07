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
Contains the implementation of the PackageFileDescriptor class.
"""

# Murasame Imports
from murasame.log import LogWriter

class PackageFileDescriptor(LogWriter):

    """Contains the description of a single package file.

    Attributes:
        _path (str): Path to the package file in the file system.

        _version (ResourceVersion): Version of the package file.

    Authors:
        Attila Kovacs
    """

    @property
    def Path(self) -> str:

        """Path to the package file in the file system.

        Authors:
            Attila Kovacs
        """

        return self._path

    @property
    def Version(self) -> 'ResourceVersion':

        """Version of the package file.

        Authors:
            Attila Kovacs
        """

        return self._version

    def __init__(self, path: str) -> None:

        """Creates a new PackageFileDescriptor instance.

        Args:
            path (str): Path to the package file in the file system.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name='murasame.pal.vfs', cache_entries=True)

        self._path = path
        self._version = None
