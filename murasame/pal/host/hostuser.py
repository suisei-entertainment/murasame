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
Contains the implementation of the HostUser class.
"""

# Runtime Imports
import os
import getpass
import pwd
import grp
from pathlib import Path

# Murasame Imports
from murasame.constants import MURASAME_PAL_LOG_CHANNEL
from murasame.log import LogWriter

class HostUser(LogWriter):

    """Utility class that provides information about the user running the
    application.

    Attributes:
        _username (str): The login name of the user.

        _user_id (int): The user ID of the user.

        _group_id (int): The group ID of the user.

        _group_name (str): The group name of the user.

        _home_dir (str): The home directory of the user.

    Authors:
        Attila Kovacs
    """

    @property
    def Username(self) -> str:

        """The login name of the user.

        Authors:
            Attila Kovacs
        """

        return self._username

    @property
    def UserID(self) -> int:

        """The user ID of the user.

        Authors:
            Attila Kovacs
        """

        return self._user_id

    @property
    def GroupID(self) -> int:

        """The group ID of the user.

        Authors:
            Attila Kovacs
        """

        return self._group_id

    @property
    def GroupName(self) -> str:

        """The group name of the user.

        Authors:
            Attila Kovacs
        """

        return self._group_name

    @property
    def HomeDirectory(self) -> Path:

        """Path to the home directory of the user.

        Authors:
            Attila Kovacs
        """

        return self._home_dir

    @property
    def IsRootUser(self) -> bool:

        """Returns whether or not the user is root.

        Authors:
            Attila Kovacs
        """

        return self._user_id == 0

    @property
    def HasRootPermissions(self) -> bool:

        """Returns whether or not the user has root permissions.

        Authors:
            Attila Kovacs
        """

        return os.geteuid() == 0

    def __init__(self) -> None:

        """Creates a new HostUser instannce.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name=MURASAME_PAL_LOG_CHANNEL,
                         cache_entries=True)

        self._username = None
        self._user_id = None
        self._group_id = None
        self._group_name = None
        self._home_dir = None

        self._detect_user()

    def _detect_user(self) -> None:

        """Executes the user detection logic.

        Authors:
            Attila Kovacs
        """

        # Get the login name of the user
        self._username = getpass.getuser()

        # Get the pwd database entry for the user.
        try:
            pwd_entry = pwd.getpwnam(self._username)
            self._user_id = pwd_entry.pw_uid
            self._group_id = pwd_entry.pw_gid
            self._home_dir = Path(pwd_entry.pw_dir)
            self.debug(f'Current user is {self._username}, '
                       f'UID={self._user_id}, GID={self._group_id}.')
        except KeyError:
            self.error(f'Failed to retrieve user information about '
                       f'user {self._username}.')

        # Get the group database entry for the user's group
        try:
            group_entry = grp.getgrgid(self._group_id)
            self._group_name = group_entry.gr_name
        except KeyError:
            self.error(f'Failed to retrieve group information about user '
                       f'{self._username}.')
