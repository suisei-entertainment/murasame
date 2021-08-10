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
import shutil

# Dependency Imports
import magic

# Murasame Imports
from murasame.constants import MURASAME_VFS_LOG_CHANNEL
from murasame.exceptions import InvalidInputError
from murasame.log import LogWriter
from murasame.utils import SystemLocator, JsonFile

class VFSPackage(LogWriter):

    """Represents a single VFS resource package.

    Attributes:
        _path (str): Path to the resource package in the file system.

        _extract_directory (str): Path to a random directory where files from
            the archive will be extracted.

    Authors:
        Attila Kovacs
    """

    @property
    def Path(self) -> str:

        """Path to the resource package in the file system.

        Authors:
            Attila Kovacs
        """

        return  self._path

    def __init__(self, path: str) -> None:

        """Creates a new VFSPackage instance.

        Args:
            path (str): Path to the resource package in the file system.

        Raises:
            InvalidInputError: Raised when the package file doesn't exist.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_VFS_LOG_CHANNEL,
                                      cache_entries=True)

        if not os.path.isfile(path):
            raise InvalidInputError(f'Resource package {path} doesn\'t exist.')

        self._path = os.path.abspath(os.path.expanduser(path))
        self._extract_directory = None

        self._load()

    def __del__(self) -> None:

        """Destructor.

        Authors:
            Attila Kovacs
        """

        # Make sure that the temp directory is deleted
        if os.path.isdir(self._extract_directory):
            shutil.rmtree(self._extract_directory)

    def _load(self) -> None:

        """Loads the resource package.

        Raises:
            InvalidInputError: Raised if the given path does not correspond to
                a tar file.

            InvalidInputError: Raised if the archive does not contain a .vfs
                VFS descriptor file.

        Authors:
            Attila Kovacs
        """

        # Avoiding circular dependency between VFS components
        #pylint: disable=import-outside-toplevel
        from murasame.api import VFSAPI
        from murasame.pal.vfs.vfsnode import VFSNode

        # Check the content type of the file
        content_type = magic.from_file(self._path, mime=True)

        if content_type != 'application/x-tar':
            raise InvalidInputError(f'Resource package {self._path} is not a '
                                    f'gzip compressed archive.')

        # Load the VFS configuration from the package
        with  tarfile.TarFile(name=self._path) as tar:
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
        node.deserialize(
            data=self._inject_package_path(descriptor_file.Content))

        # Merge the package tree into the main VFS tree

        # Pylint can't find the instance() member of the Singleton class
        #pylint: disable=no-member
        vfs = SystemLocator.instance().get_provider(VFSAPI)
        if not vfs:
            raise RuntimeError('Failed to retrieve the virtual file system '
                               'from the system locator.')

        vfs.Root.merge_with(node)

    def _inject_package_path(self, descriptor: dict) -> dict:

        """Injects the real path to the resource package into the resource
        descriptor.

        Args:
            descriptor (dict): The vfs package descriptor to inject the path
                into.

        Returns:
            dict: The modified package descriptor that now contains the real
                path to the resource package.

        Authors:
            Attila Kovacs
        """

        descriptor['package_path'] = self._path
        descriptor = self._inject_path_to_subdirectories(descriptor=descriptor)
        descriptor = self._inject_path_to_files(descriptor=descriptor)
        return  descriptor

    def _inject_path_to_subdirectories(self, descriptor: dict) -> dict:

        """Inject the real path of the resource package to all subdirectories
            of the resource package.

        Args:
            descriptor (dict): The descriptor to inject the path into.

        Returns:
            dict: The modified package descriptor.

        Authors:
            Attila Kovacs
        """

        subdirectories = None

        try:
            subdirectories = descriptor['subdirectories']
        except KeyError:
            subdirectories = {}

        for dummy, subdirectory in subdirectories.items():
            subdirectory = self._inject_path_to_subdirectories(
                descriptor=subdirectory)
            subdirectory = self._inject_path_to_files(descriptor=subdirectory)

        return descriptor

    def _inject_path_to_files(self, descriptor: dict) -> dict:

        """Inject the real path of the resource package to all resource files
            of the resource package.

        Args:
            descriptor (dict): The descriptor to inject the path into.

        Returns:
            The modified package descriptor.

        Authors:
            Attila Kovacs
        """

        files = None

        try:
            files = descriptor['files']
        except KeyError:
            files = {}

        for dummy, file in files.items():
            file['resource'][0]['descriptor']['package_path'] = self._path

        return descriptor
