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

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

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

KEY_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles'))

def get_password():

    """
    Returns the test password to be used in the unit tests.
    """

    return b'testpassword'

class TestRSA:

    """
    Contains the RSA related unit tests.
    """

    def test_key_generation(self):

        """
        Tests that an RSA key can be generated.
        """

        # STEP #1 - 2048 bit RSA key can be generated without encryption
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048)

        assert sut.PrivateKey is not None

        # STEP #2 - 4096 bit RSA key can be generated without encryption
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        assert sut.PrivateKey is not None

        # STEP #3 - 2048 bit RSA key can be generated with encryption
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        assert sut.PrivateKey is not None

        # STEP #4 - 4096 bit RSA key can be generated with encryption
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096,
            cb_retrieve_password=get_password)

        assert sut.PrivateKey is not None


    def test_saving_public_key(self):

        """
        Tests that the generated public key can be saved to disk.
        """

        # STEP #1 - 2048 bit RSA public key can be saved
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048)

        sut.save_public_key(
            public_key_path='{}/public_2048_1.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/public_2048_1.pem'.format(KEY_PATH))

        # STEP #2 - 4096 bit RSA public key can be saved
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        sut.save_public_key(
            public_key_path='{}/public_4096_1.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/public_4096_1.pem'.format(KEY_PATH))

    def test_saving_private_key(self):

        """
        Tests that the generated private key can be saved to disk.
        """

        # STEP #1 - 2048 bit RSA public key can be saved unencrypted
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048)

        sut.save_private_key(
            private_key_path='{}/private_2048_1.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/private_2048_1.pem'.format(KEY_PATH))

        # STEP #2 - 4096 bit RSA public key can be saved unencrypted
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        sut.save_private_key(
            private_key_path='{}/private_4096_1.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/private_4096_1.pem'.format(KEY_PATH))

        # STEP #3 - 2048 bit RSA public key can be saved encrypted
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        sut.save_private_key(
            private_key_path='{}/private_2048_2.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/private_2048_2.pem'.format(KEY_PATH))

        # STEP #4 - 4096 bit RSA public key can be saved encrypted
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096,
            cb_retrieve_password=get_password)

        sut.save_private_key(
            private_key_path='{}/private_4096_2.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/private_4096_2.pem'.format(KEY_PATH))

    def test_saving_key_pair(self):

        """
        Tests that an RSA key pair can be saved.
        """

        # STEP #1 - 2048 bit key pair can be saved unencrypted
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048)

        sut.save_key_pair(
            private_key_path='{}/pair_private_2048_1.pem'.format(KEY_PATH),
            public_key_path='{}/pair_public_2048_1.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/pair_private_2048_1.pem'.format(KEY_PATH))
        assert os.path.isfile('{}/pair_public_2048_1.pem'.format(KEY_PATH))

        # STEP #2 - 4096 bit key pair can be saved unencrypted
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        sut.save_key_pair(
            private_key_path='{}/pair_private_4096_1.pem'.format(KEY_PATH),
            public_key_path='{}/pair_public_4096_1.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/pair_private_4096_1.pem'.format(KEY_PATH))
        assert os.path.isfile('{}/pair_public_4096_1.pem'.format(KEY_PATH))

        # STEP #3 - 2048 bit key pair can be saved encrypted
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        sut.save_key_pair(
            private_key_path='{}/pair_private_2048_2.pem'.format(KEY_PATH),
            public_key_path='{}/pair_public_2048_2.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/pair_private_2048_2.pem'.format(KEY_PATH))
        assert os.path.isfile('{}/pair_public_2048_2.pem'.format(KEY_PATH))

        # STEP #4 - 4096 bit key pair can be saved encrypted
        sut = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096,
            cb_retrieve_password=get_password)

        sut.save_key_pair(
            private_key_path='{}/pair_private_4096_2.pem'.format(KEY_PATH),
            public_key_path='{}/pair_public_4096_2.pem'.format(KEY_PATH))

        assert os.path.isfile('{}/pair_private_4096_2.pem'.format(KEY_PATH))
        assert os.path.isfile('{}/pair_public_4096_2.pem'.format(KEY_PATH))

    def test_public_key_loading(self):

        """
        Tests that a generated public key can be loaded.
        """

        # STEP #1 - Existing key file can be loaded
        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        generator.save_public_key(
            public_key_path='{}/load_test_public.pem'.format(KEY_PATH))

        sut = RSAPublic(key_path='{}/load_test_public.pem'.format(KEY_PATH))

        assert sut.Key is not None

        # STEP #2 - InvalidInputError is raised when trying to open a
        #           non-existing key file.
        with pytest.raises(InvalidInputError):
            sut = RSAPublic(key_path='/non/existing/path')

    def test_private_key_loading(self):

        """
        Tests that a generated private key can be loaded.
        """

        # STEP #1 - Unencrypted RSA private key can be loaded
        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        generator.save_private_key(
            private_key_path='{}/load_test_private.pem'.format(KEY_PATH))

        sut = RSAPrivate(
            key_path='{}/load_test_private.pem'.format(KEY_PATH))

        assert sut.Key is not None

        # STEP #2 - Encrypted RSA private key can be loaded
        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096,
            cb_retrieve_password=get_password)

        generator.save_private_key(
            private_key_path='{}/load_test_private.pem'.format(KEY_PATH))

        sut = RSAPrivate(
            key_path='{}/load_test_private.pem'.format(KEY_PATH),
            cb_retrieve_password=get_password)

        assert sut.Key is not None

        # STEP #3 - InvalidInputError is raised when trying to open a
        #           non-existing key file.
        with pytest.raises(InvalidInputError):
            sut = RSAPrivate(key_path='/non/existing/path')

    def test_message_verification(self):

        """
        Tests that messages can be signed and verified using an RSA key pair.
        """

        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        generator.save_key_pair(
            private_key_path='{}/signing_private.pem'.format(KEY_PATH),
            public_key_path='{}/signing_public.pem'.format(KEY_PATH))

        sut_signer = RSASigner(
            private_key_path='{}/signing_private.pem'.format(KEY_PATH))

        sut_verifier = RSAVerifier(
            public_key_path='{}/signing_public.pem'.format(KEY_PATH))

        message = 'test message'

        # STEP #1 - Test without encoding
        signature = sut_signer.sign(message)
        assert sut_verifier.verify(message, signature)

        # #STEP #2 - Test with encoding
        signature = sut_signer.sign(message=message, encode=True)
        assert sut_verifier.verify(
            message=message, signature=signature, encoded=True)

    def test_message_encryption(self):

        """
        Tests that messages can be encrypted and decrypted using an RSA key
        pair.
        """

        generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_4096)

        generator.save_key_pair(
            private_key_path='{}/encryption_private.pem'.format(KEY_PATH),
            public_key_path='{}/encryption_public.pem'.format(KEY_PATH))

        sut_encryptor = RSAEncryptor(
            public_key_path='{}/signing_public.pem'.format(KEY_PATH))

        sut_decryptor = RSADecryptor(
            private_key_path='{}/signing_private.pem'.format(KEY_PATH))

        message = 'test message'

        assert message ==sut_decryptor.decrypt(sut_encryptor.encrypt(message))
