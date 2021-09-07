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
Contains the unit tests of the RSA handling utilities.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils import (
    RSAKeyGenerator,
    RSAKeyLengths,
    RSAPublic,
    RSAPrivate,
    RSASigner,
    RSAVerifier,
    RSAEncryptor,
    RSADecryptor)

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

def get_password() -> str:

    """Returns the test password to be used in the unit tests.

    Authors:
        Attila Kovacs
    """

    return b'testpassword'

class TestRSA:

    """Contains the RSA related unit tests.

    Authors:
        Attila Kovacs
    """

    def test_2048_bit_key_generation_without_encryption(self) -> None:

        """Tests that a 2048 bit unencrypted RSA key can be generated.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048)

        assert sut.PrivateKey is not None

    def test_4096_bit_key_generation_without_encryption(self) -> None:

        """Tests that a 4096 bit unencrypted RSA key can be generated.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        assert sut.PrivateKey is not None

    def test_2048_bit_key_generation_with_encryption(self) -> None:

        """Tests that a 2048 bit encrypted RSA key can be generated.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        assert sut.PrivateKey is not None

    def test_4096_bit_key_generation_with_encryption(self) -> None:

        """Tests that a 4096 bit encrypted RSA key can be generated.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096,
            cb_retrieve_password=get_password)

        assert sut.PrivateKey is not None


    def test_saving_2048_bit_public_key(self) -> None:

        """Tests that the generated 2048 bit public key can be saved to disk.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048)

        sut.save_public_key(
            public_key_path=f'{TEST_FILES_DIRECTORY}/public_2048_1.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/public_2048_1.pem')

    def test_saving_4096_bit_public_key(self) -> None:

        """Tests that the generated 4096 bit public key can be saved to disk.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        sut.save_public_key(
            public_key_path=f'{TEST_FILES_DIRECTORY}/public_4096_1.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/public_4096_1.pem')

    def test_saving_2048_bit_unencrypted_private_key(self) -> None:

        """Tests that the generated 2048 bit unencrypted private key can be
        saved to disk.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048)

        sut.save_private_key(
            private_key_path=f'{TEST_FILES_DIRECTORY}/private_2048_1.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/private_2048_1.pem')

    def test_saving_4096_bit_unencrypted_private_key(self) -> None:

        """Tests that the generated 4096 bit unencrypted private key can be
        saved to disk.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        sut.save_private_key(
            private_key_path=f'{TEST_FILES_DIRECTORY}/private_4096_1.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/private_4096_1.pem')

    def test_saving_2048_bit_encrypted_private_key(self) -> None:

        """Tests that the generated 2048 bit encrypted private key can be saved
        to disk.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        sut.save_private_key(
            private_key_path=f'{TEST_FILES_DIRECTORY}/private_2048_2.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/private_2048_2.pem')

    def test_saving_4096_bit_encrypted_private_key(self) -> None:

        """Tests that the generated 4096 bit encrypted private key can be saved
        to disk.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096,
            cb_retrieve_password=get_password)

        sut.save_private_key(
            private_key_path=f'{TEST_FILES_DIRECTORY}/private_4096_2.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/private_4096_2.pem')

    def test_saving_2048_bit_key_pair_unencrypted(self) -> None:

        """Tests that a 2048 bit RSA key pair can be saved unencrypted.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048)

        sut.save_key_pair(
            private_key_path=f'{TEST_FILES_DIRECTORY}/pair_private_2048_1.pem',
            public_key_path=f'{TEST_FILES_DIRECTORY}/pair_public_2048_1.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/pair_private_2048_1.pem')
        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/pair_public_2048_1.pem')

    def test_saving_4096_bit_key_pair_unencrypted(self) -> None:

        """Tests that a 4096 bit RSA key pair can be saved unencrypted.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        sut.save_key_pair(
            private_key_path=f'{TEST_FILES_DIRECTORY}/pair_private_4096_1.pem',
            public_key_path=f'{TEST_FILES_DIRECTORY}/pair_public_4096_1.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/pair_private_4096_1.pem')
        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/pair_public_4096_1.pem')

    def test_saving_2048_bit_key_pair_encrypted(self) -> None:

        """Tests that a 2048 bit RSA key pair can be saved encrypted.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        sut.save_key_pair(
            private_key_path=f'{TEST_FILES_DIRECTORY}/pair_private_2048_2.pem',
            public_key_path=f'{TEST_FILES_DIRECTORY}/pair_public_2048_2.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/pair_private_2048_2.pem')
        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/pair_public_2048_2.pem')

    def test_saving_4096_bit_key_pair_encrypted(self) -> None:

        """Tests that a 4096 bit RSA key pair can be saved encrypted.

        Authors:
            Attila Kovacs
        """

        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096,
            cb_retrieve_password=get_password)

        sut.save_key_pair(
            private_key_path=f'{TEST_FILES_DIRECTORY}/pair_private_4096_2.pem',
            public_key_path=f'{TEST_FILES_DIRECTORY}/pair_public_4096_2.pem')

        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/pair_private_4096_2.pem')
        assert os.path.isfile(f'{TEST_FILES_DIRECTORY}/pair_public_4096_2.pem')

    def test_loading_existing_public_key(self) -> None:

        """Tests that an existing public key can be loaded.

        Authors:
            Attila Kovacs
        """

        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        generator.save_public_key(
            public_key_path=f'{TEST_FILES_DIRECTORY}/load_test_public.pem')

        sut = RSAPublic(key_path=f'{TEST_FILES_DIRECTORY}/load_test_public.pem')

        assert sut.Key is not None

    def test_loading_non_existing_public_key(self) -> None:

        """Tests that a non-existent public key cannot be loaded.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = RSAPublic(key_path='/non/existing/path')

    def test_loading_unencrypted_private_key(self) -> None:

        """Tests that a generated private key can be loaded.

        Authors:
            Attila Kovacs
        """

        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        generator.save_private_key(
            private_key_path=f'{TEST_FILES_DIRECTORY}/load_test_private.pem')

        sut = RSAPrivate(
            key_path=f'{TEST_FILES_DIRECTORY}/load_test_private.pem')

        assert sut.Key is not None

    def test_loading_encrypted_private_key(self) -> None:

        """Tests that a generated encrypted private key can be loaded.

        Authors:
            Attila Kovacs
        """

        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096,
            cb_retrieve_password=get_password)

        generator.save_private_key(
            private_key_path=f'{TEST_FILES_DIRECTORY}/load_test_private.pem')

        sut = RSAPrivate(
            key_path=f'{TEST_FILES_DIRECTORY}/load_test_private.pem',
            cb_retrieve_password=get_password)

        assert sut.Key is not None

    def test_loading_non_existing_private_key(self) -> None:

        """Tests that a non-existing private key cannot be loaded.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = RSAPrivate(key_path='/non/existing/path')

    def test_message_verification_without_encoding(self) -> None:

        """Tests that messages can be signed and verified using an RSA key pair
        without encoding.

        Authors:
            Attila Kovacs.
        """

        sut_signer = RSASigner(
            private_key_path=f'{TEST_FILES_DIRECTORY}/signing_private.pem')

        sut_verifier = RSAVerifier(
            public_key_path=f'{TEST_FILES_DIRECTORY}/signing_public.pem')

        message = 'test message'

        signature = sut_signer.sign(message)
        assert sut_verifier.verify(message, signature)

    def test_message_verification_with_encoding(self) -> None:

        """Tests that messages can be signed and verified using an RSA key pair
        with encoding.

        Authors:
            Attila Kovacs.
        """

        sut_signer = RSASigner(
            private_key_path=f'{TEST_FILES_DIRECTORY}/signing_private.pem')

        sut_verifier = RSAVerifier(
            public_key_path=f'{TEST_FILES_DIRECTORY}/signing_public.pem')

        message = 'test message'

        signature = sut_signer.sign(message=message, encode=True)
        assert sut_verifier.verify(
            message=message, signature=signature, encoded=True)

    def test_message_encryption(self) -> None:

        """Tests that messages can be encrypted and decrypted using an RSA key
        pair.

        Authors:
            Attila Kovacs
        """

        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        generator.save_key_pair(
            private_key_path=f'{TEST_FILES_DIRECTORY}/encryption_private.pem',
            public_key_path=f'{TEST_FILES_DIRECTORY}/encryption_public.pem')

        sut_encryptor = RSAEncryptor(
            public_key_path=f'{TEST_FILES_DIRECTORY}/signing_public.pem')

        sut_decryptor = RSADecryptor(
            private_key_path=f'{TEST_FILES_DIRECTORY}/signing_private.pem')

        message = 'test message'

        assert message ==sut_decryptor.decrypt(sut_encryptor.encrypt(message))
