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
Utility class to help in parsing and handling content files.
"""

# Runtime Imports
import os
from typing import Callable

class ContentFile:

    """Represents a single content file on disk.

    The content of the file can be encrypted.

    Attributes:
        _path (str): Path to the file.

        _content (dict): The content of the file.

        _cb_retrieve_key (Callable): Optional callback function that will be
            called to retrieve the key to decrypt the file.

    Authors:
        Attila Kovacs
    """

    @property
    def Path(self) -> str:

        """Provides access to the path of the file.

        Authors:
            Attila Kovacs
        """

        return self._path

    @property
    def Content(self) -> dict:

        """Provides access to the content of the file.

        Authors:
            Attila Kovacs
        """

        return self._content

    def __init__(self, path: str, cb_retrieve_key: Callable = None) -> None:

        """Creates a new ContentFile instance.

        Args:
            path (str): Path to the file on disk.

            cb_retrieve_key (Callable): Optional callback function that will be
                called to retrieve the key to decrypt the file.

        Authors:
            Attila Kovacs
        """

        self._path = os.path.abspath(path)
        self._content = {}
        self._cb_retrieve_key = cb_retrieve_key

    def load(self) -> None:

        """Attempts to load the file from disk.

        If the file doesn't exist, it will create an empty structure in memory.

        Raises:
            InvalidInputError: Raised when the file cannot be loaded from disk
                or its content cannot be parsed as a valid file.

        Authors:
            Attila Kovacs
        """

        if os.path.isfile(self._path):

            if self._cb_retrieve_key is None:
                self.load_unencrypted()
            else:
                self.load_encrypted()
        else:
            # Just create an empty structure.
            self._content = {}

    def save(self, compact: bool = True) -> None:

        """Saves the content of the file to disk.

        Args:
            compact (bool): Specifies whether or not the file should be saved
                in a compact, less readable format, or in a properly indented
                and formatted way. This has no effect on encrypted files.

        Raises:
            RuntimeError: Raised when the file cannot be saved to disk.

        Authors:
            Attila Kovacs
        """

        if self._cb_retrieve_key is None:
            self.save_unencrypted(compact=compact)
        else:
            self.save_encrypted(compact=compact)

    def overwrite_content(self, content: dict) -> None:

        """Overwrites the content of the file with the content of a
        dictionary.

        Args:
            content (dict): The new content of the file.

        Authors:
            Attila Kovacs
        """

        self._content = content

    def save_unencrypted(self, compact: bool = True) -> None:

        """
        Saves the content of the file unencrypted to disk.

        Args:
            compact (bool): Specifies whether or not the file should be saved
                in a compact, less readable format, or in a properly indented
                and formatted way. This has no effect on encrypted files.

        Raises:
            RuntimeError: Raised when the file cannot be saved.

        Authors:
            Attila Kovacs
        """

        del compact

        raise NotImplementedError(
            f'ContentFile.save_unencrypted() has to be implemented by '
            f'{self.__class__.__name__}')

    def load_unencrypted(self) -> None:

        """Try to load the file as an unencrypted file.

        Raises:
            InvalidInputError: Raised when the file cannot be loaded.

            InvalidInputError: Raised when the content of the file cannot be
                parsed by the parser.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'ContentFile.load_unencrypted() has to be implemented by '
            f'{self.__class__.__name__}')

    def save_encrypted(self, compact: bool = True) -> None:

        """Encrypt the content of the file and save it to disk.

        Args:
            compact (bool): Specifies whether or not the file should be saved
                in a compact, less readable format, or in a properly indented
                and formatted way. This has no effect on encrypted files.

        Raises:
            RuntimeError: Raised if the content of the file cannot be saved to
                disk.

        Authors:
            Attila Kovacs
        """

        del compact

        raise NotImplementedError(
            f'ContentFile.save_encrypted() has to be implemented by '
            f'{self.__class__.__name__}')

    def load_encrypted(self) -> None:

        """Try to load and decrypt the file.

        Raises:
            InvalidInputError: Raised when the file cannot be loaded.

            InvalidInputError: Raised when the content of the file cannot
                be parsed.

        Authors:
            Attila Kovacs
        """

        raise NotImplementedError(
            f'ContentFile.load_encrypted() has to be implemented by '
            f'{self.__class__.__name__}')
