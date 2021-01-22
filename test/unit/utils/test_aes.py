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

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils import AESCipher

class TestAESEncryption:

    """
    Contains the unit tests for the content encryption functions.
    """

    def test_content_encrpytion(self):

        """
        Tests that content can be encrpyted and decrypted successfully.
        """

        test_string = 'this is a test'
        key = 'secret test password'

        # STEP #1 - Encrypt and decrypt using the same AESCipher object.
        sut = AESCipher(key)
        encrypted = sut.encrypt(test_string)
        decrypted = sut.decrypt(encrypted)
        assert decrypted == test_string

        # STEP #2 - Encrypt and decrypt using different AESCipher objects
        sut1 = AESCipher(key)
        encrypted = sut1.encrypt(test_string)

        sut2 = AESCipher(key)
        decrypted = sut2.decrypt(encrypted)
        assert decrypted == test_string

