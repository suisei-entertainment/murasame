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
Contains the implementation of the VFS class.
"""

# Platform Imports
import os
from typing import Any

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils import System
from murasame.logging import LogWriter

class VFS:

    """
    The root class of the Virtual File System.

    Authors:
        Attila Kovacs
    """

    def get(self, key: str, version: 'ContentVersion' = None) -> 'VFSNode':

        """
        Retrieves a VFS node by its key.

        Args:
            key:        The key of the VFS node to retrieve.

        Returns:
            The VFSNode object associated with the given key.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del key
        del version

    def get_content(self, key: str, version: 'ContentVersion' = None) -> Any:

        """
        Retrieves the content of a VFS node by its key.

        Args:
            key:        The key of the VFS node to retrieve.

        Returns:
            The content of the file associated with the VFS key.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del key
        del version

    def register_source(self, path: str) -> None:

        """
        Registers a new VFS data source. This can be a directory or a package.
        All resources from this data source will be added to the VFS tree.

        Args:
            path:       Path to the data source.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del path

@System(VFS)
class DefaultVFS(LogWriter):

    """
    The root class of the Virtual File System.

    Authors:
        Attila Kovacs
    """

    @property
    def Root(self) -> 'VFSNode':

        """
        Provides access to the root node of the VFS.

        Authors:
            Attila Kovacs
        """

        return self._root

    def __init__(self) -> None:

        """
        Creates a new VFS instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name='murasame.vfs', cache_entries=True)

        self._root = None
        """
        The root node of the virtual file system.
        """

        self.info('VFS has been created.')

    def get(self, key: str) -> 'VFSNode':

        """
        Retrieves a VFS node by its key.

        Args:
            key:        The key of the VFS node to retrieve.

        Returns:
            The VFSNode object associated with the given key.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Retrieving VFS node {key}...')

    def get_content(self, key: str, version: 'ContentVersion' = None) -> Any:

        """
        Retrieves the content of a VFS node by its key.

        Args:
            key:        The key of the VFS node to retrieve.

        Returns:
            The content of the file associated with the VFS key.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Retrieving VFS resource {key}({version})...')

    def register_source(self, path: str) -> None:

        """
        Registers a new VFS data source. This can be a directory or a package.
        All resources from this data source will be added to the VFS tree.

        Args:
            path:       Path to the data source.

        Authors:
            Attila Kovacs
        """

        # Normalize path
        path = os.path.abspath(os.path.expanduser(path))

        self.debug(f'Registering {path} as a VFS data source...')

        # Load the source based on its type
        if os.path.isdir(path):
            self._register_directory(path)
        elif os.path.isfile(path):
            self._register_package(path)
        else:
            self.error(
                f'Failed to register VFS data source {path}. A VFS data '
                f'source has to be a directory or a resource package.')
            raise InvalidInputError(
                f'Failed to register VFS data source {path}. A VFS data '
                f'source has to be a directory or a resource package.')

    def _register_directory(self, path: str) -> None:

        """
        Registers a file system directory as a VFS data source.

        Args:
            path:       Path to the directory to add.

        Authors:
            Attila Kovacs
        """

        self.debug(
            'Registering new data source from file system directory...')

    def _register_package(self, path: str) -> None:

        """
        Registers a resource package as a VFS data source.

        Args:
            path:       Path to the package to add.

        Authors:
            Attila Kovacs
        """

        self.debug('Registering new data source from resource package...')
