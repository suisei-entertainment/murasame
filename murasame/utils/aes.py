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

# Runtime Imports
import os
import base64
import hashlib
import binascii

# Dependency Imports
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Murasame Imports
from murasame.exceptions import InvalidInputError

IV_SIZE = 16
"""
Size of the initialization vector.
"""

TAG_SIZE = 16
"""
Size of the GCM tag.
"""

BLCOK_SIZE = 128
"""
AES block size.
"""

class AESCipher:

    """Simple utility class to encode and decode content using AES256.

    Attributes:
        _key (bytes): Password to use for encryption and decryption. Always 32 bytes.

    Authors:
        Attila Kovacs
    """

    def __init__(self, key: str) -> None:

        """Creates a new AESCipher instance.

        Authors:
            Attila Kovacs
        """

        self._key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, content: str) -> bytes:

        """Encrypts the content using AES.

        Args:
            content (str): The content to encrypt.

        Returns:
            bytes: The encrypted content in a base64 encoded format.

        Authors:
            Attila Kovacs
        """

        # Create initialization vector
        initialization_vector = os.urandom(IV_SIZE)

        # Make sure that the input is properly encoded
        content = content.encode('utf-8')

        # Pad the input to the proper block size
        padder = padding.PKCS7(BLCOK_SIZE).padder()
        content = padder.update(content)
        content += padder.finalize()

        # Encrypt the data
        cipher = Cipher(
            algorithms.AES(self._key),
            modes.GCM(initialization_vector))
        encryptor = cipher.encryptor()
        content = encryptor.update(content) + encryptor.finalize()

        # Append the initialization vector and the tag to the data
        content = initialization_vector + encryptor.tag + content

        # Base64 encode the result
        content = base64.b64encode(content)

        return content

    def decrypt(self, content: bytes) -> str:

        """Decrypts the content using AES.

        Args:
            encoded_contet (bytes): The encrypted content encoded in a base64
                format.

        Raises:
            InvalidInputError: Raised if the input file is not properly
                encoded.

        Returns:
            str: The decrypted content.

        Authors:
            Attila Kovacs
        """

        # Base64 decode the input data
        try:
            content = base64.b64decode(content)
        except binascii.Error as error:
            raise InvalidInputError('The input file is not properly encoded.') \
                from error

        # Retrieve the initialization vector
        initialization_vector = content[:IV_SIZE]

        # Remove the initialization vector from the content
        content = content[IV_SIZE:]

        # Retrieve the tag
        tag = content[:TAG_SIZE]

        # Remove the tag from the content
        content = content[TAG_SIZE:]

        # Decrypt the data
        cipher = Cipher(
            algorithms.AES(self._key),
            modes.GCM(initialization_vector, tag))
        decryptor = cipher.decryptor()
        content = decryptor.update(content) + decryptor.finalize()

        # Unpad the data
        unpadder = padding.PKCS7(BLCOK_SIZE).unpadder()
        content = unpadder.update(content)
        content += unpadder.finalize()

        # Decode the content
        content = content.decode('utf-8')

        return content
