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
Contains the data used for RSA testing.
"""

# Murasame Imports
from murasame.utils.rsa import RSAKeyLengths, RSAKeyGenerator

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

def create_rsa_data():

    generator = RSAKeyGenerator(
        key_length=RSAKeyLengths.KEY_LENGTH_4096)

    generator.save_key_pair(
        private_key_path=f'{TEST_FILES_DIRECTORY}/signing_private.pem',
        public_key_path=f'{TEST_FILES_DIRECTORY}/signing_public.pem')
