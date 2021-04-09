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
Contains the unit tests of the VFSResource class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.pal.vfs.vfslocalfileconnector import VFSLocalFileConnector
from murasame.pal.vfs.vfslocalfile import VFSLocalFile

JSON_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/vfstest.json'))

JSON_DESCRIPTOR_DATA = \
{
    'type': 'localfile',
    'path': JSON_PATH,
    'contenttype': 'application/json'
}

JSON_DESCRIPTOR = VFSLocalFile()
JSON_DESCRIPTOR.deserialize(data=JSON_DESCRIPTOR_DATA)

JSON_DESCRIPTOR_NO_MIME_DATA = \
{
    'type': 'localfile',
    'path': JSON_PATH
}

JSON_DESCRIPTOR_NO_MIME = VFSLocalFile()
JSON_DESCRIPTOR_NO_MIME.deserialize(data=JSON_DESCRIPTOR_NO_MIME_DATA)

JSON_CONF_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/vfstestjson.conf'))

JSON_CONF_DESCRIPTOR_DATA = \
{
    'type': 'localfile',
    'path': JSON_CONF_PATH
}

JSON_CONF_DESCRIPTOR = VFSLocalFile()
JSON_CONF_DESCRIPTOR.deserialize(data=JSON_CONF_DESCRIPTOR_DATA)

YAML_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/vfstest.yaml'))

YAML_DESCRIPTOR_DATA = \
{
    'type': 'localfile',
    'path': YAML_PATH,
    'contenttype': 'application/x-yaml'
}

YAML_DESCRIPTOR = VFSLocalFile()
YAML_DESCRIPTOR.deserialize(data=YAML_DESCRIPTOR_DATA)

YAML_DESCRIPTOR_NO_MIME_DATA = \
{
    'type': 'localfile',
    'path': YAML_PATH
}

YAML_DESCRIPTOR_NO_MIME = VFSLocalFile()
YAML_DESCRIPTOR_NO_MIME.deserialize(data=YAML_DESCRIPTOR_NO_MIME_DATA)

YAML_CONF_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/vfstestyaml.conf'))

YAML_CONF_DESCRIPTOR_DATA = \
{
    'type': 'localfile',
    'path': YAML_CONF_PATH,
}

YAML_CONF_DESCRIPTOR = VFSLocalFile()
YAML_CONF_DESCRIPTOR.deserialize(data=YAML_CONF_DESCRIPTOR_DATA)

GENERIC_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/vfstest.txt'))

GENERIC_DESCRIPTOR_DATA = \
{
    'type': 'localfile',
    'path': GENERIC_PATH
}

GENERIC_DESCRIPTOR = VFSLocalFile()
GENERIC_DESCRIPTOR.deserialize(data=GENERIC_DESCRIPTOR_DATA)

BINARY_DESCRIPTOR_DATA = \
{
    'type': 'localfile',
    'path': GENERIC_PATH,
    'contenttype': 'application/x-binary'
}

BINARY_DESCRIPTOR = VFSLocalFile()
BINARY_DESCRIPTOR.deserialize(data=BINARY_DESCRIPTOR_DATA)

NONEXISTENT_DESCRIPTOR_DATA = \
{
    'type': 'localfile',
    'path': '/path/to/file'
}

NONEXISTENT_DESCRIPTOR = VFSLocalFile()
NONEXISTENT_DESCRIPTOR.deserialize(data=NONEXISTENT_DESCRIPTOR_DATA)

class TestVFSLocalFileConnector:

    """
    Contains the unit tests for the VFSLocalFileConnector class.
    """

    def test_creation(self):

        """
        Tests that a VFSLocalFileConnector instance can be created.
        """

        sut = VFSLocalFileConnector()
        assert sut is not None

    def test_loading_files(self):

        """
        Tests that files can be loaded through the local file connector.
        """

        # Create test files
        if os.path.isfile(JSON_PATH):
            os.remove(JSON_PATH)

        with open(JSON_PATH, 'w') as file:
            file.write('{\"test\": \"value\"}')

        if os.path.isfile(YAML_PATH):
            os.remove(YAML_PATH)

        with open(YAML_PATH, 'w') as file:
            file.write('test: value')

        if os.path.isfile(GENERIC_PATH):
            os.remove(GENERIC_PATH)

        with open(GENERIC_PATH, 'w') as file:
            file.write('test')

        if os.path.isfile(JSON_CONF_PATH):
            os.remove(JSON_CONF_PATH)

        with open(JSON_CONF_PATH, 'w') as file:
            file.write('{\"test\": \"value\"}')

        if os.path.isfile(YAML_CONF_PATH):
            os.remove(YAML_CONF_PATH)

        with open(YAML_CONF_PATH, 'w') as file:
            file.write('test: value')

        # STEP #1 - JSON files can be loaded through the connector.
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=JSON_DESCRIPTOR)
        assert data['test'] == 'value'

        # STEP #2 - JSON files without specified MIME type can be loaded
        #           through the connector.
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=JSON_DESCRIPTOR_NO_MIME)
        assert data['test'] == 'value'

        # STEP #3 - YAML files can be loaded through the connector.
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=YAML_DESCRIPTOR)
        assert data['test'] == 'value'

        # STEP #4 - YAML files without specified MIME type can be loaded
        #           through the connector.
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=YAML_DESCRIPTOR_NO_MIME)
        assert data['test'] == 'value'

        # STEP #5 - Generic files can be loaded through the connector.
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=GENERIC_DESCRIPTOR)
        assert data == 'test'

        # STEP #6 - Binary files can be loaded through the connector.
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=BINARY_DESCRIPTOR)
        assert data == b'test'

        # STEP #7 - Conf files with JSON content can be cloaded through the
        #           connector.
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=JSON_CONF_DESCRIPTOR)
        assert data['test'] == 'value'

        # STEP #8 - Conf files with YAML content can be loaded through the
        #           connector.
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=YAML_CONF_DESCRIPTOR)
        assert data['test'] == 'value'

        # STEP #9 - Non-existent files cannot be loaded
        sut = VFSLocalFileConnector()
        data = sut.load(descriptor=NONEXISTENT_DESCRIPTOR)
        assert data == None

        # STEP #10 - Invalid descriptor cannot be loaded
        sut = VFSLocalFileConnector()
        with pytest.raises(InvalidInputError):
            sut.load(descriptor=None)

    def test_saving_files(self):

        """
        Tests that files can be saved through the local file connector.
        """

        # STEP #1 - JSON file can be saved

        # STEP #2 - YAML file can be saved

        # STEP #3 - Conf file can be saved

        # STEP #3 - File without a MIME type can be saved
