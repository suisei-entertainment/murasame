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

# Platform Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.password import PasswordComplexity

# Test data
COMMON_PASSWORD_LIST_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/commonpwd.txt'))
COMMON_PASSWORD_LIST = "password1\npassword2\npassword3"
COMMON_PASSWORD_LIST_2 = "password1\npassword2\npassword3\npassword4"

class TestPasswordComplexity:

    def test_creation(self):

        """
        Tests that the password complexity validator can be created.
        """

        # STEP #1 - Creation with default parameters
        sut = PasswordComplexity()
        assert sut is not None
        assert sut.validate(password='test')

    def test_length_validation(self):

        """
        Tests that passwords are validated for length correctly.
        """

        # STEP #1 - Test with default parameters
        sut = PasswordComplexity()
        assert sut.validate(password='test')
        assert sut.validate(password='')
        assert sut.validate(password='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

        # STEP #2 - Test with configured minimum length
        sut = PasswordComplexity(min_length=5)
        assert not sut.validate(password='test')
        assert sut.validate(password='test1')

        # STEP #3 - Test with configured maximum length
        sut = PasswordComplexity(max_length=5)
        assert sut.validate(password='test')
        assert not sut.validate(password='test11')

    def test_character_validation(self):

        """
        Tests that passwords are validated for characters correctly.
        """

        # STEP #1 - Test with default parameters
        sut = PasswordComplexity()
        assert sut.validate(password='test')
        assert sut.validate(password='TEST')
        assert sut.validate(password='Test')

        # STEP #2 - Test with lowercase required
        sut = PasswordComplexity(require_lower=True)
        assert sut.validate(password='test')
        assert not sut.validate(password='TEST')
        assert sut.validate(password='Test')

        # STEP #3 - Test with uppercase required
        sut = PasswordComplexity(require_upper=True)
        assert not sut.validate(password='test')
        assert sut.validate(password='TEST')
        assert sut.validate(password='Test')

        # STEP #4 - Test with lower and uppercase required
        sut = PasswordComplexity(require_lower=True, require_upper=True)
        assert not sut.validate(password='test')
        assert not sut.validate(password='TEST')
        assert sut.validate(password='Test')

    def test_numerical_validation(self):

        """
        Tests that passwords are validated for numerical characters correctly.
        """

        # STEP #1 - Test with default parameters
        sut = PasswordComplexity()
        assert sut.validate(password='test')
        assert sut.validate(password='TEST')
        assert sut.validate(password='Test')
        assert sut.validate(password='1111')
        assert sut.validate(password='Test1')
        assert sut.validate(password='@')
        assert sut.validate(password='Test@')

        # STEP #2 - Test with number required
        sut = PasswordComplexity(require_number=True)
        assert not sut.validate(password='test')
        assert not sut.validate(password='TEST')
        assert not sut.validate(password='Test')
        assert sut.validate(password='1111')
        assert sut.validate(password='Test1')
        assert not sut.validate(password='@')
        assert not sut.validate(password='Test@')

    def test_symbol_required(self):

        """
        Tests that passwords are validated for symbols correctly.
        """

        # STEP #1 - Test with default parameters
        sut = PasswordComplexity()
        assert sut.validate(password='test')
        assert sut.validate(password='TEST')
        assert sut.validate(password='Test')
        assert sut.validate(password='1111')
        assert sut.validate(password='Test1')
        assert sut.validate(password='@')
        assert sut.validate(password='Test@')

        # STEP #2 - Test with symbol required
        sut = PasswordComplexity(require_symbol=True)
        assert not sut.validate(password='test')
        assert not sut.validate(password='TEST')
        assert not sut.validate(password='Test')
        assert not sut.validate(password='1111')
        assert not sut.validate(password='Test1')
        assert sut.validate(password='@')
        assert sut.validate(password='Test@')

    def test_common_passwords(self):

        """
        Tests that passwords can be validated against a common password list.
        """

        # Setup
        with open(COMMON_PASSWORD_LIST_PATH, 'w') as pwd_file:
            pwd_file.write(COMMON_PASSWORD_LIST)

        # STEP #1 - Test against password list
        sut = PasswordComplexity(not_common=True,
                                 common_pwds=COMMON_PASSWORD_LIST_PATH)
        assert sut.validate(password='test')
        assert not sut.validate(password='password1')
        assert not sut.validate(password='password2')
        assert not sut.validate(password='password3')
        assert sut.validate(password='password4')

        # STEP #2 - Test against reloaded password list
        with open(COMMON_PASSWORD_LIST_PATH, 'w') as pwd_file:
            pwd_file.write(COMMON_PASSWORD_LIST_2)

        sut.reload()
        assert sut.validate(password='test')
        assert not sut.validate(password='password1')
        assert not sut.validate(password='password2')
        assert not sut.validate(password='password3')
        assert not sut.validate(password='password4')
