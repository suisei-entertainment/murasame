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
Contains the unit tests of the VFSPackage class.
"""

# Runtime Imports
import os
import sys
import tarfile
import json
from pathlib import Path

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.api import VFSAPI
from murasame.pal.vfs.vfspackage import VFSPackage
from murasame.pal.vfs.vfs import VFS
from murasame.utils import SystemLocator

TEST_PACKAGE_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/vfspackage.pkg'))

class TestPackage:

    """Contains the unit tests for the VFSPackage class.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls) -> None:

        # Setup VFS
        SystemLocator.instance().register_provider(VFSAPI, VFS())

    @classmethod
    def teardown_class(cls) -> None:

        SystemLocator.instance().reset()

    def test_creation(self) -> None:

        """Tests that a VFSPackage object can be created.

        Authors:
            Attila Kovacs
        """

        sut = VFSPackage(path=TEST_PACKAGE_PATH)
        assert sut is not None
        assert sut.Path == TEST_PACKAGE_PATH

    def test_package_loading(self) -> None:

        """Tests that a VFSPackage loads correctly from file.

        Authors:
            Attila Kovacs
        """

        vfs = SystemLocator.instance().get_provider(VFSAPI)

        sut = VFSPackage(path=TEST_PACKAGE_PATH)
        assert vfs.has_node('/directory1')
        assert vfs.has_node('/directory2')
        assert vfs.has_node('/directory1/file1.txt')
        assert vfs.has_node('/directory2/file2.txt')
        assert vfs.get_node('/directory1/file1.txt').Latest.Descriptor.PackagePath == TEST_PACKAGE_PATH
        assert vfs.get_node('/directory2/file2.txt').Latest.Descriptor.PackagePath == TEST_PACKAGE_PATH
