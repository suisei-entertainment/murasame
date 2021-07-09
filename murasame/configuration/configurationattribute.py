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
Contains the implementation of the ConfigurationAttribute class.
"""

# Runtime Imports
from typing import Any

# Murasame Imports
from murasame.exceptions import InvalidInputError

class ConfigurationAttribute:

    """Representation of a single configuration attribute.

    Attributes:
        _name (str): The name of the attribute
        _value (Any): The currentvalue of the attribute.
        _type (str): The data type of the attribute.

    Authors:
        Attila Kovacs
    """

    @property
    def Name(self) -> str:

        """The name of the attribute.

        Authors:
            Attila Kovacs
        """

        return self._name

    @property
    def Value(self) -> Any:

        """The current value of the attribute.

        Authors:
            Attila Kovacs
        """

        return self._value

    @Value.setter
    def Value(self, value: Any) -> None:

        if self._type == 'STRING':
            self._value = str(value)
        elif self._type == 'INT':

            try:
                self._value = int(value)
                return
            except ValueError:
                pass

            try:
                self._value = int(float(value))
                return
            except ValueError as exception:
                raise InvalidInputError(f'Failed to convert input value '
                                        f'{value} to integer.') from exception

        elif self._type == 'FLOAT':

            try:
                self._value = float(value)
            except ValueError as exception:
                raise InvalidInputError(f'Failed to convert input value '
                                        f'{value} to float.') from exception

    @property
    def Type(self) -> str:

        """The data type of the property.

        Authors:
            Attila Kovacs
        """

        return self._type

    def __init__(self, name: str, value: Any, data_type: str) -> None:

        """Creates a new ConfigurationAttribute instance.

        Args:
            name (str): The name of the attribute.
            value (Any): The value of the attribute.
            data_type (str): The data type of the attribute.

        Authors:
            Attila Kovacs
        """

        self._name = name
        self._value = value
        self._type = data_type

    def __str__(self) -> str:

        """Returns the string representation of the object.

        Authors:
            Attila Kovacs
        """

        return f'{self._name} : {self._type} = {self._value}'

    def __repr__(self) -> str:

        """Returns the string representation of the object.

        Authors:
            Attila Kovacs
        """

        return f'{self._name} : {self._type} = {self._value}'
