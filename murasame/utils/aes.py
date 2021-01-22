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
Contains the implementation of the AESCipher class.
"""

# Platform Imports
import os
import base64
import hashlib
import binascii

# Dependency Imports
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Murasame Imports
from murasame.exceptions import InvalidInputError

class AESCipher:

    """
    Simple utility class to encode and decode content using AES256.

    Authors:
        Attila Kovacs
    """

    def __init__(self, key: str) -> None:

        """
        Creates a new AESCipher instance.

        Authors:
            Attila Kovacs
        """

        self._key = hashlib.sha256(key.encode()).digest()
        """
        Password to use for encryption and decryption. Always 32 bytes.
        """

    def encrypt(self, content: str) -> bytes:

        """
        Encrypts the content using AES.

        Args:
            content:        The content to encrypt.

        Returns:
            The encrypted content in a base64 encoded format.

        Authors:
            Attila Kovacs
        """

        # Create initialization vector
        #initialization_vector = get_random_bytes(AES.block_size)
        initialization_vector = os.urandom(16)

        # Make sure that the input is properly encoded
        content = content.encode('utf-8')

        # Pad the input to the proper block size
        #content = pad(data_to_pad=content, block_size=AES.block_size)
        padder = padding.PKCS7(128).padder()
        content = padder.update(content)
        content += padder.finalize()

        # Encrypt the data
        cipher = self._create_cipher(initialization_vector)
        encryptor = cipher.encryptor()
        content = encryptor.update(content) + encryptor.finalize()

        # Append the initialization vector to the data
        content = initialization_vector + content

        # Base64 encode the result
        content = base64.b64encode(content)

        return content

    def decrypt(self, content: bytes) -> str:

        """
        Decrypts the content using AES.

        Args:
            encoded_contet:         The encrypted content encoded in a base64
                                    format.

        Raises:
            InvalidInputError:      Raised if the input file is not properly
                                    encoded.

        Returns:
            The decrypted content.

        Authors:
            Attila Kovacs
        """

        # Base64 decode the input data
        try:
            content = base64.b64decode(content)
        except binascii.Error:
            raise InvalidInputError('The input file is not properly encoded.')

        # Retrieve the initialization vector
        initialization_vector = content[:16]

        # Remove the initialization vector from the content
        content = content[16:]

        # Decrypt the data
        cipher = self._create_cipher(initialization_vector)
        decryptor = cipher.decryptor()
        content = decryptor.update(content) + decryptor.finalize()

        # Unpad the data
        unpadder = padding.PKCS7(128).unpadder()
        content = unpadder.update(content)
        content += unpadder.finalize()

        # Decode the content
        content = content.decode('utf-8')

        return content

    def _create_cipher(self, initialization_vector: bytes) -> bytes:

        """
        Creates the Cipher object that will be used.

        Args:
            initialization_vector:      The initialization vector to be used to
                                        create the AES cipher.

        Returns:
            The created cipher object.

        Authors:
            Attila Kovacs
        """

        return Cipher(algorithms.AES(self._key),
                      modes.CBC(initialization_vector),
                      backend=default_backend())
