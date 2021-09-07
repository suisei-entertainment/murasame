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
Contains the unit tests of the Singleton class.
"""

# Runtime Imports
import os
import sys
import shutil

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.utils import SystemLocator, System
from murasame.utils.systemlocator import SystemPath

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

SYSTEM_DIR = f'{TEST_FILES_DIRECTORY}/systems/'

class TestSystemLocator:

    """Contains the unit tests of the system locator pattern.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls) -> None:
        sys.path.append(TEST_FILES_DIRECTORY)

    def test_system_path(self) -> None:

        """Tests that system paths can be created correctly.

        Authors:
            Attila Kovacs
        """

        system_path = '/path/to/systems'
        system_package = 'path.to.systems'

        sut = SystemPath(system_path, system_package)
        assert sut.Path == system_path
        assert sut.Package == system_package

    def test_system_discovery_with_valid_system_path(self) -> None:

        """Tests that system discovery works properly when a valid system path
        is provided.

        Authors:
            Attila Kovacs
        """

        # Register the path with the system locator
        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')

        # Run system discovery
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem

        assert SystemLocator.instance().get_provider(AbstractSystem) is not None

    def test_system_discovery_with_valid_system_path(self) -> None:

        """Tests that system discovery works properly when an invalid system
        path is provided.

        Authors:
            Attila Kovacs
        """

        from systems.testsystem import AbstractSystem
        SystemLocator.instance().register_path('/invalid/path', 'systems')
        SystemLocator.instance().discover_systems()

        assert SystemLocator.instance().get_provider(AbstractSystem) is not None

    def test_duplicate_system_path_registration(self) -> None:

        """Tests that system paths cannot be registered twice.

        Authors:
            Attila Kovacs
        """

        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem
        assert  SystemLocator.instance().get_provider(AbstractSystem) is not None

    def test_accessing_systems(self) -> None:

        """Tests that systems can be accessed through the SystemLocator.

        Authors:
            Attila Kovacs
        """

        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem
        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

    def test_resetting_system_locator(self) -> None:

        """Tests that the system locator can be reset.

        Authors:
            Attila Kovacs
        """

        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem, ConcreteSystem
        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

        SystemLocator.instance().reset()
        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is None

    def test_adding_providers_after_reset(self) -> None:

        """Tests that new providers can be registered after the system locator
        has been reset.

        Authors:
            Attila Kovacs
        """

        from systems.testsystem import AbstractSystem, ConcreteSystem
        SystemLocator.instance().reset()
        SystemLocator.instance().register_provider(AbstractSystem, ConcreteSystem())

        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

    def test_unregistering_single_provider(self) -> None:

        """Tests that as single registered provider can be unregistered.

        Authors:
            Attila Kovacs
        """

        SystemLocator.instance().reset()

        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem, ConcreteSystem
        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

        SystemLocator.instance().unregister_provider(AbstractSystem, provider)
        provider = SystemLocator.instance().get_provider(AbstractSystem)

        assert provider is None

    def test_unregistering_all_providers(self) -> None:

        """Tests that all providers can be unregistered.

        Authors:
            Attila Kovacs
        """

        from systems.testsystem import AbstractSystem, ConcreteSystem
        SystemLocator.instance().reset()
        SystemLocator.instance().register_provider(AbstractSystem, ConcreteSystem())

        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

        SystemLocator.instance().unregister_all_providers(AbstractSystem)
        provider = SystemLocator.instance().get_provider(AbstractSystem)

        assert provider is None
