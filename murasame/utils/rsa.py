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
Contains the implementation of the RSA class.
"""

# Runtime Imports
import os
import base64

from enum import IntEnum
from typing import Callable

# Dependency Imports
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

# Murasame Imports
from murasame.exceptions import InvalidInputError

class RSAKeyLengths(IntEnum):

    """List of supported RSA key lengths.

    Attributes:
        KEY_LENGTH_2048: 2048 bit key

        KEY_LENGTH_4096: 4096 bit key

    Authors:
        Attila Kovacs
    """

    KEY_LENGTH_2048 = 2048
    KEY_LENGTH_4096 = 4096

class RSAPublic:

    """Represents a single RSA public key.

    Attributes:
        _public_key (object): The public key object.

    Authors:
        Attila Kovacs
    """

    @property
    def Key(self) -> object:

        """Provides access to the public key.

        Authors:
            Attila Kovacs
        """

        return self._public_key

    def __init__(self, key_path: str) -> None:

        """Creates a new RSAPublicKey instance.

        Args:
            key_path (str): Path to the file containing the public key.

        Raises:
            InvalidInputError: Raised when the key file doesn't exist.

        Authors:
            Attila Kovacs
        """

        self._public_key = None

        # Check that the file actually exists
        key_path = os.path.abspath(os.path.expanduser(key_path))
        if not os.path.isfile(key_path):
            raise InvalidInputError(f'Public key {key_path} does not exist.')

        # Load the public key
        with open(key_path, "rb") as key_file:
            self._public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend())

    def verify(self,
               message: str,
               signature: str,
               hashing_algorithm: Callable = hashes.SHA512,
               encoded: bool = False) -> bool:

        """Verifies a given message using the stored public key.

        Args:
            message (str): The message to verify.

            signature (str): The signature of the message.

            hashing_algorithm (Callable): The hashing algorithm to use.

            encoded (bool): Whether or not the signature is base64 encoded.

        Return:
            bool: 'True' if the message was successfully verified, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        # Decode the signature if it's encoded
        if encoded:
            signature = base64.b64decode(signature)

        # Verify the message
        try:
            self._public_key.verify(
                signature,
                bytes(message, encoding='utf-8'),
                padding.PSS(mgf=padding.MGF1(hashing_algorithm()),
                            salt_length=padding.PSS.MAX_LENGTH),
                hashing_algorithm())
        except InvalidSignature:
            return False

        return True

    def encrypt(self,
                message: str,
                hashing_algorithm: Callable = hashes.SHA512) -> str:

        """Encrypts the given message using the public key.

        Args:
            message (str): The message to encrypt.

            hashing_algorithm (Callable): The hashing algorithm to use.

        Returns:
            str: The encrypted message as a string.

        Authors:
            Attila Kovacs
        """

        return self._public_key.encrypt(
            bytes(message, encoding='utf-8'),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashing_algorithm()),
                         algorithm=hashing_algorithm(),
                         label=None))

class RSAPrivate:

    """Represents a single RSA private key.

    Attributes:
        _private_key (object): The private key object.

    Authors:
        Attila Kovacs
    """

    @property
    def Key(self) -> object:

        """Provides access to the private key.

        Authors:
            Attila Kovacs
        """

        return self._private_key

    def __init__(self,
                 key_path: str,
                 cb_retrieve_password: Callable = None) -> None:

        """Creates a new RSAPrivateKey instance.

        Args:
            key_path (str): Path to the file containing the private key.

            cb_retrieve_password (Callable): Callback function that when
                called, should return the password to be used to protect the
                key when saved to disk.

        Raises:
            InvalidInputError: Raised when the key file doesn't exist.

        Authors:
            Attila Kovacs
        """

        self._private_key = None

        # Check that the file actually exists
        key_path = os.path.abspath(os.path.expanduser(key_path))
        if not os.path.isfile(key_path):
            raise InvalidInputError(f'Private key {key_path} does not exist.')

        # Load the key
        if cb_retrieve_password is not None:

            with open(key_path, "rb") as key_file:
                self._private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=cb_retrieve_password(),
                    backend=default_backend())

        else:

            with open(key_path, "rb") as key_file:
                self._private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend())

    def sign(self,
             message: str,
             hashing_algorithm: Callable = hashes.SHA512,
             encode: bool = False) -> str:

        """Signs the given message using the private key.

        Args:
            message (str): The message to sign.

            hashing_algorithm (Callable): The hashing algorithm to use.

            encode (bool): Whether or not the signature should be returned in
                a base64 encoded form.

        Returns:
            str: The message signature.

        Authors:
            Attila Kovacs
        """

        signature = ''

        # Generate the signature
        signature = self._private_key.sign(
            bytes(message, encoding='utf-8'),
            padding.PSS(mgf=padding.MGF1(hashing_algorithm()),
                        salt_length=padding.PSS.MAX_LENGTH),
            hashing_algorithm())

        if encode:
            signature = base64.b64encode(signature)

        return signature

    def decrypt(self,
                message: str,
                hashing_algorithm: Callable = hashes.SHA512) -> str:

        """Decrypts the given message using the private key.

        Args:
            message (str): The message to decrypt.

            hashing_algorithm (Callable): The hashing algorithm to use.

        Returns:
            str: The decrypted message.

        Authors:
            Attila Kovacs
        """

        decrypted = self._private_key.decrypt(
            message,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashing_algorithm()),
                         algorithm=hashing_algorithm(),
                         label=None))

        return str(decrypted, encoding='utf-8')

