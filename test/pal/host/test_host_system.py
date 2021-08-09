
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
Contains the unit tests of HostSystem class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.host.hostsystem import HostSystem

# Test Imports
from test.constants import TEST_FILES_DIRECTORY

class TestHostSystem:

    """
    Contains the unit tests of HostSystem class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """
        Tests that a HostSystem instance can be created.

        Authors:
            Attila Kovacs
        """

        sut = HostSystem()
        assert sut is not None

    def test_initialization(self):

        """
        Tests that a HostSystem instane can be initialized.

        Authors:
            Attila Kovacs
        """

        sut = HostSystem()
        sut.initialize(geoip_database_path=TEST_FILES_DIRECTORY)
        assert sut.HostDescriptor is not None
