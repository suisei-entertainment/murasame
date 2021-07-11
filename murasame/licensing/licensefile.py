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
Contains the implementation of the LicenseFile class.
"""

# Murasame Imports
from murasame.exceptions import InvalidInputError, InvalidLicenseKeyError
from murasame.utils import JsonFile
from murasame.licensing.licensedescriptor import LicenseDescriptor

class LicenseFile:

    """Represents a single license file loaded into memory.

    Attributes:
        _signature (str): The signature of the license file.
        _license (LicenseDescriptor): The license descriptor.

    Authors:
        Attila Kovacs
    """

    @property
    def Signature(self) -> bytes:

        """Provides access to the signature of the license.

        Authors:
            Attila Kovacs
        """

        return self._signature

    @property
    def License(self) -> 'LicenseDescriptor':

        """Provides access to the license descriptor.
        """

        return self._license

    def __init__(self,
                 license_file_path: str,
                 cb_retrieve_password: 'Callable' = None) -> None:

        """Creates a new LicenseFile instance.

        Args:
            license_file_path (str): Path to the license file.
            cb_retrieve_password (Callable): Callback function that is called
                to retrieve the password required to decrypt the license file.

        Authors:
            Attila Kovacs
        """

        self._signature = None
        self._license = None

        self._load_license_file(license_file_path, cb_retrieve_password)

    def _load_license_file(self,
                           license_file_path: str,
                           cb_retrieve_password: 'Callable') -> None:

        """Loads and decrypts the license file.

        Args:
            license_file_path (str): Path to the license file.
            cb_retrieve_password (Callable): Callback function that is called
                to retrieve the password required to decrypt the license file.

        Authors:
            Attila Kovacs
        """

        # Load the file
        license_file = JsonFile(path=license_file_path,
                                cb_retrieve_key=cb_retrieve_password)
        try:
            license_file.load()
        except InvalidInputError as exception:
            raise InvalidLicenseKeyError(
                f'Failed to load license file from '
                f'{license_file_path}.') from exception

        # Retrieve the signature
        try:
            self._signature = license_file.Content['signature']
        except KeyError as exception:
            raise InvalidLicenseKeyError(
                f'No signature found in license file '
                f'{license_file_path}.') from exception

        # Retrieve the license descriptor
        descriptor = None

        try:
            descriptor = license_file.Content['license']
        except KeyError as exception:
            raise InvalidLicenseKeyError(
                f'No license descriptor found in license '
                f'file {license_file_path}.') from exception

        # Build the descriptor
        try:
            self._license = LicenseDescriptor(
                license_key=descriptor['key'],
                owner_id=descriptor['owner'],
                license_type=descriptor['type'])

            features = descriptor['features']

            for key, metadata in features.items():
                self._license.add_feature(
                    feature_id=key,
                    metadata=metadata)

        except KeyError as exception:
            raise InvalidLicenseKeyError(
                f'Malformed license descriptor in license '
                f'file {license_file_path}.') from exception
