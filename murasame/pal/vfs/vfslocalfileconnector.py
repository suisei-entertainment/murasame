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
Contains the implementation of the VFSLocalFileConnector class.
"""

# Runtime Imports
import os
from typing import Any

# Dependency Imports
import magic

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils import JsonFile, YamlFile
from murasame.pal.vfs.vfsresourceconnector import VFSResourceConnector
from murasame.pal.vfs.vfslocalfile import VFSLocalFile

class VFSLocalFileConnector(VFSResourceConnector):

    """
    Resource connector implementation for files in the local file system.

    Authors:
        Attila Kovacs
    """

    def load(self, descriptor: 'VFSResourceDescriptor') -> Any:

        """
        Loads the content of the VFS resource into memory.

        Args:
            descriptor:     The resource descriptor of the resource to load.

        Raises:
            InvalidInputError:      Raised when the provided descriptor is not
                                    a VFSLocalFile.

        Returns:
            The loaded resource data.

        Authors:
            Attila Kovacs
        """

        # This connector can only load resources with type VFSLocalFile
        if not descriptor or not isinstance(descriptor, VFSLocalFile):
            raise InvalidInputError('Invalid descriptor type provided.')

        # Retrieve the path from the descriptor
        path = os.path.abspath(os.path.expanduser(descriptor.Path))

        self.debug(f'Loading the content of VFS resource from {path}...')

        # Check the existense of the physical file
        if not os.path.isfile(path):
            self.warning(f'{path} does not exist in the local file system.')
            return None

        # Check the content type of the file
        content_type = descriptor.ContentType

        # If there is no content type provided in the descriptor, try to guess
        # the content type from the extension.
        if not content_type:
            self.debug(f'No content type provided in the descriptor, trying to '
                       f'guess the content type of {path}.')
            content_type = magic.from_file(path, mime=True)
            self.debug(f'Content type for {path} is identified as '
                       f'{content_type}.')

            # Update the content type in the descriptor
            descriptor.update_content_type(content_type)

        self.debug(f'Loading {path} as {content_type}...')

        if content_type == 'application/json':
            return self._load_as_json(path)
        elif content_type == 'application/x-yaml':
            return self._load_as_yaml(path)

        self.debug(f'Content type {content_type} doesn\'t match any of the '
                   f'supported MIME types, loading the file as a binary.')
        return self._load_as_binary(path)

    @staticmethod
    def _load_as_json(path: str) -> dict:

        """
        Loads the content of the file expecting the file to be a JSON file.

        Args:
            path:       Path to the file to load.

        Returns:
            The parsed content of the file as a dictionary.

        Authors:
            Attila Kovacs
        """

        file = JsonFile(path)
        file.load()
        return file.Content

    @staticmethod
    def _load_as_yaml(path: str) -> dict:

        """
        Loads the content of the file expecting the file to be a YAML file.

        Args:
            path:       Path to the file to load.

        Returns:
            The parsed content of the file as a dictionary.

        Authors:
            Attila Kovacs
        """

        file = YamlFile(path)
        file.load()
        return file.Content

    @staticmethod
    def _load_as_binary(path: str) -> dict:

        """
        Loads the content of the file as a simple binary without any additional
        parsing.

        Args:
            path:       Path to the file to load.

        Returns:
            The raw content of the file.

        Authors:
            Attila Kovacs
        """

        with open(path, 'rb') as file:
            return file.read()
