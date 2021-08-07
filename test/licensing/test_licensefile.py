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
Contains the unit tests of LicenseFile class.
"""

# Runtime Imports
import os
import sys
import uuid

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.licensing import (
    LicenseGenerator,
    LicenseDescriptor,
    LicenseFile,
    LicenseTypes)
from murasame.utils import (
    RSAKeyGenerator,
    RSAKeyLengths,
    RSAPrivate,
    RSAPublic)

TEST_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles'))

def get_password():
    return b'testpassword'

def get_encryption_key():
    return 'encryptionkey'

class TestLicenseFile:

    """
    Contains the unit tests for the LicenseFile class.

    Authors:
        Attila Kovacs
    """

    @classmethod
    def setup_class(cls):

        key_generator = RSAKeyGenerator(
            key_length=RSAKeyLengths.KEY_LENGTH_2048,
            cb_retrieve_password=get_password)

        key_generator.save_key_pair(
            private_key_path=f'{TEST_PATH}/license_private.pem',
            public_key_path=f'{TEST_PATH}/license_public.pem')

    @classmethod
    def teardown_class(cls):

        if os.path.isfile(f'{TEST_PATH}/license_private.pem'):
            os.remove(f'{TEST_PATH}/license_private.pem')

        if os.path.isfile(f'{TEST_PATH}/license_public.pem'):
            os.remove(f'{TEST_PATH}/license_public.pem')

        if os.path.isfile(f'{TEST_PATH}/license.lic'):
            os.remove(f'{TEST_PATH}/license.lic')

        if os.path.isfile(f'{TEST_PATH}/license2.lic'):
            os.remove(f'{TEST_PATH}/license2.lic')

    def test_creation_with_existing_private_key(self):

        """
        Tests that a LicenseFile object can be created when providing an
        existing RSAPrivate object.

        Authors:
            Attila Kovacs
        """

        private_key = RSAPrivate(
            key_path='{}/license_private.pem'.format(TEST_PATH),
            cb_retrieve_password=get_password)

        public_key = RSAPublic(
            key_path='{}/license_public.pem'.format(TEST_PATH))

        generator = LicenseGenerator(
            private_key=private_key,
            cb_retrieve_encryption_password=get_encryption_key)

        license_path = f'{TEST_PATH}/license.lic'

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

        generator.generate(output_path=license_path,
                           license_descriptor=descriptor)

        sut = LicenseFile(license_file_path=license_path,
                          cb_retrieve_password=get_encryption_key)

        assert sut.Signature is not None
        assert isinstance(sut.License, LicenseDescriptor)

    def test_creation_with_private_key_path(self):

        """
        Tests that a license file can be created when providing a path to a
        private key file in the file system.

        Authors:
            Attila Kovacs
        """

        generator = LicenseGenerator(
            private_key_path=f'{TEST_PATH}/license_private.pem',
            cb_retrieve_key_password=get_password,
            cb_retrieve_encryption_password=get_encryption_key)

        license_path = f'{TEST_PATH}/license2.lic'

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

        generator.generate(output_path=license_path,
                           license_descriptor=descriptor)

        sut = LicenseFile(license_file_path=license_path,
                          cb_retrieve_password=get_encryption_key)

        assert sut.Signature is not None
        assert isinstance(sut.License, LicenseDescriptor)