class RSAKeyGenerator:

    """Utility class to generate an RSA key pair.

    Attributes:
        _cb_retrieve_password (Callable): Callback function to retrieve the
            password to be used to encrypt the key.

        _private_key (object): The generated private key.

    Authors:
        Attila Kovacs
    """

    @property
    def PrivateKey(self) -> object:

        """
        Provides access to the private key.

        Authors:
            Attila Kovacs
        """

        return self._private_key

    def __init__(self,
                 key_length: RSAKeyLengths = RSAKeyLengths.KEY_LENGTH_4096,
                 cb_retrieve_password: Callable = None) -> None:

        """
        Creates a new RSAKeyGenerator instance.

        Args:
            key_length (RSAKeyLengths): The length of the modulus in bits.

            cb_retrieve_password (Callable): Callback function that when
                called, should return the password to be used to protect the
                key when saved to disk.

        Authors:
            Attila Kovacs
        """

        self._cb_retrieve_password = cb_retrieve_password

        # Generate the key
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_length,
            backend=default_backend())

    def save_key_pair(self,
                      private_key_path: str,
                      public_key_path: str) -> None:

        """Saves both the public and private keys to disk.

        Args:
            private_key_path (str): Path to the file where the private key will
                be saved.

            public_key_path (str): Path to the file where the public key will
                be saved.

        Authors:
            Attila Kovacs
        """

        self.save_private_key(private_key_path=private_key_path)
        self.save_public_key(public_key_path=public_key_path)

    def save_private_key(self, private_key_path: str) -> None:

        """Saves the private key to disk.

        Args:
            private_key_path (str): Path to the file where the private key will
                be saved.

        Authors:
            Attila Kovacs
        """

        pem = None

        if self._cb_retrieve_password:

            pem = self._private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(
                    self._cb_retrieve_password()))

        else:

            pem = self._private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption())

        lines = pem.splitlines()

        with open(private_key_path, 'wb') as file:
            for line in lines:
                file.write(line)
                file.write(b'\n')

    def save_public_key(self, public_key_path: str) -> None:

        """Saves the public key to disk.

        Args:
            public_key_path (str): Path to the file where the public key will
                be saved.

        Authors:
            Attila Kovacs
        """

        public_key = self._private_key.public_key()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

        lines = pem.splitlines()

        with open(public_key_path, 'wb') as file:
            for line in lines:
                file.write(line)
                file.write(b'\n')

class RSASigner:

    """Utility class to help with signing messages.

    Attributes:
        _hashing_algorithm (Callable): The hashing algorithm to use.

        _private_key (RSAPrivate): The private key to use.

    Authors:
        Attila Kovacs
    """

    def __init__(self,
                 private_key_path: str = None,
                 private_key: RSAPrivate = None,
                 cb_retrieve_password: Callable = None,
                 hashing_algorithm: Callable = hashes.SHA512) -> None:

        """Creates a new RSASigner instance.

        Args:
            private_key_path (str): Path to the file containing the private
                key.

            private_key (RSAPrivate): An existing private key object to use
                for signing.

            cb_retrieve_password (Callable): Callback function that when
                called, should return the password to be used to protect the
                key when saved to disk.

            hashing_algorithm (Callable): The hashing algorithm to use.

        Authors:
            Attila Kovacs
        """

        self._hashing_algorithm = hashing_algorithm
        self._private_key = None

        if private_key is not None:
            self._private_key = private_key
        else:
            self._private_key = RSAPrivate(
                key_path=private_key_path,
                cb_retrieve_password=cb_retrieve_password)

    def sign(self, message: str, encode: bool = False) -> bytes:

        """Signs the given message using the private key.

        Args:
            message (str): The message to sign.

            encode (bool): Whether or not the signature should be returned in a
                base64 encoded form.

        Returns:
            bytes: The message signature.

        Authors:
            Attila Kovacs
        """

        return self._private_key.sign(
            message, self._hashing_algorithm, encode=encode)

