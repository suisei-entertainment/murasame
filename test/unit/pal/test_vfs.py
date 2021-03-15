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
Contains the unit tests of the VFS class.
"""

# Runtime Imports
import os
import sys
import shutil

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.vfs.vfs import VFS, DefaultVFS
from murasame.pal.vfs.vfsnode import VFSNode
from murasame.utils import SystemLocator

VFS_ROOT_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/vfs'))

class TestVFS:

    """
    Contains the unit tests for the VFS class.
    """

    def test_creation(self):

        """
        Tests that a VFS object can be created.
        """

        SystemLocator.instance().register_provider(VFS, DefaultVFS())
        sut = SystemLocator.instance().get_provider(VFS)
        assert sut is not None

        SystemLocator.instance().unregister_all_providers(VFS)

    def test_adding_nodes(self):

        """
        Tests that nodes can be added to the VFS.
        """

        # STEP #1 - Normal addition
        SystemLocator.instance().register_provider(VFS, DefaultVFS())
        sut = SystemLocator.instance().get_provider(VFS)

        assert not sut.has_node('test')

        sut.add_node(VFSNode(node_name='test'))

        assert sut.has_node('test')

        SystemLocator.instance().unregister_all_providers(VFS)

        # STEP #2 - Adding a node with the same name twice results in a merge
        SystemLocator.instance().register_provider(VFS, DefaultVFS())
        sut = SystemLocator.instance().get_provider(VFS)

        node1 = VFSNode(node_name='test1')
        node2 = VFSNode(node_name='test2')
        node3 = VFSNode(node_name='test1')
        node4 = VFSNode(node_name='test4')
        node1.add_node(node2)
        node3.add_node(node4)

        sut.add_node(node1)
        sut.add_node(node3)

        assert sut.has_node('test1')
        assert sut.has_node('test1/test2')
        assert sut.has_node('test1/test4')

        SystemLocator.instance().unregister_all_providers(VFS)

        # STEP #3 - Node can be added to existing parent
        SystemLocator.instance().register_provider(VFS, DefaultVFS())
        sut = SystemLocator.instance().get_provider(VFS)

        node1 = VFSNode(node_name='test1')
        node2 = VFSNode(node_name='test2')
        node3 = VFSNode(node_name='test3')

        node1.add_node(node2)
        sut.add_node(node1)
        sut.add_node(node=node3, parent='test1/test2')

        assert sut.has_node('test1/test2/test3')

        SystemLocator.instance().unregister_all_providers(VFS)

    def test_removing_nodes(self):

        """
        Tests that nodes can be removed from the VFS.
        """

        SystemLocator.instance().register_provider(VFS, DefaultVFS())
        sut = SystemLocator.instance().get_provider(VFS)

        sut.add_node(VFSNode(node_name='test'))
        assert sut.has_node('test')
        sut.remove_node(node_name='test')
        assert not sut.has_node('test')

        SystemLocator.instance().unregister_all_providers(VFS)

    def test_adding_directories(self):

        """
        Tests that file system directories can be added to the VFS.
        """

        # Create test directories
        if os.path.isdir(VFS_ROOT_PATH):
            shutil.rmtree(VFS_ROOT_PATH)

        os.mkdir(VFS_ROOT_PATH)
        os.mkdir(f'{VFS_ROOT_PATH}/subdirectory1')

        with open(f'{VFS_ROOT_PATH}/subdirectory1/file1', 'w') as file:
            file.write('{\"attribute1\": \"value1\"}')

        os.mkdir(f'{VFS_ROOT_PATH}/subdirectory2')

        with open(f'{VFS_ROOT_PATH}/subdirectory2/file2', 'w') as file:
            file.write('{\"attribute2\": \"value2\"}')

        with open(f'{VFS_ROOT_PATH}/subdirectory2/file3', 'w') as file:
            file.write('{\"attribute3\": \"value3\"}')

        os.mkdir(f'{VFS_ROOT_PATH}/subdirectory2/subdirectory3')

        with open(f'{VFS_ROOT_PATH}/subdirectory2/subdirectory3/file4', 'w') as file:
            file.write('{\"attribute4\": \"value4\"}')

        SystemLocator.instance().register_provider(VFS, DefaultVFS())
        sut = SystemLocator.instance().get_provider(VFS)

        sut.register_source(path=VFS_ROOT_PATH)

        assert sut.has_node('subdirectory1')
        assert sut.has_node('subdirectory1/file1')
        assert sut.has_node('subdirectory2')
        assert sut.has_node('subdirectory2/file2')
        assert sut.has_node('subdirectory2/file3')
        assert sut.has_node('subdirectory2/subdirectory3')
        assert sut.has_node('subdirectory2/subdirectory3/file4')

        SystemLocator.instance().unregister_all_providers(VFS)
