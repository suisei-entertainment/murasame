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
import tarfile
import uuid

# Dependency Imports
import magic

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.logging import LogWriter
from murasame.utils import SystemLocator, JsonFile

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

        self._extract_directory = None
        """
        Path to a random directory where files from the archive will be
        extracted.
        """

        self._load()

    def _load(self) -> None:

        """
        Loads the resource package.

        Raises:
            InvalidInputError:      Raised if the given path does not
                                    correspond to a tar file.
            InvalidInputError:      Raised if the archive does not contain a
                                    .vfs VFS descriptor file.

        Authors:
            Attila Kovacs
        """

        # Avoiding circular dependency between VFS components
        #pylint: disable=import-outside-toplevel
        from murasame.pal.vfs.vfs import VFS
        from murasame.pal.vfs.vfsnode import VFSNode

        # Check the content type of the file
        content_type = magic.from_file(self._path, mime=True)

        if content_type != 'application/x-tar':
            raise InvalidInputError(f'Resource package {self._path} is not a '
                                    f'gzip compressed archive.')

        # Load the VFS configuration from the package
        tar = tarfile.TarFile(name=self._path)
        descriptor = tar.getmember(name='.vfs')
        if not descriptor:
            raise InvalidInputError(f'Resource package {self._path} does not '
                                    f'contains a VFS descriptor.')

        self._extract_directory = f'/tmp/{uuid.uuid4()}'
        self.debug(f'Random directory for package {self._path} is '
                   f'{self._extract_directory}.')

        tar.extractall(path=self._extract_directory, members=[descriptor])

        descriptor_file = JsonFile(path=f'{self._extract_directory}/.vfs')
        descriptor_file.load()

        # Create the package tree
        node = VFSNode(node_name='ROOT')
        node.deserialize(data=descriptor_file.Content)

        # Merge the package tree into the main VFS tree

        # Pylint can't find the instance() member of the Singleton class
        #pylint: disable=no-member
        vfs = SystemLocator.instance().get_provider(VFS)
        if not vfs:
            raise RuntimeError('Failed to retrieve the virtual file system '
                               'from the system locator.')

        vfs.Root.merge_with(node)
