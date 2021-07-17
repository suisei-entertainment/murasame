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
Contains the implementation of a basic singleton class.
"""

class Singleton:

    """A non-thread-safe helper class to ease implementing singletons.

    This should be used as a decorator -- not a metaclass -- to the class that
    should be a singleton.

    The decorated class can define one `__init__` function that takes only the
    `self` argument. Also, the decorated class cannot be inherited from. Other
    than that, there are no restrictions that apply to the decorated class.

    To get the singleton instance, use the `instance` method. Trying to use
    `__call__` will result in a `TypeError` being raised.

    Attributes:
        _decorated (object): The actual class to declare as Singleton.

        _instance (object): The actual instance of the wrapped object.

    Authors:
        Attila Kovacs
    """

    def __init__(self, decorated: object) -> None:

        """Creates a new Singleton instance.

        Args:
            decorated (object): The actual class that is created as a singleton.

        Authors:
            Attila Kovacs
        """

        self._decorated = decorated

    def instance(self) -> object:

        """Returns the singleton instance.

        Upon its first call, it creates a new instance of the decorated class
        and calls its `__init__` method. On all subsequent calls, the already
        created instance is returned.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=attribute-defined-outside-init

        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self) -> None:

        """Prevents direct calls to the singleton class.

        Raises:
            TypeError: Called when someone tries to access the decorated class
                outside the instance() call.

        Authors:
            Attila Kovacs
        """

        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst: object) -> bool:

        """Checks whether or not an object is the instance of the decorated
        class.

        Args:
            inst (object): The object instance to check.

        Returns:
            bool: 'True' if the object is an instance of the decorated class,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        return isinstance(inst, self._decorated)
