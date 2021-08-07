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
Contains the unit tests of the ProductVersion class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.utils import ProductVersion
from murasame.exceptions import InvalidInputError

# Test data
SIMPLE_TEST_VERSION = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

BIGGER_TEST_VERSION = \
{
    'major': '2',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

SMALLER_TEST_VERSION = \
{
    'major': '0',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

INTERNAL_VERSION = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'internal',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

ALPHA_VERSION = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'alpha',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

EAP_VERSION = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'eap',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

RC_VERSION = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'rc',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

GA_VERSION = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'ga',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

INVALID_MAJOR_VERSION = \
{
    'major': 'invalid',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

NEGATIVE_MAJOR_VERSION = \
{
    'major': '-1',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

NO_MAJOR_VERSION = \
{
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

INVALID_MINOR_VERSION = \
{
    'major': '1',
    'minor': 'invalid',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

NEGATIVE_MINOR_VERSION = \
{
    'major': '1',
    'minor': '-2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

NO_MINOR_VERSION = \
{
    'major': '1',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

INVALID_PATCH_LEVEL = \
{
    'major': '1',
    'minor': '2',
    'patch': 'invalid',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

NEGATIVE_PATCH_LEVEL = \
{
    'major': '1',
    'minor': '2',
    'patch': '-3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

NO_PATCH_LEVEL = \
{
    'major': '1',
    'minor': '2',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

NO_RELEASE_LEVEL = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}

INVALID_RELEASE_LEVEL = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'invalid',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef'
    }
}


ADDITIONAL_METADATA = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test',
        'scm': 'abcdef',
        'additional': 'data'
    }
}

METADATA_NO_CODENAME = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'scm': 'abcdef'
    }
}

METADATA_NO_SCM = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'codename': 'test'
    }
}

NO_METADATA = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'beta'
}

VERSION_WITH_BUILD_NUMBER = \
{
    'major': '1',
    'minor': '2',
    'patch': '3',
    'release': 'beta',
    'meta':
    {
        'build': '1'
    }
}

class TestProductVersion:

    """
    Contains the unit tests for the ProductVersion class.

    Authors:
        Attila Kovacs
    """

    def test_product_version_creation(self):

        """
        Tests that a product version instance can be created successfully with
        normal config data.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)

        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.BETA
        assert sut.Codename == 'test'
        assert sut.SCM == 'abcdef'
        assert sut.Build == '0'

    def test_product_version_creation_with_invalid_major_version(self):

        """
        Tests that product version cannot be created with invalid major
        version.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(INVALID_MAJOR_VERSION)

    def test_product_version_creation_with_invalid_minor_version(self):

        """
        Tests that product version cannot be created with invalid minor
        version.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(INVALID_MINOR_VERSION)

    def test_product_version_creation_with_invalid_major_patch_level(self):

        """
        Tests that product version cannot be created with invalid patch level.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(INVALID_PATCH_LEVEL)

    def test_product_version_creation_without_metadata(self):

        """
        Tests that product version can be created without metadata.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(NO_METADATA)
        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.BETA
        assert sut.Codename == 'UNKNOWN'
        assert sut.SCM == 'UNKNOWN'

    def test_product_version_creation_with_partial_metadata(self):

        """
        Tests that product version can be created with partial metadata.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(METADATA_NO_CODENAME)
        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.BETA
        assert sut.Codename == 'UNKNOWN'
        assert sut.SCM == 'abcdef'

        sut = ProductVersion(METADATA_NO_SCM)
        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.BETA
        assert sut.Codename == 'test'
        assert sut.SCM == 'UNKNOWN'

    def test_product_version_creation_with_no_major_version(self):

        """
        Tests that product version cannot be created without a major version.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(NO_MAJOR_VERSION)

    def test_product_version_creation_with_no_minor_version(self):

        """
        Tests that product version cannot be created without a minor version.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(NO_MINOR_VERSION)

    def test_product_version_creation_with_no_patch_level(self):

        """
        Tests that product version cannot be created without a patch level.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(NO_PATCH_LEVEL)

    def test_product_version_creation_with_no_release_level(self):

        """
        Tests that product version can be created with no release level.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(NO_RELEASE_LEVEL)
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.GA

    def test_product_version_creation_with_various_release_levels(self):

        """
        Tests the creation of product version with various release levels.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(INTERNAL_VERSION)
        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.INTERNAL
        assert sut.Codename == 'test'
        assert sut.SCM == 'abcdef'

        sut = ProductVersion(ALPHA_VERSION)
        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.ALPHA
        assert sut.Codename == 'test'
        assert sut.SCM == 'abcdef'

        sut = ProductVersion(EAP_VERSION)
        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.EAP
        assert sut.Codename == 'test'
        assert sut.SCM == 'abcdef'

        sut = ProductVersion(RC_VERSION)
        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.RC
        assert sut.Codename == 'test'
        assert sut.SCM == 'abcdef'

        sut = ProductVersion(GA_VERSION)
        assert sut.MajorVersion == 1
        assert sut.MinorVersion == 2
        assert sut.PatchLevel == 3
        assert sut.ReleaseLevel == ProductVersion.ReleaseLevels.GA
        assert sut.Codename == 'test'
        assert sut.SCM == 'abcdef'

    def test_product_version_creation_with_invalid_release_level(self):

        """
        Tests that a product version cannot be created with invalid release
        level.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(INVALID_RELEASE_LEVEL)

    def test_product_version_creation_with_negative_version_numbers(self):

        """
        Tests that product version cannot be created with negative version
        numbers.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(NEGATIVE_MAJOR_VERSION)

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(NEGATIVE_MINOR_VERSION)

        with pytest.raises(InvalidInputError):
            sut = ProductVersion(NEGATIVE_PATCH_LEVEL)

    def test_metadata_retrieval_in_raw_format(self):

        """
        Tests that metadata can be retrieved from the product version in raw
        format.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        assert sut.MetaData == {'codename': 'test', 'scm': 'abcdef'}

    def test_accessing_metadata_fields_through_raw_format(self):

        """
        Tests that metadata fields can be accessed through the raw metadata.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(ADDITIONAL_METADATA)
        assert sut.MetaData == {'codename': 'test', 'scm': 'abcdef', 'additional': 'data'}
        assert sut.Build == '0'
        assert sut.MetaData['additional'] == 'data'

    def test_accessing_build_number(self):

        """
        Tests that the build number can be accessed.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(VERSION_WITH_BUILD_NUMBER)
        assert sut.Build == '1'

        sut = ProductVersion(NO_METADATA)
        assert sut.Build == '0'

    def test_version_string_conversion_full_version(self):

        """
        Tests string representations of the full product version.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        assert sut.VersionString == '1.2.3-BETA+test(abcdef)'

        sut = ProductVersion(NO_METADATA)
        assert sut.VersionString == '1.2.3-BETA'

    def test_version_string_conversion_short_version(self):

        """
        Tests string represnetation of the short product version.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        assert sut.ShortVersionString == '1.2.3'

    def test_version_string_metadata_conversion(self):

        """
        Tests that the metadata conversion to string in the product version is
        correct.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        assert sut.MetaString == 'test(abcdef)'

        sut = ProductVersion(NO_METADATA)
        assert sut.MetaString == 'UNKNOWN(UNKNOWN)'

        sut = ProductVersion(METADATA_NO_CODENAME)
        assert sut.MetaString == 'UNKNOWN(abcdef)'

        sut = ProductVersion(METADATA_NO_SCM)
        assert sut.MetaString == 'test(UNKNOWN)'

    def test_version_string_conversion_release_levels(self):

        """
        Tests that the string conversion of various release levels is correct.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(INTERNAL_VERSION)
        assert sut.VersionString == '1.2.3-DEVELOPMENT+test(abcdef)'

        sut = ProductVersion(ALPHA_VERSION)
        assert sut.VersionString == '1.2.3-ALPHA+test(abcdef)'

        sut = ProductVersion(EAP_VERSION)
        assert sut.VersionString == '1.2.3-EAP+test(abcdef)'

        sut = ProductVersion(RC_VERSION)
        assert sut.VersionString == '1.2.3-RC+test(abcdef)'

        sut = ProductVersion(GA_VERSION)
        assert sut.VersionString == '1.2.3-GA+test(abcdef)'

    def test_product_version_operators(self):

        """
        Tests that product versions can be compared by using operators

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        sut_equal = ProductVersion(SIMPLE_TEST_VERSION)
        sut_smaller = ProductVersion(SMALLER_TEST_VERSION)
        sut_bigger = ProductVersion(BIGGER_TEST_VERSION)

        assert (sut == sut_equal) == True
        assert (sut == sut_smaller) == False
        assert (sut != sut_equal) == False
        assert (sut != sut_smaller) == True
        assert (sut < sut_smaller) == False
        assert (sut < sut_bigger) == True
        assert (sut > sut_smaller) == True
        assert (sut > sut_bigger) == False
        assert (sut <= sut_smaller) == False
        assert (sut <= sut_bigger) == True
        assert (sut <= sut_equal) == True
        assert (sut >= sut_smaller) == True
        assert (sut >= sut_bigger) == False
        assert (sut >= sut_equal) == True

        assert (sut == 1) == False
        assert (sut != 1) == True

        with pytest.raises(TypeError):
            sut < 1

        with pytest.raises(TypeError):
            sut > 1

        with pytest.raises(TypeError):
            sut <= 1

        with pytest.raises(TypeError):
            sut >= 1

        assert sut.__repr__() == 'ProductVersion(1.2.3-BETA+test(abcdef))'
        assert sut.__str__() == '1.2.3-BETA+test(abcdef)'
        assert sut.__hash__() == hash(sut.VersionString)

    def test_bumping_major_version(self):

        """
        Tests that major version can be bumped.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        sut.bump_major_version()
        assert sut.VersionString == '2.0.0-BETA+test(abcdef)'

    def test_bumping_minor_version(self):

        """
        Tests that minor version can be bumped.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        sut.bump_minor_version()
        assert sut.VersionString == '1.3.0-BETA+test(abcdef)'

    def test_bumping_patch_level(self):

        """
        Tests that patch level can be bumped.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        sut.bump_patch_level()
        assert sut.VersionString == '1.2.4-BETA+test(abcdef)'

    def test_bumping_build_number(self):

        """
        Tests that build number can be bumped.

        Authors:
            Attila Kovacs
        """

        sut = ProductVersion(VERSION_WITH_BUILD_NUMBER)
        sut.bump_build_number()
        assert sut.VersionString == '1.2.3-BETA+UNKNOWN(Build 2)'

        sut = ProductVersion(SIMPLE_TEST_VERSION)
        sut.bump_build_number()
        assert sut.VersionString == '1.2.3-BETA+test(abcdef)'
