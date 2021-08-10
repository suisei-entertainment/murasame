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
Contains the implementation of the PasswordGenerator class.
"""

# Runtime Imports
import string
import secrets

class PasswordGenerator:

    """Utility class to generate simple passwords.

    Authors:
        Attila Kovacs
    """

    @staticmethod
    def generate(
        pwd_length: int = 12,
        allowed_chars: int = string.ascii_letters + string.digits + string.punctuation) -> str:

        """Generates a password.

        Args:
            pwd_length (int): The length of the password to generate.
            allowed_chars (int): The list of allowed characters in the password.

        Returns:
            str: The generated password as a string.

        Authors:
            Attila Kovacs
        """

        return ''.join(secrets.choice(allowed_chars) for _ in range(pwd_length))
