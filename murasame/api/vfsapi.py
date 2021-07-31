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
Contains the definition of the VFSAPI.
"""

# Runtime Imports
from abc import ABC, abstractmethod
from typing import Any

class VFSAPI(ABC):

    """The root class of the Virtual File System.

    Authors:
        Attila Kovacs
    """

    @abstractmethod
    def get_node(self, key: str) -> 'VFSNode':

        """Retrieves a VFS node by its key.

        Args:
            key (str): The key of the VFS node to retrieve.

        Returns:
            VFSNode: The VFSNode object associated with the given key.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del key

    @abstractmethod
    def get_content(self, key: str, version: 'ResourceVersion' = None) -> Any:

        """Retrieves the content of a VFS node by its key.

        Args:
            key (str): The key of the VFS node to retrieve.

            version (ResourceVersion): The version of the content to retrieve.

        Returns:
            The content of the file associated with the VFS key.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del key
        del version

    @abstractmethod
    def register_source(self, path: str) -> None:

        """Registers a new VFS data source.

        This can be a directory or a package. All resources from this data
        source will be added to the VFS tree.

        Args:
            path (str): Path to the data source.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del path

    @abstractmethod
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

        #pylint: disable=no-self-use

        del node
        del parent

    @abstractmethod
    def remove_node(self, node_name: str) -> None:

        """Removes an existing VFS node from the node tree.

        Args:
            node_name (str): Name of the node to remove.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del node_name

    @abstractmethod
    def has_node(self, name: str) -> bool:

        """Returns whether or not there is a VFS node with a given name in the
        VFS tree.

        Args:
            name (str): The name of the node to check for.

        Returns:
            bool: 'True' if the there is a node with the given name in the VFS,
            ' False' otherwise.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del name
        return  False

    @abstractmethod
    def get_all_files(
            self,
            node_name: str,
            recursive: bool = False,
            filename_filter: str = None) -> list:

        """Returns a list of all VFS file nodes under a given directory node.

        Args:
            node_name (str): The name of the VFS node to retrieve the files
                from.

            recursive (bool): Whether or not files in subdirectories should be
                returned as well.

            filename_filter (str): Optional filter string to only include files
                in the result list that match the given filter.

        Returns:
            list: A list of VFS file nodes.
        """

        #pylint: disable=no-self-use

        del node_name
        del recursive
        del filename_filter
