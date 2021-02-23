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
Contains the implementation of the Secrets class.
"""

# Platform Imports
import os
from typing import Union

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils.jsonfile import JsonFile

class Secrets:

    """
    Simple utility class to load an encrypted JSON file from the application's
    configuration directory and read keys from it.

    To decrypt the secrets file the decryption key is read from an environment
    variable.

    Authors:
        Attila Kovacs
    """

    # Pylint with Python 3.9 seems to trigger a falso positive thinking the
    # Union type is unsubscriptable., so disable that check here for now.
    #pylint: disable=unsubscriptable-object

    def __init__(self, config_directory: str) -> None:

        """
        Creates a new Secrets instance.

        Args:
            config_directory:       Path to the directory where application
                                    configuration is stored.

        Authors:
            Kovacs Attila
        """

        # Path to the directory where application configuration is stored.
        self._config_directory = config_directory

    @staticmethod
    def retrieve_key() -> Union[str, None]:

        """
        Callback function to retrieve the decryption key for the secrets.conf
        file.

        Returns:
            The decryption key as a string, or None if the key cannot be
            retrieved.

        Authors:
            Attila Kovacs
        """

        pwd = os.getenv('MURASAME_SECRETS_KEY')
        if not pwd:
            return None

        return pwd

    def get_secret(self, key: str) -> Union[str, None]:

        """
        Loads the secrets file to memory and reads the given key from it.

        Args:
            key:        The key to read from the file.

        Returns:
            The value of the given key, or None if the key cannot be retrieved.

        Authors:
            Attila Kovacs
        """

        file_path = os.path.abspath(
            os.path.expanduser(f'{self._config_directory}/secrets.conf'))

        # Check whether or not the file exists
        if not os.path.isfile(file_path):
            return None

        # Load the file and decrypt it
        file = JsonFile(path=file_path, cb_retrieve_key=Secrets.retrieve_key)

        try:
            file.load()
        except InvalidInputError:
            return None

        try:
            return file.Content[key]
        except KeyError:
            return None