class RSAVerifier:

    """Utility class to verify messages using a public key.

    Attributes:
        _hashing_algorithm (Callable): The hashing algorithm to use.

        _public_key (RSAPublic): The public key to use for verifying the
            messages.

    Authors:
        Attila Kovacs
    """

    def __init__(
            self,
            public_key_path: str = None,
            public_key: str = None,
            hashing_algorithm: Callable = hashes.SHA512) -> None:

        """Creates a new RSAVerifier instance.

        Args:
            public_key_path (str): Path to the file containing the public key.

            hashing_algorithm (Callable): The hashing algorithm to use.

        Authors:
            Attila Kovacs
        """

        self._hashing_algorithm = hashing_algorithm
        self._public_key = None

        if public_key is not None:
            self._public_key = public_key
        else:
            self._public_key = RSAPublic(key_path=public_key_path)

    def verify(
        self,
        message: str,
        signature: bytes,
        encoded: bool = False) -> bool:

        """Verifies a given message using the stored public key.

        Args:
            message (str): The message to verify.

            signature (bytes): The signature of the message.

            encoded (bool): Whether or not the signature is base64 encoded.

        Authors:
            Attila Kovacs
        """

        return self._public_key.verify(
            message=message,
            signature=signature,
            hashing_algorithm=self._hashing_algorithm,
            encoded=encoded)

class RSAEncryptor:

    """Utility class to encrypt a string using an RSA private key.

    Attributes:
        _hashing_algorithm (Callable): The hashing algorithm to use.

        _public_key (RSAPublic): The public key to use for the encryption.

    Authors:
        Attila Kovacs
    """

    def __init__(
            self,
            public_key_path: str = None,
            public_key: RSAPublic = None,
            hashing_algorithm: Callable = hashes.SHA512) -> None:

        """Creates a new RSAEncryptor instance.

        Args:
            public_key_path (str): Path to the file containing the RSA public
                key.

            public_key (RSAPublic): The public key object to use for
                encryption.

            hashing_algorithm (Callable): The hashing algorithm to use.

        Authors:
            Attila Kovacs
        """

        self._hashing_algorithm = hashing_algorithm
        self._public_key = None

        if public_key is not None:
            self._public_key = public_key
        else:
            self._public_key = RSAPublic(key_path=public_key_path)

    def encrypt(self, message: str) -> str:

        """Encrypts the given message using the private key.

        Args:
            message (str): The message to encrypt.

        Returns:
            str: The encrypted message.

        Authors:
            Attila Kovacs
        """

        return self._public_key.encrypt(
            message=message,
            hashing_algorithm=self._hashing_algorithm)

class RSADecryptor:

    """Utility class to decrypt a string using an RSA public key.

    Attributes:
        _hashing_algorithm (Callable): The hashing algorithm to use.

        _private_key (RSAPrivate): The private key to use for the decrpytion.

    Authors:
        Attila Kovacs
    """

    def __init__(
            self,
            private_key_path: str = None,
            private_key: RSAPublic = None,
            cb_retrieve_password: Callable = None,
            hashing_algorithm: Callable = hashes.SHA512) -> None:

        """Creates a new RSADecryptor instance.

        Args:
            private_key_path (str): Path to the file containing the RSA private
                key.

            private_key (RSAPrivate): The private key to use for decrpyion.

            cb_retrieve_password (Callable): Callback function that when
                called, should return the password to be used to protect the
                key when saved to disk.

            hashing_algorithm (Callable): The hashing algorithm to use.

        Authors:
            Attila Kovacs
        """

        self._hashing_algorithm = hashing_algorithm
        self._private_key = None

        if private_key is not None:
            self._private_key = private_key
        else:
            self._private_key = RSAPrivate(
                key_path=private_key_path,
                cb_retrieve_password=cb_retrieve_password)

    def decrypt(self, message: str) -> str:

        """Decrypts the given string using the public key.

        Args:
            message (str): The message to decrypt.

        Returns:
            str: The decrypted message.

        Authors:
            Attila Kovacs
        """

        return self._private_key.decrypt(
            message=message,
            hashing_algorithm=self._hashing_algorithm)
