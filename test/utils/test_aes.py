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
Contains the unit tests of the basic AES encryption and decryption functions.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.utils import AESCipher

TEST_STRING = 'this is a test'

KEY = 'secret test password'

class TestAESEncryption:

    """
    Contains the unit tests for the content encryption functions.

    Authors:
        Attila Kovacs
    """

    def test_content_encrpytion_same_cipher(self):

        """
        Tests that content can be encrypted and decrypted successfully with
        the same AES cipher.

        Authors:
            Attila Kovacs
        """

        sut = AESCipher(KEY)
        encrypted = sut.encrypt(TEST_STRING)
        decrypted = sut.decrypt(encrypted)
        assert decrypted == TEST_STRING

    def test_content_encryption_different_ciphers(self):

        """
        Tests that content can be encrypted and decrypted successfully with
        different AES cipher objects.

        Authors:
            Attila Kovacs
        """

        sut1 = AESCipher(KEY)
        encrypted = sut1.encrypt(TEST_STRING)

        sut2 = AESCipher(KEY)
        decrypted = sut2.decrypt(encrypted)
        assert decrypted == TEST_STRING
