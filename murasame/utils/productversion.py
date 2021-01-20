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
Contains the implementation of the ProductVersion class.
"""

# Used to postpone evalutation of annotations so that type hints of a class
# can be used while declaring that class
from __future__ import annotations

# Platform Imports
from enum import IntEnum

# Murasame Imports
from murasame.exceptions import InvalidInputError

class ProductVersion:

    """
    Utility class for parsing and storing product version info that is
    compatible with the Semantic Versioning 2.0.0 standard as described at
    https://semver.org/spec/v2.0.0.html.

    Authors:
        Attila Kovacs
    """

    @property
    def MajorVersion(self) -> int:

        """
        The major product version.

        Authors:
            Attila Kovacs
        """

        return self._major

    @property
    def MinorVersion(self) -> int:

        """
        The minor product version.

        Authors:
            Attila Kovacs
        """

        return self._minor

    @property
    def PatchLevel(self) -> int:

        """
        The patch level.

        Authors:
            Attila Kovacs
        """

        return self._patch

    @property
    def ReleaseLevel(self) -> str:

        """
        The configured release level.

        Authors:
            Attila Kovacs
        """

        return self._release_level

    @property
    def MetaData(self) -> dict:

        """
        The content of the metadata field as a dictionary.

        Authors:
            Attila Kovacs
        """

        return self._meta

    @property
    def MetaString(self) -> str:

        """
        The version metadata in string format.

        Authors:
            Attila Kovacs
        """

        return self._get_metadata_string()

    @property
    def Codename(self) -> str:

        """
        The codename of the product version. Returns 'UNKNOWN' if there is no
        codename specified in the metadata field.

        Authors:
            Attila Kovacs
        """

        if self._meta is None:
            return 'UNKNOWN'

        try:
            return self._meta['codename']
        except KeyError:
            return 'UNKNOWN'

    @property
    def SCM(self) -> str:

        """
        The SCM identifier from which the product was built. Returns 'UNKNOWN'
        if there is no scm specified in the metadata field.

        Authors:
            Attila Kovacs
        """

        if self._meta is None:
            return 'UNKNOWN'

        try:
            return self._meta['scm']
        except KeyError:
            return 'UNKNOWN'

    @property
    def Build(self) -> str:

        """
        The build number. Returns '0' if there is no build number specified in
        the metadata field.

        Authors:
            Attila Kovacs
        """

        if self._meta is None:
            return '0'

        try:
            return self._meta['build']
        except KeyError:
            return '0'

    @property
    def VersionString(self) -> str:

        """
        The string representation of the product version.

        Authors:
            Attila Kovacs
        """

        if self._meta is not None:
            return '{}.{}.{}-{}+{}'.format(
                self._major,
                self._minor,
                self._patch,
                self._get_release_level_string(),
                self._get_metadata_string())

        return '{}.{}.{}-{}'.format(
            self._major,
            self._minor,
            self._patch,
            self._get_release_level_string())

    @property
    def ShortVersionString(self) -> str:

        """
        Returns the short string representation of the product version only
        containing the major version, minor version and the patch number.

        Authors:
            Attila Kovacs
        """

        return '{}.{}.{}'.format(self._major, self._minor, self._patch)

    class ReleaseLevels(IntEnum):

        """
        List of supported release levels.

        Authors:
            Attila Kovacs
        """

        INTERNAL = 0    # Marks an internal, non-public release.
        ALPHA = 1       # Marks an alpha release
        BETA = 2        # Marks a closed beta release
        EAP = 3         # Marks an early access program release
        RC = 4          # Marks a release candidate release
        GA = 5          # Marks a general availability release

    def __init__(self, version_data: dict) -> None:

        """
        Creates a new ProductVersion instance.

        Args:
            version_data:       The product version in serialized JSON format.

        Authors:
            Attila Kovacs
        """

        self._major = None             # Major product version
        self._minor = None             # Minor product version
        self._patch = None             # Patch level
        self._release_level = None     # Release level
        self._meta = None              # Additional metadata

        self.load(version_data)

    def __eq__(self, other: ProductVersion) -> bool:

        """
        Equality operator.

        Args:
            other:      The product version instance to compare with.

        Returns:
            'True' if the two product versions are equal, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ProductVersion):
            return NotImplemented

        return self.is_equal(other)

    def __ne__(self, other: ProductVersion) -> bool:

        """
        Inequality operator.

        Args:
            other:      The product version instance to compare with.

        Returns:
            'True' if the two product versions are not equal, 'False'
            otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ProductVersion):
            return NotImplemented

        return not self.is_equal(other)

    def __lt__(self, other: ProductVersion) -> bool:

        """
        Less-than operator.

        Args:
            other:      The product version instance to compare with.

        Returns:
            'True' if this product version is older than the other one, 'False'
            otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ProductVersion):
            return NotImplemented

        return self.is_older(other)

    def __le__(self, other: ProductVersion) -> bool:

        """
        Less-than or equal operator.

        Args:
            other:      The product version instance to compare with.

        Returns:
            'True' if this product version is the same or older than the other
            one, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ProductVersion):
            return NotImplemented

        return self.is_older(other) or self.is_equal(other)

    def __gt__(self, other: ProductVersion) -> bool:

        """
        Greater-than operator.

        Args:
            other:      The product version instance to compare with.

        Returns:
            'True' if this product version is newer than the other one, 'False'
            otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ProductVersion):
            return NotImplemented

        return self.is_newer(other)

    def __ge__(self, other: ProductVersion) -> bool:

        """
        Greater-than or equal operator.

        Args:
            other:      The product version instance to compare with.

        Returns:
            'True' if this product version is the same or newer than the other
            one, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if not isinstance(other, ProductVersion):
            return NotImplemented

        return self.is_newer(other) or self.is_equal(other)

    def __repr__(self) -> str:

        """
        Unambiguity operator.

        Authors:
            Attila Kovacs
        """

        return 'ProductVersion({})'.format(self.VersionString)

    def __str__(self) -> str:

        """
        Returns the string representation of this product version.

        Authors:
            Attila Kovacs
        """

        return self.VersionString

    def __hash__(self) -> int:

        """
        Provides the hash for this product version.

        Authors:
            Attila Kovacs
        """

        return hash(self.VersionString)

    def load(self, version_data: dict) -> None:

        """
        Loads the product version from its serialized JSON format.

        Args:
            version_data:       The version data to load.

        Authors:
            Attila Kovacs
        """

        self._load_major_version(version_data)
        self._load_minor_version(version_data)
        self._load_patch_level(version_data)
        self._load_release_level(version_data)
        self._load_metadata(version_data)

    def is_equal(self, other: ProductVersion) -> bool:

        """
        Returns whether or not this product version equals to the given one.

        Args:
            other:      The other product version to compare with.

        Returns:
            'True' if the two product versions are equal, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        if self.MajorVersion == other.MajorVersion \
           and self.MinorVersion == other.MinorVersion \
           and self.PatchLevel == other.PatchLevel:
            return True

        return False

    def is_newer(self, other: ProductVersion) -> bool:

        """
        Returns whether or not this ProductVersion is newer than an other one.

        Args:
            other:      The other product version to compare with.

        Returns:
            'True' if the twis product versions is newer, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        result = False

        if self.MajorVersion > other.MajorVersion:
            result = True
        else:
            if self.MinorVersion > other.MinorVersion:
                result = True
            else:
                if self.PatchLevel > other.PatchLevel:
                    result = True

        return result

    def is_older(self, other: ProductVersion) -> bool:

        """
        Returns whether or not this ProductVersion is older than an other one.

        Args:
            other:      The other product version to compare with.

        Returns:
            'True' if the twis product versions is older, 'False' otherwise.

        Authors:
            Attila Kovacs
        """

        result = False

        if self.MajorVersion < other.MajorVersion:
            result = True
        else:
            if self.MinorVersion < other.MinorVersion:
                result = True
            else:
                if self.PatchLevel < other.PatchLevel:
                    result = True

        return result

    def bump_major_version(self) -> None:

        """
        Bumps the major version of the product version.

        Authors:
            Attila Kovacs
        """

        self._major += 1
        self._minor = 0
        self._patch = 0

    def bump_minor_version(self) -> None:

        """
        Bumps the minor version of the product version.

        Authors:
            Attila Kovacs
        """

        self._minor += 1
        self._patch = 0

    def bump_patch_level(self) -> None:

        """
        Bumps the patch level of the product version.

        Authors:
            Attila Kovacs
        """

        self._patch += 1

    def bump_build_number(self) -> None:

        """
        Bumps the build number if it's available as metadata.

        Authors:
            Attila Kovacs
        """

        if 'build' in self._meta:
            self._meta['build'] = int(self._meta['build']) + 1

    def _get_release_level_string(self) -> str:

        """
        Returns the string representation of the configured product release
        level.

        Returns:
            The release level in string format.

        Authors:
            Attila Kovacs
        """

        release_level = ''

        if self._release_level == ProductVersion.ReleaseLevels.INTERNAL:
            release_level = 'DEVELOPMENT'
        elif self._release_level == ProductVersion.ReleaseLevels.ALPHA:
            release_level = 'ALPHA'
        elif self._release_level == ProductVersion.ReleaseLevels.BETA:
            release_level = 'BETA'
        elif self._release_level == ProductVersion.ReleaseLevels.EAP:
            release_level = 'EAP'
        elif self._release_level == ProductVersion.ReleaseLevels.RC:
            release_level = 'RC'
        elif self._release_level == ProductVersion.ReleaseLevels.GA:
            release_level = 'GA'

        return release_level

    def _get_metadata_string(self) -> str:

        """
        Returns the version metadata in string format. It will include the SCM
        version or the build number as well. If both are available as metadata
        fields, then only the build number will be included.

        Returns:
            The version metadata in string format.

        Authors:
            Attila Kovacs
        """

        if self._meta is None:
            return 'UNKNOWN(UNKNOWN)'

        codename = ''
        scm = ''
        has_scm = False
        build = ''
        has_build = False

        try:
            codename = self._meta['codename']
        except KeyError:
            codename = 'UNKNOWN'

        try:
            build = self._meta['build']
            has_build = True
        except KeyError:
            build = 0

        try:
            scm = self._meta['scm']
            has_scm = True
        except KeyError:
            scm = 'UNKNOWN'

        if has_build:
            return '{}(Build {})'.format(codename, build)

        if has_scm:
            return '{}({})'.format(codename, scm)

        return '{}(UNKNOWN)'.format(codename)

    def _load_major_version(self, version_data: dict) -> None:

        """
        Loads the major product version from the configuration.

        Authors:
            Attila Kovacs
        """

        try:
            major = int(version_data['major'])
            if major < 0:
                raise InvalidInputError(
                    'Invalid product version. Major version cannot be a '
                    'negative number.')
            self._major = major
        except KeyError as exception:
            raise InvalidInputError(
                'Invalid product version. Major version not '
                'found.') from exception
        except ValueError as exception:
            raise InvalidInputError(
                'Invalid product version. Major version is not '
                'integer.') from exception

    def _load_minor_version(self, version_data: dict) -> None:

        """
        Loads the minor product version from the configuration.

        Authors:
            Attila Kovacs
        """

        try:
            minor = int(version_data['minor'])
            if minor < 0:
                raise InvalidInputError(
                    'Invalid product version. Minor version cannot be a '
                    'negative number.')
            self._minor = minor
        except KeyError as exception:
            raise InvalidInputError(
                'Invalid product version. Minor version not '
                'found.') from exception
        except ValueError as exception:
            raise InvalidInputError(
                'Invalid product version. Minor version is not '
                'integer.') from exception

    def _load_patch_level(self, version_data: dict) -> None:

        """
        Loads the patch level from the configuration.

        Authors:
            Attila Kovacs
        """

        try:
            patch = int(version_data['patch'])
            if patch < 0:
                raise InvalidInputError(
                    'Invalid product version. Patch level cannot be a '
                    'negative number.')
            self._patch = patch
        except KeyError as exception:
            raise InvalidInputError(
                'Invalid product version. Patch level not '
                'found.') from exception
        except ValueError as exception:
            raise InvalidInputError(
                'Invalid product version. Patch level is not '
                'integer.') from exception

    def _load_release_level(self, version_data: dict) -> None:

        """
        Loads the release level from the configuration.

        Authors:
            Attila Kovacs
        """

        try:
            release_level = version_data['release'].lower()

            if release_level == 'internal':
                self._release_level = ProductVersion.ReleaseLevels.INTERNAL
            elif release_level == 'alpha':
                self._release_level = ProductVersion.ReleaseLevels.ALPHA
            elif release_level == 'beta':
                self._release_level = ProductVersion.ReleaseLevels.BETA
            elif release_level == 'eap':
                self._release_level = ProductVersion.ReleaseLevels.EAP
            elif release_level == 'rc':
                self._release_level = ProductVersion.ReleaseLevels.RC
            elif release_level == 'ga':
                self._release_level = ProductVersion.ReleaseLevels.GA
            else:
                raise InvalidInputError(
                    'Unknown release level is configured: {}'.format(
                        release_level))

        except KeyError:
            self._release_level = ProductVersion.ReleaseLevels.GA

    def _load_metadata(self, version_data: dict) -> None:

        """
        Loads the version metadata from the configuration.

        Authors:
            Attila Kovacs
        """

        try:
            self._meta = version_data['meta']
        except KeyError:
            self._meta = None
