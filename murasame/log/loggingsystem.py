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
Contains the implementation of the LoggingSystem class.
"""

# Runtime Imports
import os
from typing import Union

# Murasame Imports
from murasame.constants import MURASAME_LOGGING_CONFIG
from murasame.exceptions import InvalidInputError
from murasame.utils import JsonFile
from murasame.log.logchannel import LogChannel
from murasame.log.defaultlogconfig import DEFAULT_LOG_CONFIG

class LoggingSystem:

    """Default log system implementation.

    Attributes:
        _channels (dict): The log channels registered in the log system.

        _root_path (str): The root path in the file system where log files are
            written.

    Authors:
        Attila Kovacs
    """

    @property
    def RootPath(self) -> str:

        """The root path of the log system where log files for file log
        targets are written.

        Authors:
            Attila Kovacs
        """

        return  self._root_path

    def __init__(self) -> None:

        """Creates a new LoggingSystem instance.

        Since log is one of the most basic functionalities, it should work
        even if the higher level systems fail, so log doesn't use the
        normal configuration mechanism of the framework, but instead tries to
        load and parse the configuration file itself.

        If no log configuration is found, it will start with a default
        log configuration for the framework.

        Authors:
            Attila Kovacs
        """

        self._channels = {}
        self._root_path = None

        if not self._load_configuration():
            self._load_default_configuration()

    def has_channel(self, name: str) -> bool:

        """Returns whether or not a given log channel is registered in the
        log system.

        Args:
            name (str): The name of the log channel to check.

        Returns:
            bool: 'True' if the given log channel is registered, 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        return name in self._channels

    def get_channel(self, name: str) -> Union['LogChannel', None]:

        """Returns a given log channel.

        Args:
            name (str): Name of the channel to retrieve.

        Authors:
            Attila Kovacs
        """

        if self.has_channel(name):
            return self._channels[name]

        return None

    def _load_configuration(self) -> bool:

        """Loads the log configuration from the config file.

        Returns:
            bool: 'True' if the configuration was loaded successfully 'False'
                otherwise.

        Authors:
            Attila Kovacs
        """

        config_path = MURASAME_LOGGING_CONFIG

        # Check whether or not there is a log configuration file in the
        # config directory of the application
        if not os.path.isfile(config_path):
            return False

        # Load the configuration file
        config_file = JsonFile(path=config_path)
        config_file.load()
        config = config_file.Content

        # Get the root log path from the configuration
        if not 'rootpath' in config:
            return False

        self._root_path = os.path.abspath(os.path.expanduser(config['rootpath']))

        # Create the root log directory if it doesn't exist
        if not os.path.isdir(self._root_path):
            try:
                os.makedirs(self._root_path, exist_ok=True)
            except OSError:
                # Failed to create the root path
                return False

        # Check for log channel configuration
        if not 'channels' in config:
            return False

        channels = config['channels']

        for channel in channels:

            # Append the root path to the configuration to the channel for
            # file log targets
            channel['__log_root_path__'] = self._root_path

            try:
                log_channel = LogChannel(configuration=channel)
                self._channels[log_channel.Name] = log_channel
            except InvalidInputError:
                # Don't fail if the configuration of a channel is wrong
                continue

        return True

    def _load_default_configuration(self) -> None:

        """Loads the default log system configuration.

        Raises:
            RuntimeError: Raised if the root log directory cannot be
                created.

            InvalidInputError: Raised if the default log configuration
                contains an error.

        Authors:
            Attila Kovacs
        """

        self._root_path = os.path.abspath(os.path.expanduser(DEFAULT_LOG_CONFIG['rootpath']))

        if not os.path.isdir(self._root_path):
            try:
                os.makedirs(self._root_path, exist_ok=True)
            except OSError as error:
                raise RuntimeError(f'Failed to create the root log '
                                   f'directory: {self._root_path}') from error

        for channel in DEFAULT_LOG_CONFIG['channels']:

            # Append the root path to the configuration to the channel for
            # file log targets
            channel['__log_root_path__'] = self._root_path

            try:
                log_channel = LogChannel(configuration=channel)
                self._channels[log_channel.Name] = log_channel
            except InvalidInputError as error:
                raise InvalidInputError(
                    'Invalid default log configuration.') from error
