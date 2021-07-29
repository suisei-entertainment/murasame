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
Contains common MDE functions.
"""

# Runtime Imports
import logging
from enum import IntEnum

# MDE Imports
from mde.constants import MDE_LOGGER_NAME
from mde.utils.version import bump_version_number
from mde.utils.constantsfile import create_constants_file
from mde.packaging.wheel import create_wheel

class MDEModes(IntEnum):

    """List of supported MDE operational modes.

    Attributes:
        UNKNOWN: Unknown operational mode.
        BUILD: Package build mode.
        RELEASE: Package release mode.

    Authors:
        Attila Kovacs
    """

    UNKNOWN = -1
    BUILD = 0
    RELEASE = 1

class MDEReturnCodes(IntEnum):

    """List of possible return codes for MDE.

    Arguments:
        SUCCESS: The execution was successful.
        INVALID_MODE: Invalid operational mode was specified for MDE.

    Authors:
        Attila Kovacs
    """

    SUCCESS = 0
    INVALID_MODE = 1

def select_mde_mode(arguments: 'argparse.Namespace') -> MDEModes:

    """Selects the operational mode of MDE based on the provided command line
    arguments.

    Args:
        arguments (argparse.Namespace): The parsed command line arguments the
            tool has been started with.

    Returns:
        MDEModes: The selected MDE operational mode.

    """

    if arguments.build_type is not None:
        return MDEModes.BUILD

    if arguments.release:
        return MDEModes.RELEASE

    return  MDEModes.UNKNOWN

def execute_mde(arguments: 'argparse.Namespace') -> MDEReturnCodes:

    """Contains the main execution logic of the MDE.

    Args:
        arguments (argparse.Namespace): The parsed command line arguments the
            tool has been started with.

    Returns:
        MDEReturnCodes: The overall return code of the application.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug('Executing MDE...')

    mde_mode = select_mde_mode(arguments=arguments)

    if mde_mode == MDEModes.UNKNOWN:
        logger.error('Unknown MDE operational mode was specified, exiting.')
        return MDEReturnCodes.INVALID_MODE
    elif mde_mode == MDEModes.RELEASE:
        return mde_release(arguments=arguments)

    return mde_build(arguments=arguments)

def mde_build(arguments: 'argparse.Namespace') -> MDEReturnCodes:

    """Creates a new package build for the framework.

    Args:
        arguments (argparse.Namespace): The parsed command line arguments.

    Returns:
        MDEReturnCodes: One of the supported MDE return codes.

    Authors:
        Attila Kovacs
    """

    build_type = arguments.build_type

    bump_version_number()
    create_constants_file()
    create_wheel()

def mde_release(arguments: 'argparse.Namespace') -> MDEReturnCodes:

    """
    Creates a new release for the framework.

    Args:
        arguments (argparse.Namespace): The parsed command line arguments.

    Returns:
        MDEReturnCodes: One of the supported MDE return codes.

    Authors:
        Attila Kovacs
    """

    pass