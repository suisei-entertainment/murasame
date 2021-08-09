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
Contains the test data for the licensing tests.
"""

# Murasame Imports
from murasame.utils.rsa import RSAKeyGenerator, RSAKeyLengths

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

def get_password():
    return b'testpassword'

def create_test_license_key():

    """
    Creates data needed for license testing.

    Authors:
        Attila Kovacs
    """

    key_generator = RSAKeyGenerator(
        key_length=RSAKeyLengths.KEY_LENGTH_2048,
        cb_retrieve_password=get_password)

    key_generator.save_key_pair(
        private_key_path=f'{TEST_FILES_DIRECTORY}/license_private.pem',
        public_key_path=f'{TEST_FILES_DIRECTORY}/license_public.pem')
