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
Contains the unit tests of the LogChannel class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.log import LogChannel, LogLevels

# Test data
BASIC_TEST_CONFIGURATION = \
{
    'name': 'testchannel',
    'defaultloglevel': 'INFO',
    'targets':
    []
}

TEST_CONFIGURATION_WITH_CONSOLE_TARGET = \
{
    'name': 'testchannel',
    'defaultloglevel': 'INFO',
    'targets':
    [
        {
            'type': 'console',
            'coloredlogs': 'True',
            'format': '[%(asctime)s][%(levelname)s]: %(message)s',
            'dateformat': '%Y-%m-%d %H:%M:%S'
        }
    ]
}

TEST_CONFIGURATION_WITH_FILE_TARGET = \
{
    'name': 'testchannel',
    'defaultloglevel': 'INFO',
    'targets':
    [
        {
            'type': 'file',
            'format': '[%(asctime)s][%(levelname)s]: %(message)s',
            'dateformat': '%Y-%m-%d %H:%M:%S',
            'filename': 'file_log_target.log',
            'maxsize': '5',
            'backupcount': '2'
        }
    ],
    '__log_root_path__': '~/.murasame/testfiles'
}

class TestLogChannel:

    """Contains all unit tests of the LogChannel class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self) -> None:

        """Tests that a log channel can be created.

        Authors:
            Attila Kovacs
        """

        sut = LogChannel(configuration=BASIC_TEST_CONFIGURATION)
        assert sut.Name == 'testchannel'
        assert sut.DefaultLogLevel == LogLevels.INFO

    def test_console_target_loading(self) -> None:

        """Tests that a console log target can be used in a log channel.

        Authors:
            Attila Kovacs
        """

        sut = LogChannel(configuration=TEST_CONFIGURATION_WITH_CONSOLE_TARGET)
        assert sut.Name == 'testchannel'
        assert sut.DefaultLogLevel == LogLevels.INFO

    def test_file_target_loading(self) -> None:

        """Tests that a file log target can be used in a log channel.

        Authors:
            Attila Kovacs
        """

        sut = LogChannel(configuration=TEST_CONFIGURATION_WITH_FILE_TARGET)
        assert sut.Name == 'testchannel'
        assert sut.DefaultLogLevel == LogLevels.INFO

    def test_syslog_target_loading(self) -> None:

        """Tests that a syslog log target can be used in a log channel.

        Authors:
            Attila Kovacs
        """

        pass

    def test_database_target_loading(self) -> None:

        """Tests that a database log target can be used in a log channel.

        Authors:
            Attila Kovacs
        """

        pass

    def test_structured_target_loading(self) -> None:

        """Tests that a structured log target can be used in a log channel.

        Authors:
            Attila Kovacs
        """

        pass
