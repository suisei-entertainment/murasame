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
Contains the test data for the certificate tests.
"""

# Runtime Imports
import os
import subprocess

# Murasame Imports
from murasame.utils.rsa import RSAKeyGenerator

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

def create_certificate_data():

    command = f'openssl req -x509 -newkey rsa:4096 -nodes -sha256 -keyout {TEST_FILES_DIRECTORY}/key.pem -out {TEST_FILES_DIRECTORY}/cert.pem -days 365 -subj "/C=US/ST=Oregon/L=Portland/O=Company Name/OU=Org/CN=www.example.com"'

    try:
        FNULL = open(os.devnull, 'w')
        subprocess.run(command, shell=True, stdout=FNULL, check=True)
    except subprocess.CalledProcessError:
        assert False

    with open(f'{TEST_FILES_DIRECTORY}/invalid_cert.pem', 'w') as file:
        file.write('invalid')

    with open(f'{TEST_FILES_DIRECTORY}/invalid_key.pem', 'w') as file:
        file.write('invalid')

    generator = RSAKeyGenerator()
    generator.save_key_pair(
        private_key_path=f'{TEST_FILES_DIRECTORY}/cert_signing_key.pem',
        public_key_path=f'{TEST_FILES_DIRECTORY}/cert_signing_key_public.pem')