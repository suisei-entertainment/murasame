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
Contains the unit tests of LicenseDescriptor class.
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
from murasame.licensing import LicenseDescriptor, LicenseTypes

class TestLicenseDescriptor:

    """
    Contains the unit tests of the LicenseDescriptor class.
    """

    def test_creation(self):

        """
        Tests that a licensedescriptor instance can be created.
        """

        key = uuid.uuid4()
        owner = uuid.uuid4()
        license_type = LicenseTypes.DEVELOPMENT

        sut = LicenseDescriptor(
            license_key=key,
            owner_id=owner,
            license_type=license_type)

        assert sut.Key == key
        assert sut.Owner == owner
        assert sut.Type == license_type
        assert sut.Features == {}

    def test_adding_feature(self):

        """
        Tests that features can be added to the license descriptor.
        """

        key = uuid.uuid4()
        owner = uuid.uuid4()
        license_type = LicenseTypes.DEVELOPMENT
        feature = uuid.uuid4()

        sut = LicenseDescriptor(
            license_key=key,
            owner_id=owner,
            license_type=license_type)

        sut.add_feature(feature_id=feature, metadata={'test': 'testvalue'})

        assert sut.has_feature(feature_id=feature)
        assert not sut.has_feature(feature_id=uuid.uuid4())

    def test_removing_feature(self):

        """
        Tests that features can be removed.
        """

        key = uuid.uuid4()
        owner = uuid.uuid4()
        license_type = LicenseTypes.DEVELOPMENT
        feature = uuid.uuid4()

        sut = LicenseDescriptor(
            license_key=key,
            owner_id=owner,
            license_type=license_type)

        sut.add_feature(feature_id=feature, metadata={'test': 'testvalue'})
        assert sut.has_feature(feature_id=feature)

        sut.remove_feature(feature_id=feature)
        assert not sut.has_feature(feature_id=feature)

    def test_serialization(self):

        """
        Tests that a license descriptor can be serialized to JSON.
        """

        key = '8c6f4d93-e848-468a-8465-bbad9f66e4f1'
        owner = '96016c79-b0f6-4432-9872-7c4cdad2001a'
        license_type = LicenseTypes.DEVELOPMENT
        feature = 'a4549bab-f116-4fb1-b553-3b6d9880cfed'

        sut = LicenseDescriptor(
            license_key=key,
            owner_id=owner,
            license_type=license_type)

        sut.add_feature(feature_id=feature, metadata={'test': 'testvalue'})

        serialized = \
        {
            'key': key,
            'owner': owner,
            'type': 'development',
            'features':
            {
                feature:
                {
                    'test': 'testvalue'
                }
            }
        }

        assert sut.serialize() == serialized
