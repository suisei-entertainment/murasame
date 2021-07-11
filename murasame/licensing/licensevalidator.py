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
Contains the implementation of the LicenseValidator class.
"""

# Platform Import
import json

# Murasame Imports
from murasame.utils import RSAPublic, JsonFile

class LicenseValidator:

    """Utility class to validate a license.

    Attributes:
        _public_key (RSAPublic): The public key to use for the validation.

    Authors:
        Attila Kovacs
    """

    def __init__(self,
                 public_key: 'RSAPublic' = None,
                 public_key_path: str = None) -> None:

        """Creates a new LicenseValidator instance.

        Args:
            public_key (RSAPublic): The public key object to use for validation.
            public_key_path (str): Path to the file containing the public key.

        Authors:
            Attila Kovacs
        """

        self._public_key = None

        if public_key is not None:
            self._public_key = public_key
        else:
            self._public_key = RSAPublic(key_path=public_key_path)

    def validate(self,
                 license_path: str,
                 cb_retrieve_password: 'Callable' = None) -> bool:

        """Validates the given license file using the public key.

        Args:
            license_path (str): Path to the license file.
            cb_retrieve_password (Callable): Callback function that is called
                to retrieve the password required to decrypt the license file.

        Returns:
            bool: 'True' if the given license is valid, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        # Load and decrypt the license file
        license_file = JsonFile(path=license_path,
                                cb_retrieve_key=cb_retrieve_password)
        license_file.load()

        # Get the string representation of the license
        try:
            license_string = json.dumps(license_file.Content['license'])
        except KeyError:
            return False

        # Get the signature
        try:
            signature = license_file.Content['signature']
            signature = bytes(signature, 'utf-8')
        except KeyError:
            return False

        if not self._public_key.verify(
                message=license_string, signature=signature, encoded=True):
            return False

        return True
