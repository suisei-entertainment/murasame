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
Contains the implementation of the system locator design pattern.
"""

# Runtime Imports
import os
import glob
import importlib
from typing import Callable, Union

# Murasame Imports
from .singleton import Singleton

class SystemPath:

    """Represents a directory that contains the systems to be registered in the
    system locator.

    Attributes:
        _path (str): The path to the directory where the systems are located.

        _package (str): Name of the package to import for importing the system
            module.

    Authors:
        Attila Kovacs
    """

    @property
    def Path(self) -> str:

        """The path to the directory where the systems are located.

        Authors:
            Attila Kovacs
        """

        return self._path

    @property
    def Package(self) -> str:

        """Name of the package to import for importing the system module.

        Authors:
            Attila Kovacs
        """

        return self._package

    def __init__(self, path: str, package: str) -> None:

        """Creates a new SystemPath instance.

        Args:
            path (str): The path to the directory where the systems are
                located.

            package (str): Name of the package to import for importing the
                system module.

        Authors:
            Attila Kovacs
        """

        self._path = path
        self._package = package

@Singleton
class SystemLocator:

    """Central class of the system locator pattern.

    Stores the list of available systems and handles system discovery.

    This implementation is based on the one by yujanshrestha.
        https://github.com/innolitics/service-locator

    Attributes:
        _systems (dict): List of registered srvice providers grouped by the
            system they provide.

        _system_paths (list): List of directories where system implementations
            are stored.

        _modules (list): List of modules loaded by the system locator.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """Creates a new SystemLocator instance.

        Authors:
            Attila Kovacs
        """

        self._systems = {}
        self._system_paths = []
        self._modules = []

    def register_provider(self, system: object, instance: object) -> None:

        """Registers a new system provider for a given system.

        Args:
            system (object): The system to register a provider for.

            instance (object): The system provider instance to register.

        Authors:
            Attila Kovacs
        """

        providers = self._systems.get(system)

        if providers is None:
            providers = []
            self._systems[system] = providers

        providers.append(instance)

    def unregister_provider(self, system: object, instance: object) -> None:

        """Unregisters a provider from a given system.

        Args:
            system (object): The system to unregister the provider from.

            instance (object): The system provider instance to unregister.

        Authors:
            Attila Kovacs
        """

        providers = self._systems.get(system)

        if providers is not None:
            providers.remove(instance)

            if len(providers) == 0:
                system_object = self._systems.get(system)
                if system_object:
                    del system_object

    def unregister_all_providers(self, system: object) -> None:

        """Unregisters all providers of a given system.

        Args:
            system (object): The system to unregister the providers from.

        Authors:
            Attila Kovacs
        """

        system_object = self._systems.get(system)
        if system_object:
            self._systems.pop(system)

    def reset(self) -> None:

        """Resets the system locator.

        Authors:
            Attila Kovacs
        """

        self._systems = {}
        self._system_paths = []

        # Also invalidate the module caches so modules can be imported again
        # if required.
        importlib.invalidate_caches()

    def get_all_providers(self, system: object) -> list:

        """Returns all providers for a given system.

        Args:
            system (object): The system to get the providers for.

        Returns:
            list: A list of system providers that provide the requested system,
                or an empty list if there are no providers registered that
                provide the requested system.

        Authors:
            Attila Kovacs
        """

        providers = self._systems.get(system) or []
        return providers

    def get_provider(self, system: object) -> Union[object, None]:

        """Returns a provider for a given system.

        This function will always return the first registered system provider
        for the given system.

        Args:
            system (object): The system to get a provider for.

        Returns:
            Union[object, None]: A provider for the given system, or None if
                there are no providers registered that provide the requested
                system.

        Authors:
            Attila Kovacs
        """

        provider = None

        try:
            provider = self.get_all_providers(system)[0]
        except IndexError:
            pass

        return provider

    def has_system_path(self, path: str) -> bool:

        """Returns whether or not the given path is already registered as a
        system path.

        Args:
            path (str): The path to check.

        Returns:
            bool: 'True' if the given path is already registered, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        for system_path in self._system_paths:
            if system_path.Path == path:
                return True

        return False

    def register_path(self, path: str, package: str) -> None:

        """Registers a new system path with the service locator.

        Args:
            path (str): The path to the directory containing the systems.

            package (str): The package that will be used to include the systems
                inside that path.

        Authors:
            Attila Kovacs
        """

        # Do not register the same path twice.
        if self.has_system_path(path):
            return

        self._system_paths.append(SystemPath(path, package))

    def discover_systems(self) -> None:

        """System discovery logic to load all systems from all registered
        system paths.

        Authors:
            Attila Kovacs
        """

        for system_path in self._system_paths:

            # Check if the directory exists
            if not os.path.isdir(os.path.abspath(system_path.Path)):
                continue

            # Collect files from the target directory
            current_dir = os.getcwd()
            os.chdir(os.path.abspath(system_path.Path))

            for file in glob.iglob('*.py', recursive=False):

                # Skip __init__.py
                if file.endswith('__init__.py'):
                    continue

                # Import the module
                dummy, filename = os.path.split(file)
                filename, dummy = os.path.splitext(filename)

                import_name = '{}.{}'.format(system_path.Package, filename)

                module_loaded = False
                for module in self._modules:
                    if module.__name__ == import_name:
                        importlib.reload(module)
                        module_loaded = True
                        break

                if not module_loaded:

                    # Register the system by loading its module
                    module = importlib.import_module(import_name)
                    if module is not None:
                        self._modules.append(module)

            os.chdir(current_dir)

# Using underscore system here would redefine an existing name
#pylint: disable=invalid-name
def System(*systems):

    """Class decorator that declares a class to provide a set of systems.

    It is expected that the class has a no-arg constructor and will be
    instantiated as a singleton.

    This decorator only works once. So if this system is unregistered manually
    or reset() is called on SystemLocator then all systems using this
    decorator has to be registered manually again.

    Args:
        systems (list): The list of systems that the decorated class will
            provide.

    Authors:
        Attila Kovacs
    """

    def real_decorator(system_class: Callable) -> object:

        """Creates the decorated class.

        Args:
            system_class (Callable): The class that will provide the system.

        Returns:
            object: The system class this decorator wraps.

        Authors:
            Attila Kovacs
        """

        # Pylint doesn't recognize the instance() member from the Singleton
        # decorator.
        # pylint: disable=no-member

        instance = system_class()
        for system in systems:
            SystemLocator.instance().register_provider(system, instance)
        return system_class

    return real_decorator
