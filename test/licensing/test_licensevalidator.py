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
Contains the unit tests of LicenseValidator class.
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
    LicenseValidator,
    LicenseGenerator,
    LicenseDescriptor,
    LicenseTypes)
from murasame.utils import (
    RSAKeyGenerator,
    RSAKeyLengths,
    RSAPrivate,
    RSAPublic)

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

def get_password():
    return b'testpassword'

def get_encryption_key():
    return 'encryptionkey'

class TestLicenseValidator:

    """
    Contains the unit tests of the LicenseValidator class.

    Authors:
        Attila Kovacs
    """

    def test_creation_with_public_key(self):

        """
        Tests that a LicenseValidator can be created with using an existing
        RSAPublic object.

        Authors:
            Attila Kovacs
        """

        public_key = RSAPublic(
            key_path=f'{TEST_FILES_DIRECTORY}/license_public.pem')

        sut = LicenseValidator(public_key=public_key)

        assert sut is not None

    def test_creation_with_public_key_path(self):

        """
        Tests that a LicenseValidator can be created with a path to a public
        key in the file system.

        Authors:
            Attila Kovacs
        """

        sut = LicenseValidator(
            public_key_path=f'{TEST_FILES_DIRECTORY}/license_public.pem')

        assert sut is not None

    def test_validation(self):

        """
        Tests that a license can be validated using the validator.

        Authors:
            Attila Kovacs
        """

        private_key = RSAPrivate(
            key_path=f'{TEST_FILES_DIRECTORY}/license_private.pem',
            cb_retrieve_password=get_password)

        public_key = RSAPublic(
            key_path=f'{TEST_FILES_DIRECTORY}/license_public.pem')

        generator = LicenseGenerator(
            private_key_path=f'{TEST_FILES_DIRECTORY}/license_private.pem',
            cb_retrieve_key_password=get_password,
            cb_retrieve_encryption_password=get_encryption_key)

        license_path = f'{TEST_FILES_DIRECTORY}/license.lic'

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

        sut = LicenseValidator(public_key=public_key)

        assert sut.validate(
            license_path=f'{TEST_FILES_DIRECTORY}/license.lic',
            cb_retrieve_password=get_encryption_key)
