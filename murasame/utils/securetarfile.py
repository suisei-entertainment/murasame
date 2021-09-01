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
Contains the implementation of the SecureTarFile class.
"""

# Runtime Imports
import os
import pathlib
import tarfile

# Murasame Imports
from murasame.exceptions import SecurityValidationError
from murasame.constants import (
    MURASAME_IO_LOG_CHANNEL,
    MURASAME_TAR_MAX_MEMBER_COUNT,
    MURASAME_TAR_MAX_MEMBER_SIZE)
from murasame.log import LogWriter

# List of file extensions to be blocked if they are inside the tar file.
BLOCKED_EXTENSIONS = \
[
    'zip',
    'rar',
    'arj',
    'gz',
    'tar',
    '7z',
    'bz2'
]

class SecureTarFile(tarfile.TarFile):

    """Utility class that extends Python's tarfile implementation with
    additional security checks against potential ZipBomb attacks.

    This implementation is based on the tarsafe implementation at
    https://github.com/beatsbears/tarsafe.

    Authors:
        Attila Kovacs
    """

    def __init__(self, *args, **kwargs) -> None:

        """Creates a new SecureTarFile instance.

        Args:
            *args (list): List of unnamed arguments.
            **kwargs (dict): List of named arguments.

        Authors:
            Attila Kovacs
        """

        super().__init__(*args, **kwargs)

        self._logger = LogWriter(channel_name=MURASAME_IO_LOG_CHANNEL,
                                 cache_entries=True)

        self._checks = []

        # Register all security checks
        self._checks.append(self._check_traversal_attempt)
        self._checks.append(self._check_unsafe_symlink)
        self._checks.append(self._check_unsafe_link)
        self._checks.append(self._check_is_device)
        self._checks.append(self._check_blacklisted_extension)
        self._checks.append(self._check_member_size)

    @classmethod
    def open(
        cls,
        name: str = None,
        mode: str = "r",
        fileobj: object = None,
        bufsize: int = tarfile.RECORDSIZE,
        **kwargs: dict) -> tarfile.TarFile:

        """Opens a tar file.

        Args:
            name (str): Path to the tar file to open.

            mode (str): The mode to access the tar file.

            fileobj (object): If fileobj is specified, it is used as an
                alternative to a file object opened in binary mode for name.
                It is supposed to be at position 0.

            bufsize (int): The block size to use when opening the file.

            **kwargs (dict): List of additional parameters.

        Returns:
            (tarfile.TarFile): The opened tar file represented by a TarFile
                object.

        """

        logger = LogWriter(channel_name=MURASAME_IO_LOG_CHANNEL,
                           cache_entries=True)
        logger.debug(f'Opening tarfile. Name: {name} Mode: {mode} FileObj: '
                     f'{fileobj} Buffer size: {bufsize} Additional '
                     f'parameters: {kwargs}')
        return super().open(name, mode, fileobj, bufsize, **kwargs)

    def extract(
        self,
        member: tarfile.TarInfo,
        path: str = "",
        set_attrs: bool = True,
        *,
        numeric_owner: bool = False) -> None:

        """Extracts the given member from the archive after performing the
        security checks.

        Args:
            member (tarfile.TarInfo): The TarInfo object representing the
                member to extract.

            path (str): Path to the directory where the member will be
                extracted.

            set_attrs (bool): Whether or not file attributes should be set
                after extraction.

            numeric_owner (bool): Whether or not to use UID and GID from the
                archive.

        Authors:
            Attila Kovacs
        """

        self._run_checks(path=path)
        super().extract(member,
                        path,
                        set_attrs=set_attrs,
                        numeric_owner=numeric_owner)

    def extractall(
        self,
        path: str = ".",
        members: list = None,
        *,
        numeric_owner: bool = False) -> None:

        """Extracts multiple members from the archive after performing the
        security checks.

        Args:
            path (str): Path to the directory where the members will be
                extracted.

            members (list): List of tarfile.TarInfo objects to extract from the
                archive. If not specified, all members will be extracted.

            numeric_owner (bool): Whether or not to use UID and GID from the
                archive.

        Authors:
            Attila Kovacs
        """

        self._run_checks(path=path)
        super().extractall(path, members, numeric_owner=numeric_owner)

    def _run_checks(self, path: str) -> None:

        """Executes all registered checks on the tar file.

        Args:
            path (str): Path where the contents of the archive would be
                extracted.

        Authors:
            Attila Kovacs
        """

        try:
            # Checks member count
            if len(self.getmembers()) > MURASAME_TAR_MAX_MEMBER_COUNT:
                raise SecurityValidationError(
                    f'The amount of members in the archive {self.name} '
                    f'exceeds the maximum amount of {MURASAME_TAR_MAX_MEMBER_COUNT}.')

            # Check members
            for tarinfo in self.__iter__():
                for check in self._checks:
                    check(tarinfo=tarinfo, path=path)
        except SecurityValidationError as error:
            self._logger.error(f'Tarfile security check failed with error: '
                               f'{error}')
            raise

    @staticmethod
    def _check_traversal_attempt(tarinfo: tarfile.TarInfo, path: str) -> None:

        """Checks for attempted directory traversal.

        Args:
            tarinfo (tarfile.TarInfo): The object to validate.

            path (str): Path where the contents of the archive would be
                extracted.

        Raises:
            SecurityValidationError: Raised when the object fails the check.

        Authors:
            Attila Kovacs
        """

        if '..' in tarinfo.name:
            raise SecurityValidationError(
                f'Attempted directory traversal for member: {tarinfo.name}')

        if not os.path.abspath(
            os.path.join(path, tarinfo.name)).startswith(path):
            raise SecurityValidationError(
                f'Attempted directory traversal for member: {tarinfo.name}')

    @staticmethod
    def _check_unsafe_symlink(tarinfo: tarfile.TarInfo, path: str) -> None:

        """Checks for attempted directory traversal through a symlink.

        Args:
            tarinfo (tarfile.TarInfo): The object to validate.

            path (str): Path where the contents of the archive would be
                extracted.

        Raises:
            SecurityValidationError: Raised when the object fails the check.

        Authors:
            Attila Kovacs
        """

        if tarinfo.issym():
            symlink_file = pathlib.Path(
                os.path.normpath(os.path.join(path, tarinfo.linkname)))
            if not os.path.abspath(
                os.path.join(path, symlink_file)).startswith(path):
                raise SecurityValidationError(
                    f'Attempted directory traversal via symlink for member: '
                    f'{tarinfo.linkname}')

    @staticmethod
    def _check_unsafe_link(tarinfo: tarfile.TarInfo, path: str) -> None:

        """Checks for attempted directory traversal through a link.

        Args:
            tarinfo (tarfile.TarInfo): The object to validate.

            path (str): Path where the contents of the archive would be
                extracted.

        Raises:
            SecurityValidationError: Raised when the object fails the check.

        Authors:
            Attila Kovacs
        """

        if tarinfo.islnk():
            link_file = pathlib.Path(
                os.path.normpath(os.path.join(path, tarinfo.linkname)))
            if not os.path.abspath(
                os.path.join(path, link_file)).startswith(path):
                raise SecurityValidationError(
                    f'Attempted directory traversal via link for member: '
                    f'{tarinfo.linkname}')

    @staticmethod
    def _check_is_device(tarinfo: tarfile.TarInfo, path: str) -> None:

        """Checks that the object is not reported to be a character or block
        device.

        Args:
            tarinfo (tarfile.TarInfo): The object to validate.

            path (str): Path where the contents of the archive would be
                extracted.

        Raises:
            SecurityValidationError: Raised when the object fails the check.

        Authors:
            Attila Kovacs
        """

        if tarinfo.ischr() or tarinfo.isblk():
            raise SecurityValidationError(
                'Tarfile returns true for isblk() or ischr().')

    @staticmethod
    def _check_blacklisted_extension(
        tarinfo: tarfile.TarInfo,
        path: str) -> None:

        """Checks that the object does not have an extension that matches an
        element of the block list.

        Args:
            tarinfo (tarfile.TarInfo): The object to validate.

            path (str): Path where the contents of the archive would be
                extracted.

        Raises:
            SecurityValidationError: Raised when the object fails the check.

        Authors:
            Attila Kovacs
        """

        for blocked_extension in BLOCKED_EXTENSIONS:
            if tarinfo.name.endswith(blocked_extension):
                raise SecurityValidationError(
                    f'Blocked file extension ({blocked_extension}) detected '
                    f'inside the archive. Member: {tarinfo.name}')

    @staticmethod
    def _check_member_size(tarinfo: tarfile.TarInfo, path: str) -> None:

        if tarinfo.size > MURASAME_TAR_MAX_MEMBER_SIZE:
            raise SecurityValidationError(
                f'Size of member {tarinfo.name} exceeds the maximum allowed '
                f'size of {MURASAME_TAR_MAX_MEMBER_SIZE} bytes.')
