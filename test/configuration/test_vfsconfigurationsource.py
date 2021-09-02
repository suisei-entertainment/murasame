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
Contains the unit tests of VFSConfigurationSource class.
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
from murasame.configuration.vfsconfigurationsource import VFSConfigurationSource
from murasame.api import VFSAPI
from murasame.pal.vfs import VFS
from murasame.utils import SystemLocator
from murasame.configuration.dictionarybackend import DictionaryBackend

# Test Imports
from test.constants import TEST_FILES_DIRECTORY
CONFIG_SOURCE_PATH = f'{TEST_FILES_DIRECTORY}/vfsconfigurationsource'

class TestVFSConfigurationSource:

    """Contains the unit tests of the VFSConfigurationSource class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self) -> None:

        """Tests that a VFSConfigurationSource instance can be created.

        Authors:
            Attila Kovacs
        """

        sut = VFSConfigurationSource(path='/test')
        assert sut is not None

    def test_loading_configuration_from_a_valid_source(self) -> None:

        """Tests that the configuration can be loaded from a valid VFS
        directory.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(path=CONFIG_SOURCE_PATH)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        backend=DictionaryBackend()

        sut = VFSConfigurationSource(path='/config')
        sut.load(backend=backend)

        assert backend.has_group('testgroup')
        assert backend.has_group('testgroup.testgroup2')
        assert backend.has_attribute('testgroup.testgroup2.testattribute1')
        assert backend.has_attribute('testgroup.testattribute2')
        assert backend.has_list('testgroup.testlist')

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)

    def test_loading_configuration_without_vfs(self) -> None:

        """Tests that the configuration cannot be loaded without a valid VFS.

        Authors:
            Attila Kovacs
        """

        backend=DictionaryBackend()
        sut = VFSConfigurationSource(path='/invalid')
        with pytest.raises(RuntimeError):
            sut.load(backend=backend)

    def test_loading_configuration_from_an_invalid_source(self) -> None:

        """Tests that an invalid VFS directory cannot be loaded.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        backend=DictionaryBackend()

        sut = VFSConfigurationSource(path='/invalid')
        with pytest.raises(InvalidInputError):
            sut.load(backend=backend)

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)