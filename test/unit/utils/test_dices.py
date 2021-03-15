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
Contains the unit tests of the Dices class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.utils.dices import Dices

class TestDices:

    """
    Contains the unit tests for the Dices class.
    """

    def test_dice_rolling(self):

        """
        Tests random number generation by throwing dices.
        """

        assert Dices.roll() == 0
        assert Dices.roll(base=10) == 10
        assert Dices.roll(
            dice_d4=1,
            dice_d6=1,
            dice_d8=1,
            dice_d10=1,
            dice_d12=1,
            dice_d20=1,
            dice_d100=1,
            base=10) >= 17
        assert Dices.roll(
            dice_d4=2,
            dice_d6=2,
            dice_d8=2,
            dice_d10=2,
            dice_d12=2,
            dice_d20=2,
            dice_d100=2,
            base=10) >= 24
