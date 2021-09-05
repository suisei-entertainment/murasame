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
Contains the unit tests of Configuration class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.configuration import Configuration
from murasame.api import VFSAPI
from murasame.pal.vfs import VFS
from murasame.utils import SystemLocator
from murasame.exceptions import InvalidInputError

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

CONFIG_TEST_DIRECTORY = f'{TEST_FILES_DIRECTORY}/configurationtest'
CONFIG_DIRECTORY = f'{CONFIG_TEST_DIRECTORY}/configuration'
CONFIG_FILE = f'{CONFIG_DIRECTORY}/configuration.conf'

class TestConfiguration:

    """Contains the unit tests  of the Configuration class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self) -> None:

        """Tests that a Configuration object can be created.

        Authors:
            Attila Kovacs
        """

        sut = Configuration()
        assert sut is not None
        assert isinstance(sut, Configuration)

    def test_initialization_without_vfs(self) -> None:

        """Tests that the configuration cannot be initialized without VFS.

        Authors:
            Attila Kovacs
        """

        sut = Configuration()
        with pytest.raises(RuntimeError):
            sut.initialize()

    def test_initialization_without_encryption(self) -> None:

        """Tests that the configuration can be initialized with non-encrypted
        configuration files.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(CONFIG_TEST_DIRECTORY)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        sut = Configuration()
        sut.initialize()

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)

    def test_initialization_with_encrypted_configuration(self) -> None:

        """Tests that the configuration can be initialized with encrypted
        configuration files.

        Authors:
            Attila Kovacs
        """

        #TODO
        pass

    def test_retrieving_existing_configuration_attributes(self) -> None:

        """Tests that the value of existing configuration attributes can be
        retrieved.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(CONFIG_TEST_DIRECTORY)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        sut = Configuration()
        sut.initialize()
        sut.load()

        assert sut.get(attribute='testgroup1.testattribute1') == 1
        assert sut.get(attribute='testgroup1.testgroup2.testattribute2') == 'testvalue'

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)

    def test_retrieving_non_existing_configuration_attributes(self) -> None:

        """Tests retrieval of non-existend configuration attributes.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(CONFIG_TEST_DIRECTORY)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        sut = Configuration()
        sut.initialize()
        sut.load()

        assert sut.get(attribute='nonexistent.nonexistent') is None

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)

    def test_setting_existing_configuration_attributes(self) -> None:

        """Tests setting the value of an existing configuration attribute.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(CONFIG_TEST_DIRECTORY)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        sut = Configuration()
        sut.initialize()
        sut.load()

        assert sut.get(attribute='testgroup1.testattribute1') == 1
        sut.set(attribute='testgroup1.testattribute1', value=2)
        assert sut.get(attribute='testgroup1.testattribute1') == 2

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)

    def test_setting_non_existing_configuration_attributes(self) -> None:

        """Tests setting the value of a non-existing configuration attribute.

        Authors:
            Attila Kovacs
        """

        vfs = VFS()
        vfs.register_source(CONFIG_TEST_DIRECTORY)
        SystemLocator.instance().register_provider(VFSAPI, vfs)

        sut = Configuration()
        sut.initialize()
        sut.load()

        sut.set(attribute='nonexistent.nonexistent', value='new')

        SystemLocator.instance().unregister_provider(VFSAPI, vfs)

    def test_saving_configuration(self) -> None:

        """Tests saving the configuration.

        Authors:
            Attila Kovacs
        """

        #TODO
        pass