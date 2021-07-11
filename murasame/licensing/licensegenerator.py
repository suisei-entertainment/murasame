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
Contains the implementation of the LicenseGenerator class.
"""

# Runtime Imports
import json

# Murasame Imports
from murasame.utils import JsonFile, RSAPrivate

class LicenseGenerator:

    """Generates license files.

    License files are structured the following way:

    {
        "license":
        {
            "key": "8c6f4d93-e848-468a-8465-bbad9f66e4f1",
            "owner": "96016c79-b0f6-4432-9872-7c4cdad2001a",
            "type": "production",
            "features":
            {
                "a4549bab-f116-4fb1-b553-3b6d9880cfed":
                {

                },
                "7b613fcf-df64-4a92-ad6e-6e3b3870427e":
                {

                }
            }
        },
        "signature": "base64 encoded license signature"

    }

    Attributes:
        _private_key (RSAPrivate): The private key to use to sign the password.

        _cb_retrieve_encryption_password (Callable) : Callback function that is
            called to retrieve the password used to encrypt the license file.

    Authors:
        Attila Kovacs
    """

    def __init__(self,
                 private_key_path: str = None,
                 private_key: 'RSAPrivate' = None,
                 cb_retrieve_key_password: 'Callable' = None,
                 cb_retrieve_encryption_password: 'Callable' = None) -> None:

        """Creates a new LicenseGenerator instance.

        Args:
            private_key_path (str): Path to the private key to use.

            private_key (RSAPrivate): The private key to use.

            cb_retrieve_key_password (Callable): Callback function that is
                called to retrieve the password required to decrypt the license
                file.

            cb_retrieve_encryption_password (Callable): Callback function that
                is called to retrieve the encryption password that is used to
                encrypt the license file.

        Authors:
            Attila Kovacs
        """

        self._private_key = None
        self._cb_retrieve_encryption_password = cb_retrieve_encryption_password

        if private_key is not None:
            self._private_key = private_key
        else:
            self._private_key = RSAPrivate(
                key_path=private_key_path,
                cb_retrieve_password=cb_retrieve_key_password)

    def generate(
            self,
            output_path: str,
            license_descriptor: 'LicenseDescriptor') -> None:

        """Generates the license file and saves it to disk.

        Args:
            output_path (str): Path where the generated license file will be
                saved.

            license_descriptor (LicenseDescriptor): The license descriptor to
                generate the license file for.

        Authors:
            Attila Kovacs
        """

        descriptor = license_descriptor.serialize()
        signature = self._private_key.sign(
            message=json.dumps(descriptor), encode=True)
        signature = signature.decode('utf-8')

        license_content = \
        {
            'license': descriptor,
            'signature': signature
        }

        license_file = JsonFile(
            path=output_path,
            cb_retrieve_key=self._cb_retrieve_encryption_password)
        license_file.overwrite_content(content=license_content)
        license_file.save()
