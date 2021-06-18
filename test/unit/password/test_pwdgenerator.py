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
Contains the unit tests of the PasswordGenerator class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.password import PasswordGenerator

class TestPasswordGenerator:

    """
    Contains the unit tests of the PasswordGenerator class.

    Authors:
        Attila Kovacs
    """

    def test_generation_single_character(self):

        """
        Tests password generation of a single character.

        Authors:
            Attila Kovacs
        """

        # STEP #1 - Generate a single character
        pwd = PasswordGenerator.generate(pwd_length=1)

        assert len(pwd) == 1

    def test_generation_multiple_characters(self):

        """
        Tests password generation of multiple characters.

        Authors:
            Attila Kovacs
        """

        pwd = PasswordGenerator.generate(pwd_length=12)

        assert len(pwd) == 12
