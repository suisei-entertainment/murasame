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
Contains the unit tests of the DictionaryBackend class.
"""

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.configuration.dictionarybackend import DictionaryBackend

class TestDictionaryBackend:

    """
    Test suite for the DictionaryBackend class.

    Authors:
        Attila Kovacs
    """

    def test_creation(self):

        """
        Tests that a dictionary backend can be created.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Simple creation test
        sut = DictionaryBackend()
        assert sut is not None

    def test_adding_groups(self):
        pass

    def test_adding_lists(self):
        pass

    def test_adding_attributes(self):
        pass

    def test_retrieving_attributes(self):
        pass

    def test_retrieving_groups(self):
        pass

    def test_retrieving_lists(self):
        pass

    def test_setting_attributes(self):
        pass