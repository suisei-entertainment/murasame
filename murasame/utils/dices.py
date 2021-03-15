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
Contains the implementation of the Dices class.
"""

# Runtime Imports
import random

class Dices:

    """
    Utility class to help generate random numbers simulating dice rolls.

    Authors:
        Attila Kovacs
    """

    @staticmethod
    def roll(
        dice_d4: int = 0,
        dice_d6: int = 0,
        dice_d8: int = 0,
        dice_d10: int = 0,
        dice_d12: int = 0,
        dice_d20: int = 0,
        dice_d100: int = 0,
        base: int = 0):

        """
        Rolls the requested amount of dices.

        Args:
            dice_d4:     The amount of D4 dices to roll.
            dice_d6:     The amount of D6 dices to roll.
            dice_d8:     The amount of D8 dices to roll.
            dice_d10:    The amount of D10 dices to roll.
            dice_d12:    The amount of D12 dices to roll.
            dice_d20:    The amount of D20 dices to roll.
            dice_d100:   The amount of D100 dices to roll.
            base:   The base value to add the dice results to.
        """

        result = base

        # D4 dices
        for dummy in range(1, dice_d4 + 1):
            result += random.randint(1, 4)

        # D6 dices
        for dummy in range(1, dice_d6 + 1):
            result += random.randint(1, 6)

        # D8 dices
        for dummy in range(1, dice_d8 + 1):
            result += random.randint(1, 8)

        # D10 dices
        for dummy in range(1, dice_d10 + 1):
            result += random.randint(1, 10)

        # D12 dices
        for dummy in range(1, dice_d12 + 1):
            result += random.randint(1, 12)

        # D20 dices
        for dummy in range(1, dice_d20 + 1):
            result += random.randint(1, 20)

        # D100 dices
        for dummy in range(1, dice_d100 + 1):
            result += random.randint(1, 100)

        return result
