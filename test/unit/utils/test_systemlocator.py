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

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils import SystemLocator, System
from murasame.utils.systemlocator import SystemPath

TEST_SYSTEM = \
"""
from murasame.utils import System, SystemLocator

class AbstractSystem:
    def system_function(self):
        pass

class AnotherAbstractSystem:
    def system_function(self):
        pass

@System(AbstractSystem)
class ConcreteSystem(AbstractSystem):
    def system_function(self):
        return True
"""

SYSTEM_DIR = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/systems/'))

class TestSystemLocator:

    """
    Contains the unit tests of the system locator pattern.
    """

    def test_system_path(self):

        """
        Tests that system paths can be created correctly.
        """

        system_path = '/path/to/systems'
        system_package = 'path.to.systems'

        sut = SystemPath(system_path, system_package)
        assert sut.Path == system_path
        assert sut.Package == system_package

    def test_system_discovery(self):

        """
        Tests that system discovery works properly.
        """

        sys.path.append(os.path.abspath(os.path.expanduser(
            '~/.murasame/testfiles/')))

        if not os.path.isdir(SYSTEM_DIR):
            os.mkdir(SYSTEM_DIR)

        # Create a test system file
        system_file = '{}/{}'.format(SYSTEM_DIR, 'testsystem.py')
        with open(system_file, 'w+') as test_file:
            test_file.write(TEST_SYSTEM)

        # Create an __init__.py file
        init_file = '{}/{}'.format(SYSTEM_DIR, '__init__.py')
        with open(init_file, 'w+') as test_file:
            test_file.write('\n')

        # STEP #1 - Load a valid system path

        # Register the path with the system locator
        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')

        # Run system discovery
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem

        assert SystemLocator.instance().get_provider(AbstractSystem) is not None

        # STEP #2 - Try to load an invalid system path
        SystemLocator.instance().register_path('/invalid/path', 'systems')
        SystemLocator.instance().discover_systems()

        assert SystemLocator.instance().get_provider(AbstractSystem) is not None

    def test_duplicate_system_path_registration(self):

        """
        Tests that system paths cannot be registered twice.
        """

        sys.path.append(os.path.abspath(os.path.expanduser(
            '~/.murasame/testfiles/')))

        if not os.path.isdir(SYSTEM_DIR):
            os.mkdir(SYSTEM_DIR)

        # Create a test system file
        system_file = '{}/{}'.format(SYSTEM_DIR, 'testsystem.py')
        with open(system_file, 'w+') as test_file:
            test_file.write(TEST_SYSTEM)

        # Create an __init__.py file
        init_file = '{}/{}'.format(SYSTEM_DIR, '__init__.py')
        with open(init_file, 'w+') as test_file:
            test_file.write('\n')

        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem
        assert  SystemLocator.instance().get_provider(AbstractSystem) is not None

    def test_accessing_systems(self):

        """
        Tests that systems can be accessed through the SystemLocator.
        """

        sys.path.append(os.path.abspath(os.path.expanduser(
            '~/.murasame/testfiles/')))

        if not os.path.isdir(SYSTEM_DIR):
            os.mkdir(SYSTEM_DIR)

            # Create a test system file
            system_file = '{}/{}'.format(SYSTEM_DIR, 'testsystem.py')
            with open(system_file, 'w+') as test_file:
                test_file.write(TEST_SYSTEM)

            # Create an __init__.py file
            init_file = '{}/{}'.format(SYSTEM_DIR, '__init__.py')
            with open(init_file, 'w+') as test_file:
                test_file.write('\n')

        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem
        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

    def test_resetting_system_locator(self):

        """
        Tests that the system locator can be reset.
        """

        # STEP #1 - Reset should remove existing providers
        sys.path.append(os.path.abspath(os.path.expanduser(
            '~/.murasame/testfiles/')))

        if not os.path.isdir(SYSTEM_DIR):
            os.mkdir(SYSTEM_DIR)

            # Create a test system file
            system_file = '{}/{}'.format(SYSTEM_DIR, 'testsystem.py')
            with open(system_file, 'w+') as test_file:
                test_file.write(TEST_SYSTEM)

            # Create an __init__.py file
            init_file = '{}/{}'.format(SYSTEM_DIR, '__init__.py')
            with open(init_file, 'w+') as test_file:
                test_file.write('\n')

        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem, ConcreteSystem
        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

        SystemLocator.instance().reset()
        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is None

        # STEP #2 - New providers can be added after reset
        SystemLocator.instance().register_provider(AbstractSystem, ConcreteSystem())

        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

    def test_provider_unregistration(self):

        """
        Tests that registered system providers can be unregistered.
        """

        # STEP #1 - Unregistering a single provider
        SystemLocator.instance().reset()

        sys.path.append(os.path.abspath(os.path.expanduser(
            '~/.murasame/testfiles/')))

        if not os.path.isdir(SYSTEM_DIR):
            os.mkdir(SYSTEM_DIR)

            # Create a test system file
            system_file = '{}/{}'.format(SYSTEM_DIR, 'testsystem.py')
            with open(system_file, 'w+') as test_file:
                test_file.write(TEST_SYSTEM)

            # Create an __init__.py file
            init_file = '{}/{}'.format(SYSTEM_DIR, '__init__.py')
            with open(init_file, 'w+') as test_file:
                test_file.write('\n')

        SystemLocator.instance().register_path(SYSTEM_DIR, 'systems')
        SystemLocator.instance().discover_systems()

        from systems.testsystem import AbstractSystem, ConcreteSystem
        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

        SystemLocator.instance().unregister_provider(AbstractSystem, provider)
        provider = SystemLocator.instance().get_provider(AbstractSystem)

        assert provider is None

        # STEP #2 - Unregister all providers
        from systems.testsystem import AbstractSystem
        SystemLocator.instance().reset()
        SystemLocator.instance().register_provider(AbstractSystem, ConcreteSystem())

        provider = SystemLocator.instance().get_provider(AbstractSystem)
        assert provider is not None
        assert provider.system_function()

        SystemLocator.instance().unregister_all_providers(AbstractSystem)
        provider = SystemLocator.instance().get_provider(AbstractSystem)

        assert provider is None
