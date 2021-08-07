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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Murasame Imports
from murasame.password import PasswordComplexity

# Test data
COMMON_PASSWORD_LIST_PATH = os.path.abspath(os.path.expanduser('~/.murasame/testfiles/commonpwd.txt'))
COMMON_PASSWORD_LIST = "password1\npassword2\npassword3"
COMMON_PASSWORD_LIST_2 = "password1\npassword2\npassword3\npassword4"

class TestPasswordComplexity:

    @classmethod
    def setup_class(cls):

        with open(COMMON_PASSWORD_LIST_PATH, 'w') as pwd_file:
            pwd_file.write(COMMON_PASSWORD_LIST)

    @classmethod
    def teardown_class(cls):

        if os.path.isfile(COMMON_PASSWORD_LIST_PATH):
            os.remove(COMMON_PASSWORD_LIST_PATH)

    def test_creation(self):

        """
        Tests that the password complexity validator can be created.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity()
        assert sut is not None
        assert sut.validate(password='test')

    def test_length_validation_with_default_parameters(self):

        """
        Tests that passwords are validated for length correctly with default
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity()
        assert sut.validate(password='test')
        assert sut.validate(password='')
        assert sut.validate(password='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    def test_length_validation_with_minimum_length(self):

        """
        Tests that passwords are validated for length correctly with custom
        minimum length specified.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity(min_length=5)
        assert not sut.validate(password='test')
        assert sut.validate(password='test1')

    def test_lenggth_validation_with_maximum_length(self):

        """
        Tests that passwords are validated for length correctly with custom
        maximum length specified.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity(max_length=5)
        assert sut.validate(password='test')
        assert not sut.validate(password='test11')

    def test_character_validation_with_default_parameters(self):

        """
        Tests that passwords are validated for characters correctly with
        default parameters.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity()
        assert sut.validate(password='test')
        assert sut.validate(password='TEST')
        assert sut.validate(password='Test')

    def test_character_validation_with_lowercase_required(self):

        """
        Tests that passwords are validated for characters correctly with
        lowercase character requirement configured.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity(require_lower=True)
        assert sut.validate(password='test')
        assert not sut.validate(password='TEST')
        assert sut.validate(password='Test')

    def test_character_validation_with_uppercase_required(self):

        """
        Tests that passwords are validated for characters correctly with
        uppercase character requirement configured.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity(require_upper=True)
        assert not sut.validate(password='test')
        assert sut.validate(password='TEST')
        assert sut.validate(password='Test')

    def test_character_validation_with_lowercase_uppercase_required(self):

        """
        Tests that passwords are validated for characters correctly with
        lowercase and uppercase character requirement configured.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity(require_lower=True, require_upper=True)
        assert not sut.validate(password='test')
        assert not sut.validate(password='TEST')
        assert sut.validate(password='Test')

    def test_numerical_validation_with_default_parameters(self):

        """
        Tests that passwords are validated for numerical characters correctly
        with default parameters.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity()
        assert sut.validate(password='test')
        assert sut.validate(password='TEST')
        assert sut.validate(password='Test')
        assert sut.validate(password='1111')
        assert sut.validate(password='Test1')
        assert sut.validate(password='@')
        assert sut.validate(password='Test@')

    def test_numerical_validation_with_custom_parameters(self):

        """
        Tests that passwords are validated for numerical characters correctly
        with custom parameters.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity(require_number=True)
        assert not sut.validate(password='test')
        assert not sut.validate(password='TEST')
        assert not sut.validate(password='Test')
        assert sut.validate(password='1111')
        assert sut.validate(password='Test1')
        assert not sut.validate(password='@')
        assert not sut.validate(password='Test@')

    def test_symbol_required_with_default_parameters(self):

        """
        Tests that passwords are validated for symbols correctly with default
        parameters.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity()
        assert sut.validate(password='test')
        assert sut.validate(password='TEST')
        assert sut.validate(password='Test')
        assert sut.validate(password='1111')
        assert sut.validate(password='Test1')
        assert sut.validate(password='@')
        assert sut.validate(password='Test@')

    def test_symbol_required_with_custom_parameters(self):

        """
        Tests that passwords are validated for symbols correctly with custom
        parameters.

        Authors:
            Attila Kovacs
        """

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

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity(not_common=True,
                                 common_pwds=COMMON_PASSWORD_LIST_PATH)
        assert sut.validate(password='test')
        assert not sut.validate(password='password1')
        assert not sut.validate(password='password2')
        assert not sut.validate(password='password3')
        assert sut.validate(password='password4')

    def test_common_passwords_after_list_reload(self):

        """
        Tests that passwords can be validated against a common password list
        after reloading the list.

        Authors:
            Attila Kovacs
        """

        sut = PasswordComplexity(not_common=True,
                                 common_pwds=COMMON_PASSWORD_LIST_PATH)

        with open(COMMON_PASSWORD_LIST_PATH, 'w') as pwd_file:
            pwd_file.write(COMMON_PASSWORD_LIST_2)

        sut.reload()
        assert sut.validate(password='test')
        assert not sut.validate(password='password1')
        assert not sut.validate(password='password2')
        assert not sut.validate(password='password3')
        assert not sut.validate(password='password4')
