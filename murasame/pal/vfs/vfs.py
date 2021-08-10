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

# Runtime Imports
import os

from typing import Any

# Murasame Imports
from murasame.constants import MURASAME_VFS_LOG_CHANNEL
from murasame.exceptions import InvalidInputError
from murasame.utils import JsonFile
from murasame.log import LogWriter
from murasame.pal.vfs.vfsnode import VFSNode, VFSNodeTypes
from murasame.pal.vfs.vfspackage import VFSPackage

class VFS(LogWriter):

    """The root class of the Virtual File System.

    Attributes:

        _root (VFSNode): The root node of the virtual file system.

        _packages (dict): Resource packages registered in the virtual file
            system.

    Authors:
        Attila Kovacs
    """

    @property
    def Root(self) -> 'VFSNode':

        """Provides access to the root node of the VFS.

        Authors:
            Attila Kovacs
        """

        return self._root

    @property
    def Packages(self) -> dict:

        """Provides access to the resource packages registered in the virtual
        file system.

        Authors:
            Attila Kovacs
        """

        return self._packages

    def __init__(self) -> None:

        """Creates a new VFS instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_VFS_LOG_CHANNEL,
                         cache_entries=True)

        self._root = VFSNode(node_name='', node_type=VFSNodeTypes.DIRECTORY)
        self._packages = {}

        self.info('VFS has been created.')

    def add_node(self, node: 'VFSNode', parent: str = '') -> None:

        """Adds a new node to the VFS.

        By default the new node will be added to the root node unless a
        different parent node is specified.

        Args:
            node (VFSNode): The node to add.

            parent (str): Name of the parent node to add the new node to.

        Authors:
            Attila Kovacs
        """

        if not node or not isinstance(node, VFSNode):
            self.error('Trying to add an invalid node to the virtual file '
                       'system.')
            return

        self.debug(f'Adding node {node.Name} to the virtual file system...')

        if parent != '':
            self.debug(f'Adding node {node.Name} to parent {parent}...')
            parent = self.get_node(key=parent)
            if not parent:
                self.error(f'The virtual file system doesn\'t have a not with '
                           f'name {parent}, cannot add node {node.Name} under '
                           f'it.')
                return
            parent.add_node(node=node)
        elif self.has_node(name=node.Name):
            self.debug(f'The virtual file system already has a node with name '
                       f'{node.Name}, merging the new node into it.')
            existing_node = self.get_node(key=node.Name)
            existing_node.merge_with(node=node)
        else:
            self.debug(f'Adding node {node.Name} to the root of the virtual '
                       f'file system.')
            self._root.add_node(node=node)

        self.debug(f'Node {node.Name} has been added to the virtual file '
                   f'system.')

    def remove_node(self, node_name: str) -> None:

        """Removes an existing VFS node from the node tree.

        Args:
            node_name (str): Name of the node to remove.

        Authors:
            Attila Kovacs
        """

        self.debug(
            f'Removing node {node_name} from the virtual file system...')

        if not self.has_node(node_name):
            self.debug(f'The virtual file system doesn\'t have a node with '
                       f'name {node_name}.')
            return

        self._root.remove_node(name=node_name)

    def get_node(self, key: str) -> 'VFSNode':

        """Retrieves a VFS node by its key.

        Args:
            key (str): The key of the VFS node to retrieve.

        Returns:
            VFSNode: The VFSNode object associated with the given key.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Retrieving VFS node {key}...')
        return self._root.get_node(name=key)

    def get_content(self, key: str, version: 'ResourceVersion' = None) -> Any:

        """Retrieves the content of a VFS node by its key.

        Args:
            key (str): The key of the VFS node to retrieve.

            version (ResourceVersion): The version of the content to retrieve.

        Returns:
            Any: The content of the file associated with the VFS key, or None
                if it was not found.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Retrieving VFS resource {key}({version})...')

        node = self._root.get_node(name=key)

        if not node:
            self.error(f'Trying to retrieve resource from non-existent '
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

        """Registers a new VFS data source. This can be a directory or a
        package.

        All resources from this data source will be added to the VFS tree.

        Args:
            path (str): Path to the data source.

        Raises:
            InvalidInputError: Raised when trying to add an invalid data source.

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

        """Returns whether or not there is a VFS node with a given name in the
        VFS tree.

        Args:
            name (str): The name of the node to check for.

        Returns:
            bool: 'True' if the there is a node with the given name in the VFS,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Checking the existence of node {name}...')

        if not self._root:
            self.debug(f'Node {name} doesn\'t exist in the virtual file '
                       f'system.')
            return False

        return  self._root.has_node(name=name)

    def get_all_files(
            self,
            node_name: str,
            recursive: bool = False,
            filename_filter: str = None) -> list:

        """Returns a list of all VFS file nodes under a given directory node.

        Args:
            node_name (str): The name of the VFS node to retrieve the files
                from.

            recursive (bool): Whether or not files in subdirectories should
                be returned as well.

            filename_filter (str): Optional filter string to only include files
                in the result list that match the given filter.

        Returns:
            list: A list of VFS file nodes.

        Authors:
            Attila Kovacs
        """

        if recursive:
            self.debug(f'Retrieving all file nodes from VFS directory node '
                       f'{node_name} and subdirectories...')
        else:
            self.debug(f'Retrieving all file nodes from VFS directory node '
                       f'{node_name}...')

        if not self._root:
            self.error(f'Node {node_name} doesn\'t exist in the virtual file '
                       f'system.')
            return []

        # Just return an empty list if the requested directory node doesn't
        #  exist, or it's not a directory node.
        if not self._root.has_node(name=node_name):
            self.error(f'Node {node_name} doesn\'t exist in the virtual file '
                       f'system.')
            return []

        node = self._root.get_node(name=node_name)
        if node.Type != VFSNodeTypes.DIRECTORY:
            self.error(f'Node {node_name} is not a directory node.')
            return  []

        return node.get_all_files(recursive=recursive,
                                  filename_filter=filename_filter)

    def _register_directory(self, path: str) -> None:

        """Registers a file system directory as a VFS data source.

        Args:
            path (str): Path to the directory to add.

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

        """Registers a resource package as a VFS data source.

        Args:
            path (str): Path to the package to add.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Registering new data source from resource package '
                   f'{path}...')

        package = VFSPackage(path=path)
        self._packages[package.Path] = package

    def _load_from_vfs_config(self, vfs_config: dict) -> None:

        """Loads the contents of a VFS data source based on a VFS configuration
        file.

        Args:
            vfs_config (dict): The contents of the VFS configuration file.

        Authors:
            Attila Kovacs
        """

        self.debug('Registering directory contents from VFS configuration '
                   'file...')

        self._root.deserialize(vfs_config)

    def _load_from_directory_contents(self, path: str) -> None:

        """Loads the contents of a directory and creates a VFS tree out of it.

        Args:
            path (str): Path to the directory to add.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Adding the contents of directory {path} to the VFS...')
        self._root.populate_from_directory(path=path)
        self.debug(f'Contents of directory {path} has been added to VFS.')
