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
Contains the implementation of the VFSNode class.
"""

# Runtime Imports
import os
import sys
from enum import IntEnum
from typing import Union

# Murasame Imports
from murasame.logging import LogWriter
from murasame.exceptions import InvalidInputError
from murasame.vfs.vfsresource import VFSResource
from murasame.vfs.vfsresourcetypes import VFSResourceTypes
from murasame.vfs.vfslocalfile import VFSLocalFile
from murasame.vfs.resourceversion import ResourceVersion

class VFSNodeTypes(IntEnum):

    """
    List of supported VFS node types.

    Authors:
        Attila Kovacs
    """

    UNKNOWN = 0 # Unknown node type
    FILE = 1 # File node
    DIRECTORY = 2 # Directory node

class VFSNode(LogWriter):

    """
    Represents a single VFS node in the virtual file system. A node either
    represents a directory or all versions of a VFS resource.

    Authors:
        Attila Kovacs
    """

    # Pylint with Python 3.9 seems to trigger a false positive thinking the
    # Union type is unsubscriptable., so disable that check here for now.
    #pylint: disable=unsubscriptable-object

    @property
    def Type(self) -> VFSNodeTypes:

        """
        Type of the node.

        Authors:
            Attila Kovacs
        """

        return self._type

    @property
    def Name(self) -> str:

        """
        The name of the node.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def Subdirectories(self) -> dict:

        """
        All subdirectory nodes of this node.

        Authors:
            Attila Kovacs
        """

        return self._directories

    @property
    def Files(self) -> dict:

        """
        All file nodes of this node.

        Authors:
            Attila Kovacs
        """

        return self._files

    @property
    def Resources(self) -> list:

        """
        List of all resources attached to this node.

        Authors:
            Attila Kovacs
        """

        return self._resources

    @property
    def Latest(self) -> Union[VFSResource, None]:

        """
        Provides access to the latest resource attached to this node according
        to its resource version.

        Authors:
            Attila Kovacs
        """

        if self._resources:
            return self._resources[0]

        return None

    def __init__(self,
                 node_name: str,
                 node_type: 'VFSNodeTypes'= VFSNodeTypes.DIRECTORY) -> None:

        """
        Creates a new VFSNode instance.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name='murasame.vfs', cache_entries=True)

        # Root node can only be a directory node
        if node_name == '' and node_type == VFSNodeTypes.FILE:
            raise InvalidInputError(
                'The root VFS node can only be a directory node.')

        # Set a predefined name for the root node

        self._type = node_type
        """
        THe type of the node.
        """

        self._name = node_name if node_name != '' else 'ROOT'
        """
        The name of the node.
        """

        self._directories = {}
        """
        All subdirectories of this node.
        """

        self._files = {}
        """
        All file nodes of this node.
        """

        self._resources = []
        """
        The actual resources attached to the node.
        """

    def isdir(self) -> bool:

        """
        Returns whether or not the node represents a directory node.

        Returns:
            'True' if the node represents a directrory, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        return self._type == VFSNodeTypes.DIRECTORY

    def isfile(self) -> bool:

        """
        Returns whether or not the node represents a file node.

        Returns:
            'True' if the node represents a file, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        return self._type == VFSNodeTypes.FILE

    def isroot(self) -> bool:

        """
        Returns whether or not the node represents the root of the VFS tree.

        Returns:
            'True' if the node represents the root of the VFS tree, 'False'
            otherwise.

        Authors:
            Attila Kovacs
        """

        return self._name == 'ROOT'

    def has_node(self, name: str) -> bool:

        """
        Returns whether or not this VFS node contains a child with the given
        name.

        Args:
            name:       Name of the child node to check.

        Returns:
            'True' if the node has a child with the given name, 'False'
            otherwise.

        Authors:
            Attila Kovacs
        """

        if '.' in name:
            # Looking for a node attached to a child node

            # Find parent
            parts = str.split(name, '.', 1)
            try:
                parent = self._directories[parts[0]]
                return parent.has_node(parts[1])
            except KeyError:
                return False

        elif name in self._directories or name in self._files:
            # Looking for a node directly attached to this node
            return True

        return False

    def add_node(self, node: 'VFSNode') -> None:

        """
        Adds a new VFS child node to this node.

        Args:
            node:       The node to add.

        Authors:
            Attila Kovacs
        """

        if not node:
            self.error(f'Trying to add an invalid child node to VFS '
                       f'node {self.Name}')
            return

        if self.has_node(node.Name):
            self.debug(f'Node {self.Name} already has a child with name '
                       f'{node.Name}, attempting to merge...')
            self.get_node(node.Name).merge_with(node)
        elif node.Type == VFSNodeTypes.DIRECTORY:
            self.debug(f'Adding new subdirectory node {node.Name} to '
                       f'node {self.Name}.')
            self._directories[node.Name] = node
        else:
            self.debug(f'Adding new file node {node.Name} to '
                       f'node {self.Name}.')
            self._files[node.Name] = node

    def remove_node(self, name: str) -> None:

        """
        Removes a child node with the given name.

        Args:
            name:       The name of the node to remove.
        """

        self.debug(f'Removing child node {name} from node {self.Name}...')

        if not self.has_node(name=name):
            self.debug(f'Node {self.Name} doesn\'t have a child node named '
                       f'{name}, nothing to remove.')
            return

        if name in self._directories:
            self.remove_subdirectory(name=name)
        else:
            self.remove_file(name=name)

    def remove_subdirectory(self, name: str) -> None:

        """
        Removes a subdirectory with the given name.

        Args:
            name:       Name of the subdirectory to remove.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Removing subdirectory {name} from node {self.Name}...')

        try:
            del self._directories[name]
            self.debug(f'Subdirectory {name} has been deleted from node '
                       f'{self.Name}.')
        except KeyError:
            self.debug(f'Node {self.Name} doesn\'t have a subdirectory named '
                      f'{name}, nothing to do.')

    def remove_file(self, name: str) -> None:

        """
        Removes a file wit the given name.

        Args:
            name:       The name of the file to remove.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Removing file {name} from node {self.Name}...')

        try:
            del self._files[name]
            self.debug(f'File {name} has been deleted from node {self.Name}.')
        except KeyError:
            self.debug(f'Node {self.Name} doesn\'t have a file named {name}, '
                       f'nothing to do.')

    def get_node(self, name: str) -> Union['VFSNode', None]:

        """
        Returns a child of this node.

        Args:
            name:       The name of the child node to retrieve.

        Returns:
            The child node, or 'None' if it doesn't exist.

        Authors:
            Attila Kovacs
        """

        # Looking for a node attached to a child node
        if '.' in name:
            parts = str.split(name, '.', 1)
            parent = self._directories[parts[0]]
            return parent.get_node(parts[1])

        # Looking for a node directly attached to this one.
        if name in self._directories:
            return self._directories[name]

        if name in self._files:
            return self._files[name]

        return None

    def merge_with(self, node: 'VFSNode') -> None:

        """
        Merges the other VFS node into this one.

        Args:
            node:       The VFS node to merge into this one.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Attempting to merge {node.Name} into {self.Name}...')

        if self.Type != node.Type:
            self.error(f'The type of {node.Name} doesn\'t match the type of '
                       f'{self.Name}, they cannot be merged.')
            raise InvalidInputError(
                f'Trying to merge two VFS nodes with different types.')

        if self.Type == VFSNodeTypes.FILE:
            self.debug(
                f'Merging resources from {node.Name} into {self.Name}...')
            for dummy, resource in node.Resources.items():
                self.add_resource(resource)
        else:
            self.debug(
                f'Merging subdirectories from {node.Name} into {self.Name}...')
            for dummy, directory in node.Subdirectories.items():
                self.add_node(directory)
            self.debug(
                f'Merging files from {node.Name} into {self.Name}...')
            for dummy, file in node.Files.items():
                self.add_node(file)

        self.debug(f'{node.Name} has been merged into {self.Name}.')

    def get_resource(self, version: int = None) -> Union[VFSResource, None]:

        """
        Returns the resource stored in the node.

        Args:
            version:        The version of the resource to retrieve. If no
                            version is provided, the latest version will be
                            returned.

        Returns:
            The VFS resource object matching the requested version, or None
            if it was not found.

        Authors:
            Attila Kovacs
        """

        # No resource is stored in a directory node.
        if self._type == VFSNodeTypes.DIRECTORY:
            return None

        # Return the latest version if no specific version is requested
        if not version:
            return self.Latest

        # Try to find the requested resource version
        for resource in self._resources:
            if resource.Version == version:
                return resource

        return None

    def has_resource(self, version: int) -> bool:

        """
        Returns whether or not the node contains a resource with the given
        resource version.

        Args:
            version:        The resource version to check.

        Returns:
            'True' if the requested resource version is found, 'False'
            otherwise.

        Authors:
            Attila Kovacs
        """

        resource = self.get_resource(version=version)
        if resource:
            return True

        return False

    def add_resource(
        self,
        resource: 'VFSResource',
        skip_sorting: bool=False) -> None:

        """
        Adds a new resource to the VFS node.

        Args:
            resource:       The resource to add.
            skip_sorting:   Do not sort the resource list after adding the
                            resource. Useful when adding multiple resources to
                            the same node. Only the last add_resource() call
                            should trigger a sort to improve performance.

        Authors:
            Attila Kovacs
        """

        # Directory nodes doesn't have resources
        if self._type == VFSNodeTypes.DIRECTORY:
            return

        # Do not add a resource with the same version twice
        if not self.has_resource(version=resource.Version):
            return

        # Add the resource and sort the list
        self._resources.append(resource)

        # Sort the resource list to have the one with the highest version
        # number at the front of the list.
        if not skip_sorting:
            self._resources.sort(key=lambda x: x.Version,
                             reverse=True)

    def remove_resource(self, version: int = None) -> None:

        """
        Removes a resource with the given version from the resource list.

        Args:
            version:        The version of the resource to remove.

        Authors:
            Attila Kovacs
        """

        resource = self.get_resource(version=version)
        if resource:
            self._resources.remove(resource)

    def serialize(self) -> dict:

        """
        Serializes the content of the VFS node into a dictionary.

        Returns:
            The content of the node as a dictionary.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Serializing VFS node {self.Name}...')

        result = {}
        result['name'] = self.Name

        if self.Type == VFSNodeTypes.DIRECTORY:

            # Serialize the node as a directory
            result['type'] = 'directory'

            # Serialize all subdirectories
            subdirectories = {}

            for dummy, subdirectory in self._directories.items():
                subdirectories[subdirectory.Name] = subdirectory.serialize()

            result['subdirectories'] = subdirectories

            # Serialize all files
            files = {}

            for dummy, file in self._files.items():
                files[file.Name] = file.serialize()

            result['files'] = files

        else:

            # Serialize the node as a file
            result['type'] = 'file'

            resources = {}

            for dummy, resource in self._resources:
                resources[resource.Name] = resource.Descriptor.serialize()

            result['resources'] = resources

        self.debug(f'Node {self.Name} has been serialized.')
        self.trace(f'Node {self.Name}: {result}')

        return result

    def deserialize(self, data: dict) -> None:

        """
        Loads the content of the node from its serialized format.

        Args:
            data:       The dictionary containing the serialized node data.

        Authors:
            Attila Kovacs
        """

        return

    def populate_from_directory(self, path: str) -> None:

        """
        Populates this VFS node with the contents of the given directory.

        Args:
            path:       Path to the directory to use as source.

        Authors:
            Attila Kovacs
        """

        directory_content = os.listdir(path)

        for element in directory_content:
            full_path = f'{path}/{element}'
            if os.path.isdir(full_path):
                self._add_subdirectory_from_directory(element, full_path)
            else:
                self._add_file_from_directory(element, full_path)

    def _add_subdirectory_from_directory(self, name:str, path: str) -> None:

        """
        Adds a new subdirectory node from a file system directory.

        Args:
            name:       The name of the subdirectory to add.
            path:       Path to the subdirectory to add.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Adding subdirectory {name}({path}) under node '
                   f'{self.Name}...')

        node = VFSNode(node_name=name)
        node.populate_from_directory(path=path)
        self.add_node(node)
        self.debug(f'Subdirectory {name} has been added to node {self.Name}.')

    def _add_file_from_directory(self, name: str, path: str) -> None:

        """
        Adds a new file node from file system directory.

        Args:
            name:       The name of the file to add.
            path:       Path to the file to add.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Adding file {name}({path}) to node {self.Name}...')

        # Create a file node based on the file path and mark it as the latest
        # version of that file so it won't be overwritten by anything coming
        # from a resource package.
        node = VFSNode(node_name=name, node_type=VFSNodeTypes.FILE)
        descriptor = VFSLocalFile()
        descriptor.deserialize(data={'type': 'localfile', 'path': f'{path}'})
        resource = VFSResource(
            resource_type=VFSResourceTypes.LOCAL_FILE,
            descriptor=descriptor,
            version=ResourceVersion(version=sys.maxsize))
        node.add_resource(resource)

        self.add_node(node)

        self.debug(f'File {name} has been added to node {self.Name}.')
