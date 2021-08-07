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
Contains the implementation of the Murasame Development Environment tool.
"""

# Platform Imports
import os
import logging

# Dependency Imports

# MDE Imports
from mde.packaging import BuildTypes
from mde.constants import MDE_LOGGER_NAME, MDE_LOG_LEVEL, MDE_BANNER
from mde.utils.loghelper import initialize_logging
from mde.utils.commandline import parse_command_line
from mde.utils.version import get_version_string
from mde.mde import execute_mde

## ============================================================================
##      >>> MAIN <<<
## ============================================================================
def main() -> int:

    """The entry point of the MDE tool.

    Authors:
        Attila Kovacs
    """

    # Print banner
    print(MDE_BANNER)
    print(f'             ---=== Murasame Development Environment {get_version_string()}===---')
    print('')

    # Configure argument parser and parse command line
    args = parse_command_line()


    # Enable debug mode if requested through the command line
    log_level = 'DEBUG' if args.debug_mode else MDE_LOG_LEVEL

    # Initialize log according to the configured log level. This will also
    # enable colored logs, if the package is available in the host system.
    initialize_logging(log_level=log_level)

    # Execute MDE based on the command line arguments
    return execute_mde(arguments=args)

if __name__ == '__main__':
    main()