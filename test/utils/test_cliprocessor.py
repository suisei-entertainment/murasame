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
Contains the unit tests of the CliProcessor class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.utils import CliProcessor, JsonFile
from murasame.exceptions import InvalidInputError

# Test data
TEST_COMMAND_MAP = \
{
    'commands':
    [
        {
            'type': 'group',
            'name': 'test group',
            'description': 'test description',
            'commands':
            [
                {
                    'type': 'switch',
                    'shortkey': '',
                    'command': '--switch-test',
                    'help': 'test',
                    'default': 'False'
                },
                {
                    'type': 'config',
                    'shortkey': '-t',
                    'command': '--config-test',
                    'help': 'test',
                    'metavar': 'VALUE'
                }
            ]
        },
        {
            'type': 'switch',
            'shortkey': '',
            'command': '--switch-test2',
            'help': 'test',
            'default': 'False'
        },
        {
            'type': 'config',
            'shortkey': '-c',
            'command': '--config-test2',
            'help': 'test',
            'metavar': 'VALUE'
        }
    ]
}

TEST_FILE_PATH = os.path.abspath(os.path.expanduser(
    '~/.murasame/testfiles/cli_test.conf'))

class TestCliProcessor:

    """Contains all unit tests of the CliProcessor class.

    Authors:
        Attila Kovacs
    """

    def test_creation_from_command_map(self) -> None:

        """Tests that a CliProcessor object can be created from a command map.

        Authors:
            Attila Kovacs
        """

        sut = CliProcessor(command_map=TEST_COMMAND_MAP)
        assert sut.Parser is not None

    def test_creation_from_config_file(self) -> None:

        """Tests that a CliProcessor object can be created from a configuration
        file.

        Authors:
            Attila Kovacs
        """

        file = JsonFile(path=TEST_FILE_PATH)
        file.overwrite_content(content=TEST_COMMAND_MAP)
        file.save()

        sut = CliProcessor(config_file=TEST_FILE_PATH)
        assert sut.Parser is not None

    def test_creation_without_command_map_or_config_file(self) -> None:

        """Tests that a CLI processor cannot be created without a valid command
        map or configuration file.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = CliProcessor(command_map=None, config_file=None)

    def test_creation_with_unparsable_command_map(self) -> None:

        """Tests that a CLI processor cannot be created if the provided command
        map cannot be parsed.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = CliProcessor(command_map={'malformed': 'value'})

    def test_creation_with_failing_config_file_and_fallback_command_map(self) -> None:

        """Tests that a CLI processor can be created if the loading of the
        configuration file fails, but there is a fallback command map.

        Authors:
            Attila Kovacs
        """

        with open(TEST_FILE_PATH, 'w') as file:
            file.write('malformed content')

        sut = CliProcessor(command_map=TEST_COMMAND_MAP,
                           config_file=TEST_FILE_PATH)

    def test_creation_with_failing_config_file_without_fallback_command_map(self) -> None:

        """Tests that a CLI processor cannot be created if the loading of the
        configuration file fails and there is no fallback command map.

        Authors:
            Attila Kovacs
        """

        with pytest.raises(InvalidInputError):
            sut = CliProcessor(config_file='/invalid/config/file')

    @staticmethod
    def parser_callback(args: 'argparse.Namespace') -> None:

        """Callback function to test argument processing.

        Authors:
            Attila Kovacs
        """

        return

    def test_argument_parsing(self) -> None:

        """Tests that arguments are parsed correctly.

        Authors:
            Attila Kovacs
        """

        sut = CliProcessor(command_map=TEST_COMMAND_MAP)

        arguments = ['--switch-test', '--config-test2', 'testvalue']

        args = sut.process(
            args=arguments,
            cb_argument_processor=TestCliProcessor.parser_callback)

        assert args.switch_test
        assert args.config_test2 == 'testvalue'
