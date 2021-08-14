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
from enum import IntEnum
from typing import Union

# Murasame Imports
from murasame.constants import MURASAME_VFS_LOG_CHANNEL
from murasame.log import LogWriter
from murasame.exceptions import InvalidInputError
from murasame.pal.vfs.vfsresource import VFSResource
from murasame.pal.vfs.vfslocalfile import VFSLocalFile
from murasame.pal.vfs.vfspackagefile import VFSPackageFile
from murasame.pal.vfs.resourceversion import ResourceVersion

class VFSNodeTypes(IntEnum):

    """List of supported VFS node types.

    Attributes:
        UNKNOWN: Unknown node type
        FILE: File node
        DIRECTORY: Directory node

    Authors:
        Attila Kovacs
    """

    UNKNOWN = 0 # Unknown node type
    FILE = 1 # File node
    DIRECTORY = 2 # Directory node

class VFSNode(LogWriter):

    """Represents a single VFS node in the virtual file system.

    A node either represents a directory or all versions of a VFS resource.

    Attributes:
        _type (VFSNodeTypes): The type of the node.

        _name (str): The name of the node.

        _directories (dict): All subdirectories of this node.

        _files (dict): All file nodes of this node.

        _resources (list): The actual resources attached to the node.

    Authors:
        Attila Kovacs
    """

    # Pylint with Python 3.9 seems to trigger a false positive thinking the
    # Union type is unsubscriptable., so disable that check here for now.
    #pylint: disable=unsubscriptable-object

    @property
    def Type(self) -> VFSNodeTypes:

        """Type of the node.

        Authors:
            Attila Kovacs
        """

        return self._type

    @property
    def Name(self) -> str:

        """The name of the node.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def Subdirectories(self) -> dict:

        """All subdirectory nodes of this node.

        Authors:
            Attila Kovacs
        """

        return self._directories

    @property
    def Files(self) -> dict:

        """All file nodes of this node.

        Authors:
            Attila Kovacs
        """

        return self._files

    @property
    def Resources(self) -> list:

        """List of all resources attached to this node.

        Authors:
            Attila Kovacs
        """

        return self._resources

    @property
    def Latest(self) -> Union[VFSResource, None]:

        """Provides access to the latest resource attached to this node
        according to its resource version.

        Authors:
            Attila Kovacs
        """

        if self._resources:
            return self._resources[0]

        return None

    @property
    def NumResources(self) -> int:

        """The amount of resources contained in this node.

        Authors:
            Attila Kovacs
        """

        return len(self._resources)

    def __init__(self,
                 node_name: str,
                 node_type: 'VFSNodeTypes'= VFSNodeTypes.DIRECTORY) -> None:

        """Creates a new VFSNode instance.

        Args:
            node_name (str): Name of the node.

            node_type (VFSNodeTypes): The type of the node.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_VFS_LOG_CHANNEL,
                         cache_entries=True)

        # Root node can only be a directory node
        if node_name == '' and node_type == VFSNodeTypes.FILE:
            raise InvalidInputError(
                'The root VFS node can only be a directory node.')

        # Set a predefined name for the root node

        self._type = node_type
        self._name = node_name if node_name != '' else 'ROOT'
        self._directories = {}
        self._files = {}
        self._resources = []

    def __del__(self) -> None:

        """Destroys the VFSNode instance.

        Authors:
            Attila Kovacs
        """

        self.reset()
        del self._name
        del self._type

    def reset(self) -> None:

        """Allows resetting the node to initial state.

        This function will not change the name or the type of the node, it
        will only clean any resources or child nodes from it.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Resetting node {self.Name}...')

        self.remove_all_subdirectories()
        self.remove_all_files()
        self.remove_all_resources()

        self.debug(f'Reset of node {self.Name} was completed.')

    def is_dir(self) -> bool:

        """Returns whether or not the node represents a directory node.

        Returns:
            bool: 'True' if the node represents a directory, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        return self._type == VFSNodeTypes.DIRECTORY

    def is_file(self) -> bool:

        """Returns whether or not the node represents a file node.

        Returns:
            bool: 'True' if the node represents a file, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        return self._type == VFSNodeTypes.FILE

    def is_root(self) -> bool:

        """Returns whether or not the node represents the root of the VFS tree.

        Returns:
            bool: 'True' if the node represents the root of the VFS tree,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        return self._name == 'ROOT'

    def has_node(self, name: str) -> bool:

        """Returns whether or not this VFS node contains a child with the given
        name.

        Args:
            name (str): Name of the child node to check.

        Returns:
            bool: 'True' if the node has a child with the given name, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        # Remove starting /
        if name.startswith('/'):
            name = name[1:]

        if '/' in name:
            # Looking for a node attached to a child node

            # Find parent
            parts = str.split(name, '/', 1)
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

        """Adds a new VFS child node to this node.

        Args:
            node (VFSNode): The node to add.

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

        """Removes a child node with the given name.

        Args:
            name (str): The name of the node to remove.

        Authors:
            Attila Kovacs
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

        """Removes a subdirectory with the given name.

        Args:
            name (str): Name of the subdirectory to remove.

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

    def remove_all_subdirectories(self) -> None:

        """Removes all subdirectories from this node.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Removing all directory nodes from node {self.Name}...')

        del self._directories
        self._directories = {}

        self.debug(
            f'All directory nodes has been removed from node {self.Name}.')

    def remove_file(self, name: str) -> None:

        """Removes a file wit the given name.

        Args:
            name (str): The name of the file to remove.

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

    def remove_all_files(self) -> None:

        """Removes all files from the node.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Removing all file nodes from node {self.Name}...')

        del self._files
        self._files = {}

        self.debug(f'All file nodes has been removed from node {self.Name}.')

    def get_node(self, name: str) -> Union['VFSNode', None]:

        """Returns a child of this node.

        Args:
            name (str): The name of the child node to retrieve.

        Returns:
            Union[VFSNode, None]: The child node, or 'None' if it doesn't exist.

        Authors:
            Attila Kovacs
        """

        # Strip the starting /
        if name.startswith('/'):
            name=name[1:]

        # Looking for a node attached to a child node
        if '/' in name:
            parts = str.split(name, '/', 1)
            parent = self._directories[parts[0]]
            return parent.get_node(parts[1])

        # Looking for a node directly attached to this one.
        if name in self._directories:
            return self._directories[name]

        if name in self._files:
            return self._files[name]

        return None

    def merge_with(self, node: 'VFSNode') -> None:

        """Merges the other VFS node into this one.

        Args:
            node (VFSNode): The VFS node to merge into this one.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Attempting to merge {node.Name} into {self.Name}...')

        if self.Type != node.Type:
            self.error(f'The type of {node.Name} doesn\'t match the type of '
                       f'{self.Name}, they cannot be merged.')
            raise InvalidInputError(
                'Trying to merge two VFS nodes with different types.')

        if self.Type == VFSNodeTypes.FILE:
            self.debug(
                f'Merging resources from {node.Name} into {self.Name}...')
            for resource in node.Resources:
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

    def get_resource(
        self,
        version: Union[int, None] = None) -> Union[VFSResource, None]:

        """Returns the resource stored in the node.

        Args:
            version (Union[int, None]): The version of the resource to
                retrieve. If no version is provided, the latest version will be
                returned.

        Returns:
            Union[VFSResource, None]: The VFS resource object matching the
                requested version, or 'None' if it was not found.

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
            if resource.Version.Version == version:
                return resource

        return None

    def has_resource(self, version: int) -> bool:

        """Returns whether or not the node contains a resource with the given
        resource version.

        Args:
            version (int): The resource version to check.

        Returns:
            bool: 'True' if the requested resource version is found, 'False'
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
        skip_sorting: bool = False) -> None:

        """Adds a new resource to the VFS node.

        Args:
            resource (VFSResource): The resource to add.

            skip_sorting (bool): Do not sort the resource list after adding the
                resource. Useful when adding multiple resources to the same
                node. Only the last add_resource() call should trigger a sort
                to improve performance.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Adding new resource to VFS node {self.Name}...')
        self.trace(f'VFS resource: {resource.Descriptor}')

        # Directory nodes don't have resources
        if self._type == VFSNodeTypes.DIRECTORY:
            self.error(f'Directory node {self.Name} cannot have resources.')
            return

        # Do not add a resource with the same version twice
        if self._resources and self.has_resource(version=resource.Version.Version):
            self.warning(f'Node {self.Name} already has a resource with the '
                         f'given version.')
            return

        # Add the resource and sort the list
        self._resources.append(resource)

        # Sort the resource list to have the one with the highest version
        # number at the front of the list.
        if not skip_sorting:
            self._resources.sort(key=lambda x: x.Version,
                             reverse=True)

        self.debug(f'New VFS resource has been added to node {self.Name}.')

    def remove_resource(self, version: int = None) -> None:

        """Removes a resource with the given version from the resource list.

        Args:
            version (int): The version of the resource to remove.

        Authors:
            Attila Kovacs
        """

        self.debug(
            f'Removing resource version {version} from node {self.Name}...')

        resource = self.get_resource(version=version)
        if resource:
            self._resources.remove(resource)
            self.debug(f'Resource v{version} was removed from {self.Name}.')
        else:
            self.debug(f'Node {self.Name} doesn\'t have a resource with '
                       f'version {version}, nothing to remove.')

    def remove_all_resources(self) -> None:

        """Removes all resources from the node.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Removing all resources from node {self.Name}...')

        del self._resources
        self._resources = []

        self.debug(f'All resources removed from node {self.Name}.')

    def serialize(self) -> dict:

        """Serializes the content of the VFS node into a dictionary.

        Returns:
            dict: The content of the node as a dictionary.

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

            resources = []

            for resource in self._resources:
                resources.append(resource.Descriptor.serialize())

            result['resource'] = resources

        self.debug(f'Node {self.Name} has been serialized.')
        self.trace(f'Node {self.Name}: {result}')

        return result

    def deserialize(self, data: dict) -> None:

        """Loads the content of the node from its serialized format.

        Args:
            data (dict): The dictionary containing the serialized node data.

        Authors:
            Attila Kovacs
        """

        self.debug('Deserializing node...')
        self.trace(f'Data: {data}')

        if not isinstance(data, dict):
            raise InvalidInputError('Trying to deserialize invalid data.')

        # Reset the node before loading the new content
        self.reset()

        # Retrieve node name
        try:
            self._name = data['name']
        except KeyError as error:
            raise InvalidInputError(
                'Node name was not found in the serialized data.') from error

        # Retrieve node type
        node_type = None
        try:
            node_type = data['type']
        except KeyError as error:
            raise InvalidInputError(
                'Node type was not found in the serialized data.') from error

        if node_type == 'directory':

            self.debug(f'Deserializing {self.Name} as a directory node...')
            self._type = VFSNodeTypes.DIRECTORY

            subdirectories = None
            files = None

            # Retrieve subdirectories
            try:
                subdirectories = data['subdirectories']
            except KeyError:
                self.debug(f'No subdirectories found for {self.Name}.')

            for name, subdirectory in subdirectories.items():
                node = VFSNode(node_name=name)
                node.deserialize(data=subdirectory)
                self.add_node(node)

            # Retrieve files
            try:
                files = data['files']
            except KeyError:
                self.debug(f'No files found for {self.Name}.')

            for name, file in files.items():
                node = VFSNode(node_name=name)
                node.deserialize(data=file)
                self.add_node(node)

        else:

            self.debug(f'Deserializing {self.Name} as a file node...')
            self._type = VFSNodeTypes.FILE

            resources = None

            # Retrieve resources
            try:
                resources = data['resource']
            except KeyError:
                self.debug(f'No resources found for {self.Name}.')

            for resource in resources:
                try:
                    resource_type = resource['descriptor']['type']
                except KeyError as error:
                    raise InvalidInputError(
                        'The resource does not specify the type.') from error

                res = None
                if resource_type == 'localfile':
                    res = VFSResource(descriptor=VFSLocalFile(),
                                      data=resource)
                elif resource_type == 'packagefile':
                    res = VFSResource(descriptor=VFSPackageFile(),
                                      data=resource)

                self.add_resource(res)

        self.debug(f'Node deserialization complete for {self.Name}.')

    def get_all_files(
            self,
            recursive: bool = False,
            filename_filter: str = None) -> list:

        """Returns a list of all VFS file nodes under this node.

        Args:
            recursive (bool): Whether or not files in subdirectories should be
                returned as well.

            filename_filter (str): Optional filter string to only include files
                in the result list that match the given filter.

        Returns:
            A list of VFS file nodes.
        """

        result = []

        for dummy, file in self.Files:
            if filename_filter is not None:
                if filename_filter in file.Name:
                    result.append(file)
            else:
                result.append(file)

        if recursive:
            for dummy, subdirectory in self.Subdirectories.items():
                result.extend(subdirectory.get_all_files())

        return  result

    def populate_from_directory(self, path: str) -> None:

        """Populates this VFS node with the contents of the given directory.

        Args:
            path (str): Path to the directory to use as source.

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

    def _add_subdirectory_from_directory(self, name: str, path: str) -> None:

        """Adds a new subdirectory node from a file system directory.

        Args:
            name (str): The name of the subdirectory to add.

            path (str): Path to the subdirectory to add.

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

        """Adds a new file node from file system directory.

        Args:
            name (str): The name of the file to add.

            path (str): Path to the file to add.

        Authors:
            Attila Kovacs
        """

        self.debug(f'Adding file {name}({path}) to node {self.Name}...')

        # Create a file node based on the file path and mark it as the latest
        # version of that file so it won't be overwritten by anything coming
        # from a resource package.
        node = VFSNode(node_name=name, node_type=VFSNodeTypes.FILE)

        data = \
        {
            'version': ResourceVersion.LATEST,
            'descriptor':
            {
                'type': 'localfile',
                'path': path
            }
        }

        resource = VFSResource(descriptor=VFSLocalFile(), data=data)
        node.add_resource(resource)

        self.add_node(node)

        self.debug(f'File {name} has been added to node {self.Name}.')
