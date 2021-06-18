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
Contains the unit tests of the VFSNode class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.pal.vfs.vfsnode import VFSNode, VFSNodeTypes
from murasame.pal.vfs.vfsresource import VFSResource
from murasame.pal.vfs.vfsresourcetypes import VFSResourceTypes
from murasame.pal.vfs.resourceversion import ResourceVersion
from murasame.pal.vfs.vfslocalfile import VFSLocalFile

# Test data
SERIALIZED_NODE_DATA = \
        {
            'name': 'test1',
            'type': 'directory',
            'subdirectories':
            {
                'test2':
                {
                    'name': 'test2',
                    'type': 'directory',
                    'subdirectories': {},
                    'files': {}
                },
                'test3':
                {
                    'name': 'test3',
                    'type': 'directory',
                    'subdirectories': {},
                    'files':
                    {
                        'test4':
                        {
                            'name': 'test4',
                            'type': 'file',
                            'resource': []
                        }
                    }
                }
            },
            'files':
            {

            }
        }

class TestVFSNode:

    """
    Contains the unit tests for the VFSNode class.

    Authors:
        Attila Kovacs
    """

    def test_creation_root_node(self):

        """
        Tests that a VFSNode object can be created as the root node of the
        VFS tree.

        Authors:
            Attila Kovacs
        """

        sut = VFSNode(node_name='', node_type=VFSNodeTypes.DIRECTORY)
        assert sut is not None
        assert sut.isroot()
        assert sut.Name == 'ROOT'

    def test_creation_non_root_node(self):

        """
        Tests that a VFSNode object can be created as a non-root node of the
        VFS tree.

        Authors:
            Attila Kovacs
        """

        sut = VFSNode(node_name='test', node_type=VFSNodeTypes.DIRECTORY)
        assert sut is not None
        assert not sut.isroot()
        assert sut.Name == 'test'
        assert not sut.Files
        assert not sut.Subdirectories
        assert not sut.Resources
        assert not sut.Latest

    def test_creation_non_directory_root_node(self):

        """
        Tests that the root node of the VFS tree can only be a directory node.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = VFSNode(node_name='', node_type=VFSNodeTypes.FILE)

    def test_type_checking_of_directory_node(self):

        """
        Tests that the type of a directory node can be checked.

        Authors:
            Attila Kovacs
        """

        sut = VFSNode(node_name='test', node_type=VFSNodeTypes.DIRECTORY)
        assert sut.Type == VFSNodeTypes.DIRECTORY
        assert sut.isdir()
        assert not sut.isfile()

    def test_type_checking_of_file_node(self):

        """
        Tests that the type of a file node can be checked.

        Authors:
            Attila Kovacs
        """

        sut = VFSNode(node_name='test', node_type=VFSNodeTypes.FILE)
        assert sut.Type == VFSNodeTypes.FILE
        assert not sut.isdir()
        assert sut.isfile()

    def test_adding_single_resource(self):

        """
        Tests that a single VFS resource can be added to the node.

        Authors:
            Attila Kovacs
        """

        resource1 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 1,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        sut = VFSNode(node_name='test1', node_type=VFSNodeTypes.FILE)
        sut.add_resource(resource1)

        assert sut.Latest == resource1
        assert sut.NumResources == 1

    def test_adding_multiple_resources_with_different_version(self):

        """
        Tests that multiple VFS resources with difference resource versions
        can be added to the node.

        Authors:
            Attila Kovacs
        """

        resource1 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 1,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        resource2 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 2,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        sut = VFSNode(node_name='test1', node_type=VFSNodeTypes.FILE)
        sut.add_resource(resource1)
        sut.add_resource(resource2)

        assert sut.Latest == resource2
        assert sut.NumResources == 2

    def test_adding_multiple_resources_with_same_version(self):

        """
        Tests that a second VFS resource with the same version as an already
        existing resource cannot be added to the node.

        Authors:
            Attila Kovacs
        """

        resource1 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 1,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        resource2 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 1,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        sut = VFSNode(node_name='test1', node_type=VFSNodeTypes.FILE)
        sut.add_resource(resource1)
        sut.add_resource(resource2)

        assert sut.Latest == resource1
        assert sut.NumResources == 1

    def test_adding_resource_in_any_order(self):

        """
        Tests that resources can be added to the VFS node in any order.

        Authors:
            Attila Kovacs
        """

        resource1 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 1,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        resource2 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 2,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        resource3 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 3,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        resource4 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 4,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        sut = VFSNode(node_name='test1', node_type=VFSNodeTypes.FILE)
        sut.add_resource(resource1)
        sut.add_resource(resource3)
        sut.add_resource(resource4)
        sut.add_resource(resource2)

        assert sut.NumResources == 4
        assert sut.Latest == resource4

    def test_removing_single_resource(self):

        """
        Tests that a single VFS resource can be removed from the node.

        Authors:
            Attila Kovacs
        """

        resource1 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 1,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        sut = VFSNode(node_name='test1', node_type=VFSNodeTypes.FILE)
        sut.add_resource(resource1)
        sut.remove_resource(version=1)

        assert sut.NumResources == 0

    def test_removing_single_resource_from_multiple(self):

        """
        Tests that a single VFS resource can be removed from the node when
        multiple resource are added to the node.

        Authors:
            Attila Kovacs
        """

        resource1 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 1,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        resource2 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 2,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        resource3 = VFSResource(descriptor=VFSLocalFile(),
                                data={'version': 3,
                                      'descriptor': {
                                            'type': 'localfile',
                                            'path': '/test'}})

        sut = VFSNode(node_name='test1', node_type=VFSNodeTypes.FILE)
        sut.add_resource(resource1)
        sut.add_resource(resource2)
        sut.add_resource(resource3)
        sut.remove_resource(version=1)

        assert sut.NumResources == 2

    def test_serialization(self):

        """
        Tests that a VFS node can be serialized to a dictionary.

        Authors:
            Attila Kovacs
        """

        sut = VFSNode(node_name='test1')
        node2 = VFSNode(node_name='test2')
        node3 = VFSNode(node_name='test3')
        node4 = VFSNode(node_name='test4', node_type=VFSNodeTypes.FILE)

        node3.add_node(node4)

        sut.add_node(node2)
        sut.add_node(node3)

        data = sut.serialize()

        assert data == SERIALIZED_NODE_DATA

    def test_deserialization(self):

        """
        Tests that a VFS node can be deserialized from a dictionary.

        Authors:
            Attila Kovacs
        """

        sut = VFSNode(node_name='whatever')
        sut.deserialize(data=SERIALIZED_NODE_DATA)

        assert sut.Name == 'test1'
        assert sut.has_node('test2')
        assert sut.has_node('test3')
        assert sut.has_node('test3/test4')
