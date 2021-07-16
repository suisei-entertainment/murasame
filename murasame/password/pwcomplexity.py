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
Contains the implementation of the PasswordComplexity class.
"""

# Runtime Imports
import os
import re

class PasswordComplexity:

    """Utility class that implements a simple password complexity validator.

    Attributes:
        _min_length (int): The minimum allowed password length. 0 means no
            minimum length.

        _max_length (int): The maximum allowed password length. 0 means no
            maximum length.

        _require_lower (bool): Whether or not the password must contain a
            lowercase character.

        _require_upper (bool): Whether or not the password must contain an
            uppercase character.

        _require_number (bool): Whether or not the password must contains an
            uppercase character.

        _require_symbol (bool): Whether or not the password must contains a
            symbol.

        _not_common (bool): Whether passwords on the most common password list
            are accepted.

        _common_pwd_path (str): Path to the file containing the passwords
            considered common.

    Authors:
        Attila Kovacs
    """

    def __init__(
        self,
        min_length: int = 0,
        max_length: int = 0,
        require_lower: bool = False,
        require_upper: bool = False,
        require_number: bool = False,
        require_symbol: bool = False,
        not_common: bool = False,
        common_pwds: str = None) -> None:

        """Creates a new PasswordComplexity instance.

        Args:
            min_length (int): The minimum allowed password length. 0 means no
                minimum length.

            max_length (int):The maximum allowed password length. 0 means no
                maximum length.

            require_lower (bool): Whether or not the password must contain a
                lowercase character.

            require_upper (bool): Whether or not the password must contain an
                uppercase character.

            require_number (bool): Whether or not the password must contains an
                uppercase character.

            require_symbol (bool): Whether or not the password must contains a
                symbol.

            not_common: Whether passwords on the most common password list
                are accepted.

            common_pwds: Path to the file containing the passwords considered
                common.

        Authors:
            Attila Kovacs
        """

        self._min_length = min_length
        self._max_length = max_length
        self._require_lower = require_lower
        self._require_upper = require_upper
        self._require_number = require_number
        self._require_symbol = require_symbol
        self._not_common = not_common
        self._common_pwd_path = common_pwds

        if self._not_common:
            self._load_common_passwords(common_pwds=common_pwds)

    def validate_length(self, password: str) -> bool:

        """Validates the given password against configured length rules.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: 'True' if the given password is valid, 'False' if it
                validates at least one complexity requirement.

        Authors:
            Attila Kovacs
        """

        # Validate password length
        length = len(password)

        if self._min_length != 0 and length < self._min_length:
            return False

        if self._max_length != 0 and length > self._max_length:
            return False

        return True

    def validate_case(self, password: str) -> bool:

        """Validates the given password against configured case rules.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: 'True' if the given password is valid, 'False' if it
                validates at least one complexity requirement.

        Authors:
            Attila Kovacs
        """

        if self._require_lower:
            has_lowercase = re.search(r"[a-z]", password) is not None
            if not has_lowercase:
                return False

        if self._require_upper:
            has_uppercase = re.search(r"[A-Z]", password) is not None
            if not has_uppercase:
                return False

        return True

    def validate_numbers(self, password: str) -> bool:

        """Validates the given password against the configured numeric rules.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: 'True' if the given password is valid, 'False' if it
                validates at least one complexity requirement.

        Authors:
            Attila Kovacs
        """

        if self._require_number:
            has_number = re.search(r"\d", password) is not None
            if not has_number:
                return False

        return True

    def validate_symbols(self, password: str) -> bool:

        """Validates the given password against the configured symbol rules.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: 'True' if the given password is valid, 'False' if it
                validates at least one complexity requirement.

        Authors:
            Attila Kovacs
        """

        if self._require_symbol:
            has_symbol = re.search(r"\W", password) is not None
            if not has_symbol:
                return False

        return True

    def validate_against_common_passwords(self, password: str) -> bool:

        """Validates the given password against the common passwords list.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: 'True' if the given password is valid, 'False' if it
                validates at least one complexity requirement.

        Authors:
            Attila Kovacs
        """

        if self._not_common and password in self._common_passwords:
            return False

        return True

    def validate(self, password: str) -> bool:

        """Validates the given password against all the configured rules.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: 'True' if the given password is valid, 'False' if it
                validates at least one complexity requirement.

        Authors:
            Attila Kovacs
        """

        # Validate password length
        if not self.validate_length(password):
            return False

        # Validate characters
        if not self.validate_case(password):
            return False

        if not self.validate_numbers(password):
            return False

        if not self.validate_symbols(password):
            return False

        # Validate against common passwords
        if not self.validate_against_common_passwords(password):
            return False

        return True

    def reload(self) -> None:

        """Reloads the list of common passwords.

        Authors:
            Attila Kovacs
        """

        if self._common_pwd_path is not None:
            self._load_common_passwords(common_pwds=self._common_pwd_path)

    def _load_common_passwords(self, common_pwds: str) -> None:

        """Loads the common passwords list from a file to memory.

        The file is expected to be a simple text file with each line
        representing a single common password.

        Args:
            common_pwds (str): Path to the file containing the list of
                passwords that are to be considered common.

        Raises:
            FileNotFoundError: Raised if the given password list file is not
                found.

            RuntimeError: Raised if the given password list file cannot be
                loaded.

        Authors:
            Attila Kovacs
        """

        self._common_passwords = []

        # Load list from the file
        common_pwds = os.path.abspath(os.path.expanduser(common_pwds))

        if not os.path.isfile(common_pwds):
            raise FileNotFoundError(
                f'The common password list ({common_pwds}) was not found.')

        try:
            with open(common_pwds, 'r') as pwd_file:
                passwords = pwd_file.readlines()
        except IOError as error:
            raise RuntimeError(
                f'Failed to load the common password '
                f'list from {common_pwds}.') from error

        for pwd in passwords:
            self._common_passwords.append(pwd.strip())
