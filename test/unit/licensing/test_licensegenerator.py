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
Contains the unit tests of LicenseGenerator class.
"""

# Platform Imports
import os
import sys
import uuid

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils import (
    RSAKeyGenerator,
    RSAKeyLengths,
    RSAPrivate,
    RSAPublic)
from murasame.licensing import (
    LicenseGenerator,
    LicenseDescriptor,
    LicenseTypes)

TEST_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles'))

def get_password():
    return b'testpassword'

def get_encryption_key():
    return 'encryptionkey'

class TestLicenseGenerator:

    """
    Contains the unit tests of the LicenseGenerator class.
    """

    def test_creation(self):

        """
        Tests that a license generator can be created.
        """

        key_generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        key_generator.save_key_pair(
            private_key_path='{}/license_private.pem'.format(TEST_PATH),
            public_key_path='{}/license_public.pem'.format(TEST_PATH))

        private_key = RSAPrivate(
            key_path='{}/license_private.pem'.format(TEST_PATH),
            cb_retrieve_password=get_password)

        # STEP #1 - Test by assigning an existing private key
        sut = LicenseGenerator(
            private_key=private_key,
            cb_retrieve_encryption_password=get_encryption_key)

        # STEP #2 - Test by creating with a key path
        sut = LicenseGenerator(
            private_key_path='{}/license_private.pem'.format(TEST_PATH),
            cb_retrieve_key_password=get_password,
            cb_retrieve_encryption_password=get_encryption_key)

        os.remove('{}/license_private.pem'.format(TEST_PATH))
        os.remove('{}/license_public.pem'.format(TEST_PATH))

    def test_generation(self):

        """
        Tests that a license key can be generatred.
        """

        key_generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        key_generator.save_key_pair(
            private_key_path='{}/license_private.pem'.format(TEST_PATH),
            public_key_path='{}/license_public.pem'.format(TEST_PATH))

        private_key = RSAPrivate(
            key_path='{}/license_private.pem'.format(TEST_PATH),
            cb_retrieve_password=get_password)

        # STEP #1 - Test by assigning an existing private key
        sut = LicenseGenerator(
            private_key=private_key,
            cb_retrieve_encryption_password=get_encryption_key)

        # STEP #2 - Test by creating with a key path
        sut = LicenseGenerator(
            private_key_path='{}/license_private.pem'.format(TEST_PATH),
            cb_retrieve_key_password=get_password,
            cb_retrieve_encryption_password=get_encryption_key)

        license_path = '{}/license.lic'.format(TEST_PATH)

        key = uuid.uuid4()
        owner = uuid.uuid4()
        license_type = LicenseTypes.DEVELOPMENT
        feature = uuid.uuid4()

        descriptor = LicenseDescriptor(
            license_key=key,
            owner_id=owner,
            license_type=license_type)
        descriptor.add_feature(
            feature_id=feature,
            metadata={'test': 'testvalue'})

        sut.generate(output_path=license_path, license_descriptor=descriptor)

        assert os.path.isfile('{}/license.lic'.format(TEST_PATH))

        os.remove('{}/license_private.pem'.format(TEST_PATH))
        os.remove('{}/license_public.pem'.format(TEST_PATH))
        os.remove('{}/license.lic'.format(TEST_PATH))