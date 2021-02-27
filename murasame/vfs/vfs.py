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
import sys
from typing import Any

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils import System, JsonFile
from murasame.logging import LogWriter
from murasame.vfs.vfsnode import VFSNode, VFSNodeTypes
from murasame.vfs.vfsresourcetypes import VFSResourceTypes
from murasame.vfs.vfsresource import VFSResource
from murasame.vfs.vfslocalfile import VFSLocalFile
from murasame.vfs.resourceversion import ResourceVersion

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

        self._root = VFSNode(node_name='', node_type=VFSNodeTypes.DIRECTORY)
        """
        The root node of the virtual file system.
        """

        self.info('VFS has been created.')

    def get_node(self, key: str) -> 'VFSNode':

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
        return self._root.get_node(name=key)

    def get_content(self, key: str, version: 'ContentVersion' = None) -> Any:

        """
        Retrieves the content of a VFS node by its key.

        Args:
            key:        The key of the VFS node to retrieve.

        Returns:
            The content of the file associated with the VFS key, or None if
            it was not found.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Retrieving VFS resource {key}({version})...')

        node = self._root.get_node(name=key)

        if not node:
            self.error(f'Trying to retrieve resource from non-existend '
                       f'VFS node: {key}.')
            return None

        resource = node.get_resource(version=version)

        if not resource:
            self.error(f'There is no resource matching the requested '
                       f'version for {key}(version {version}).')
            return None

        self.debug(f'Found resource for {key}(version {version}).')
        return resource.Resource

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

    def has_node(self, name: str) -> bool:

        """
        Returns whether or not there is a VFS node with a given name in the
        VFS tree.

        Args:
            name:       The name of the node to check for.

        Returns:
            'True' if the there is a node with the given name in the VFS,
            ' False' otherwise.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Checking the existence of node {name}...')

        if '.' not in name:
            # Checking for a root level node
            return self._root.has_node(name)

        # Checking for a non-root level node
        parts = str.split(name, '.', 1)
        if self._root.has_node(parts[0]):
            return self._root.get_node(parts[0]).has_node(parts[1])

        self.debug(f'Node {name} doesn\'t exist in the virtual file system.')
        return False

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

        path = os.path.abspath(os.path.expanduser(path))

        # Abort if the directory doesn't exist
        if not os.path.isdir(path):
            self.warning(
                f'Trying to add a non-existent directory({path}) as a VFS '
                f'data source.')
            return

        # Check if the directory contains a VFS configuration
        vfs_config_file = f'{path}/.vfs'
        if os.path.isfile(vfs_config_file):
            vfs_config = JsonFile(path=vfs_config_file)
            self._load_from_vfs_config(vfs_config=vfs_config.Content)
        else:
            self._load_from_directory_contents(path=path)

    def _register_package(self, path: str) -> None:

        """
        Registers a resource package as a VFS data source.

        Args:
            path:       Path to the package to add.

        Authors:
            Attila Kovacs
        """

        self.debug('Registering new data source from resource package...')

    def _load_from_vfs_config(self, vfs_config: dict) -> None:

        """
        Loads the contents of a VFS data source based on a VFS configuration
        file.

        Args:
            vfs_config:     THe contents of the VFS configuration file.

        Authors:
            Attila Kovcs
        """

        self.debug('Registering directory contents from VFS configuration '
                   'file...')

    def _load_from_directory_contents(self, path: str) -> None:

        """
        Loads the contents of a directory and creates a VFS tree out of it.

        Args:
            path:       Path to the directory to add.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Adding the contents of directory {path} to the VFS...')

        directory_content = os.listdir(path)

        for element in directory_content:
            full_path = f'{path}/{element}'
            if os.path.isdir(full_path):
                self._add_subdirectory_from_directory(element, full_path)
            else:
                self._add_file_from_directory(element, full_path)

        self.debug(f'Contents of directory {path} has been added to VFS.')

    def _add_subdirectory_from_directory(self, name:str, path: str) -> None:

        """
        Adds a new subdirectory node from a file system directory.

        Args:
            name:       The name of the subdirectory to add.
            path:       Path to the subdirectory to add.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Adding subdirectory {name}({path}) under the root node...')

        self._root.add_node(VFSNode(node_name=name))

        self.debug(f'Subdirectory {name} has been added.')

    def _add_file_from_directory(self, name: str, path: str) -> None:

        """
        Adds a new file node from file system directory.

        Args:
            name:       The name of the file to add.
            path:       Path to the file to add.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Adding file {name}({path}) to the root node...')

        # Create a file node based on the file path and mark it as the latest
        # version of that file so it won't be overwritten by anything coming
        # from a resource package.
        node = VFSNode(node_name=name, node_type=VFSNodeTypes.FILE)
        descriptor = VFSLocalFile()
        descriptor.deserialize(data={'path': f'{path}'})
        resource = VFSResource(
            resource_type=VFSResourceTypes.LOCAL_FILE,
            descriptor=descriptor,
            version=ResourceVersion(version=sys.maxsize))
        node.add_resource(resource)

        self._root.add_node(node)

        self.debug(f'File {name} has been added to the root node.')
