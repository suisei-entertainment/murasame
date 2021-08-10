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
Contains the implementation of the CliProcessor class.
"""

# Runtime Imports
import os
import sys
import argparse
from typing import Callable

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils.jsonfile import JsonFile

class CliProcessor:

    """Utility class based on argparse to simplify the configuration and
    processing of CLI commands.

    Attributes:
        _parser (ArgumentParser): The wrapped ArgumentParser instance.

    Authors:
        Attila Kovacs
    """

    @property
    def Parser(self) -> argparse.ArgumentParser:

        """Provides access to the underlying ArgumentParser object.

        Authors:
            Attila Kovacs
        """

        return self._parser

    def __init__(self,
                 command_map: list = None,
                 config_file: str = None,
                 description_string: str = None,
                 usage_string: str = None,
                 epilog_string: str = None) -> None:

        """Creates a new CliProcessor instance.

        Args:
            command_map (list): The command map to use to configure the class.

            config_file (str): Optional path to config file containing the
                command map to use. If a path is provided, it will overwrite
                the command map.

            description_string (str): Optional description string to pass to
                argparse.

            usage_string (str): Optional usage string to pass to argparse.

            epilog_string (str): Optional epilog string to pass to argparse.

        Raises:
            InvalidInputError: Raised if the config file cannot be loaded and
                there is no command map provided.

            InvalidInputError: Raised if command registration failed.

        Authors:
            Attila Kovacs
        """

        # Check that either a command map or a config file is provided.
        if command_map is None and config_file is None:
            raise InvalidInputError(
                'Either a command map or a config file has to be provided to '
                'configure the command line processor.')

        # Basic setup of argument parser
        self._parser = argparse.ArgumentParser(
            description=description_string,
            usage=usage_string,
            epilog=epilog_string)

        # Load the config file if it is provided
        if config_file:
            config_file = os.path.abspath(os.path.expanduser(config_file))

        if config_file:
            if os.path.isfile(config_file):
                conf = JsonFile(path=config_file)

                try:
                    conf.load()
                    command_map = conf.Content
                except InvalidInputError:
                    # If the config file cannot be loaded, fall back to the
                    # command map if it has been provided, only raise the
                    # exception if it's not available.
                    if not command_map:
                        raise
            elif not command_map:
                raise InvalidInputError(
                    f'The specified configuration file ({config_file}) '
                    f'doesn\'t exist and there is no command map provided '
                    'as fallback.')

        # Configure commands
        self._register_commands(command_map)

    def process(self,
                cb_argument_processor: Callable,
                args: list = None) -> argparse.Namespace:

        """Processes the command line arguments.

        Args:
            cb_argument_processor (Callable): A callback function that will be
                called after the command line has been parsed.

            args (list): The list of command line arguments the application was
                called with. If this parameter is not supplied, the arguments
                will be automatically retrieved.

        Returns:
            argparse.Namespace: The processed command line arguments as an
                argparse Namespace object.

        Authors:
            Attila Kovacs
        """

        # Automatically retrieve the command line arguments the application was
        # started with if it is not supplied
        if args is None:
            args = sys.argv[1:]

        # Parse the CLI arguments
        arguments = self._parser.parse_args(args=args)

        # Process arguments
        if arguments:
            cb_argument_processor(arguments)

        return arguments

    def _register_commands(self, command_map: list) -> None:

        """Registers all CLI commands from the command map with the argument
        parser.

        Args:
            command_map (list): The command map to configure.

        Raises:
            InvalidInputErrorL Raised when the provided command map does not
                contain a valid command list.

            InvalidInputError: Raised when the type of a command map element
                cannot be determined.

            InvalidInputError: Raised when the element cannot be properly
                parsed.

        Authors:
            Attila Kovacs
        """

        try:
            commands = command_map['commands']
        except KeyError as error:
            raise InvalidInputError(
                'The provided command map does not contain a valid command '
                'list.') from error

        # Iterate over the command map and process the content
        for element in commands:
            try:
                element_type = element['type']
            except KeyError as exception:
                raise InvalidInputError(
                    f'Failed to determine the type of an element in the '
                    f'command map. No type field was found. '
                    f'Element: {element}') from exception
            except TypeError as error:
                raise InvalidInputError(
                    f'Failed to parse the element descriptor {element} '
                    'properly.') from error

            if element_type == 'group':
                self._register_group(element)
            elif element_type == 'switch':
                self._register_switch(element=element, target=self._parser)
            elif element_type == 'config':
                self._register_config(element=element, target=self._parser)
            else:
                raise InvalidInputError(
                    f'Unknown command type {element_type} encountered.')

    def _register_group(self, element: dict) -> None:

        """Registers a new command group in the parser.

        Args:
            element (dict): The group descriptor to register.

        Raises:
            InvalidInputError:  Raised when the name or description of a
                command group is not specified in the configuration.

            InvalidInputError:  Raised when there is no command list specified
                in the configuration.

            InvalidInputError:  Raised when there is no command type specified
                for a command in the command group.

            InvalidInputError:  Raised when an invalid command type is
                encountered.

        Authors:
            Attila Kovacs
        """

        # Get group parameters
        try:
            name = element['name']
            description = element['description']
        except KeyError as exception:
            raise InvalidInputError(
                f'Command group name or description was not found in '
                f'element {element}') from exception

        # Add the group to the parser
        group = self._parser.add_argument_group(name, description=description)

        # Add commands to the group
        commands = None

        # Get commands
        try:
            commands = element['commands']
        except KeyError as exception:
            raise InvalidInputError(
                f'No commands list was found in command group '
                f'{name}') from exception

        # Register all commands based on type
        for command in commands:

            try:
                command_type = command['type']
            except KeyError as exception:
                raise InvalidInputError(
                    f'No command type specified in command '
                    f'{command}') from exception

            if command_type == 'switch':
                self._register_switch(element=command, target=group)
            elif command_type == 'config':
                self._register_config(element=command, target=group)
            else:
                raise InvalidInputError(
                    'Invalid command type {} encountered.'.format(
                        command_type))

    @staticmethod
    def _register_switch(element: dict, target: object) -> None:

        """Registers a new switch type command in the parser.

        Args:
            element (dict): The command descriptor to register.

            target (object): Where the command will be registered. Either the
                parser itself, or an argument group.

        Raises:
            InvalidInputError: Raised when a mandatory parameter is missing
                from the configuration.

        Authors:
            Attila Kovacs
        """

        short_key = None
        command = None
        helptext = None

        try:
            short_key = element['shortkey']
            command = element['command']
            helptext = element['help']
        except KeyError as exception:
            raise InvalidInputError(
                f'Missing parameters when processing switch command '
                f'{element}') from exception

        default = None
        try:
            default = element['default']
        except KeyError:
            default = False

        if short_key == '':
            target.add_argument(command,
                                help=helptext,
                                action='store_true',
                                default=default)
        else:
            target.add_argument(short_key,
                                command,
                                help=helptext,
                                action='store_true',
                                default=default)

    @staticmethod
    def _register_config(element: dict, target: object) -> None:

        """Registers a new config option type command in the parser.

        Args:
            element (dict): The command descriptor to register.

            target (object): Where the command will be registered. Either the
                parser itself, or an argument group.

        Raises:
            InvalidInputError: Raised when a mandatory parameter is missing
                from the configuration.

        Authors:
            Attila Kovacs
        """

        short_key = None
        command = None
        helptext = None

        try:
            short_key = element['shortkey']
            command = element['command']
            helptext = element['help']
        except KeyError as exception:
            raise InvalidInputError(
                f'Missing parameters when processing switch command '
                f'{element}') from exception

        metavar = None
        try:
            metavar = element['metavar']
        except KeyError:
            metavar = False

        if short_key == '':
            target.add_argument(command,
                                help=helptext,
                                action='store',
                                metavar=metavar)
        else:
            target.add_argument(short_key,
                                command,
                                help=helptext,
                                action='store',
                                metavar=metavar)
