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
Contains the implementation of the LicenseDescriptor class.
"""

# Murasame Imports
from murasame.licensing.licensetypes import LicenseTypes

class LicenseDescriptor:

    """Represents a single license.

    Attributes:
        _license_key (UUID): The unique license key.
        _owner_id (UUID): Unique ID of the owner of the license.
        _type (LicenseTypes): The type of the license.
        _features (dict): List of features that are enabled by the license.

    Authors:
        Attila Kovacs
    """

    @property
    def Key(self) -> 'UUID':

        """Provides access to the unique license key.

        Authors:
            Attila Kovacs
        """

        return self._license_key

    @property
    def Owner(self) -> 'UUID':

        """Provides access to the unique ID of the owner of the license.

        Authors:
            Attila Kovacs
        """

        return self._owner_id

    @property
    def Type(self) -> 'LicenseTypes':

        """Provides access to the type of the license.

        Authors:
            Attila Kovacs
        """

        return self._type

    @property
    def Features(self) -> list:

        """Provides access to the list of features associated with the license.

        Authors:
            Attila Kovacs
        """

        return self._features

    def __init__(
            self,
            license_key: 'UUID',
            owner_id: 'UUID',
            license_type: 'LicenseTypes') -> None:

        """Creates a new LicenseDescriptor instance.

        Args:
            license_key (UUID): The unique license key.
            owner_id (UUID): Unique ID of the owner of the license.
            license_type (LicenseTypes): The type of the license.

        Authors:
            Attila Kovacs
        """

        self._license_key = license_key
        self._owner_id = owner_id
        self._type = license_type
        self._features = {}

    def has_feature(self, feature_id: 'UUID') -> bool:

        """Returns whether or not a given feature is associated by the license.

        Args:
            feature_id (UUIS): The feature id to check.

        Returns:
            bool: 'True' if the given feature is covered by the license,
                'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if str(feature_id) in self._features:
            return True

        return False

    def add_feature(self, feature_id: 'UUID', metadata: dict) -> None:

        """Adds the given feature to the license.

        Args:
            feature_id (UUID): The unique ID of the feature.
            metadata (dict): Additional metadata associated with the license,
                e.g. capacity limitation.

        Authors:
            Attila Kovacs
        """

        if self.has_feature(feature_id):
            return

        self._features[str(feature_id)] = metadata

    def remove_feature(self, feature_id: 'UUID') -> None:

        """Removes a given feature from the license.

        Args:
            feature_id (UUID): The unique ID of the feature.

        Authors:
            Attila Kovacs
        """

        if self.has_feature(feature_id):
            del self._features[str(feature_id)]

    def serialize(self) -> dict:

        """Returns the license descriptor serialized to a JSON format.

        Returns:
            dict: The license descriptor as a dictionary.

        Authors:
            Attila Kovacs
        """

        descriptor = \
        {
            'key': str(self._license_key),
            'owner': str(self._owner_id),
            'type': self._serialize_license_type(),
            'features': self._features
        }

        return descriptor

    def _serialize_license_type(self) -> str:

        """Returns the type of the license serialized as a string.

        Authors:
            Attila Kovacs
        """

        if self._type == LicenseTypes.PRODUCTION:
            return 'production'

        return 'development'
