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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.vfs.vfsnode import VFSNode, VFSNodeTypes

class TestVFSNode:

    """
    Contains the unit tests for the VFSNode class.
    """

    def test_creation(self):

        """
        Tests that a VFSNode object can be created.
        """

        # STEP #1 - Create root node
        sut = VFSNode(node_name='', node_type=VFSNodeTypes.DIRECTORY)
        assert sut is not None
        assert sut.isroot()
        assert sut.Name == 'ROOT'

        # STEP #2 - Create non-root node
        sut = VFSNode(node_name='test', node_type=VFSNodeTypes.DIRECTORY)
        assert sut is not None
        assert not sut.isroot()
        assert sut.Name == 'test'
        assert not sut.Files
        assert not sut.Subdirectories
        assert not sut.Resources
        assert not sut.Latest

        # STEP #3 - Root node can only be a directory node
        with pytest.raises(InvalidInputError):
            sut = VFSNode(node_name='', node_type=VFSNodeTypes.FILE)

    def test_type_checking(self):

        """
        Tests that the type of the node can be checked.
        """

        # STEP #1 - Directory node
        sut = VFSNode(node_name='test', node_type=VFSNodeTypes.DIRECTORY)
        assert sut.Type == VFSNodeTypes.DIRECTORY
        assert sut.isdir()
        assert not sut.isfile()

        # STEP #2 - File node
        sut = VFSNode(node_name='test', node_type=VFSNodeTypes.FILE)
        assert sut.Type == VFSNodeTypes.FILE
        assert not sut.isdir()
        assert sut.isfile()

    def test_adding_resource(self):

        """
        Tests that resources can be added to the node.
        """

        pass

    def test_removing_resource(self):

        """
        Tests that resources can be removed from the node.
        """

        pass
