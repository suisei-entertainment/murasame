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
Contains utility functions used for handling command line arguments.
"""

# Runtime Imports
import argparse

# MDE Imports
from mde.constants import MDE_DESCRIPTION, MDE_EPILOG

def configure_arguments() -> argparse.ArgumentParser:

    """
    Configure the argument parser with the supported command line arguments.

    Returns:
        argparse.ArgumentParser: The configured argument parser to be used for
            parsing command line arguments.

    Authors:
        Attila Kovacs
    """

    # Create the parser
    parser = argparse.ArgumentParser(
        description=MDE_DESCRIPTION,
        epilog=MDE_EPILOG)

    # Add supported arguments
    parser.add_argument(
        '--release',
        dest='release',
        default=False,
        action='store_true',
        help='Generates a new release.')

    parser.add_argument(
        '--build',
        dest='build_type',
        default=None,
        action='store',
        help='The type of build to generate.')

    parser.add_argument(
        '--debug',
        dest='debug_mode',
        default=False,
        action='store_true',
        help='Enable debug mode of MDE.')

    parser.add_argument(
        '--github-token',
        dest='github_token',
        default=None,
        action='store',
        help='The GitHub access token to use when interacting with GitHub.')

    parser.add_argument(
        '--draft',
        dest='release_draft',
        default=False,
        action='store_true',
        help='Whether or not the release should be marked as a draft.')

    return parser

def parse_command_line() -> argparse.Namespace:

    """Parses the command line arguments and returns an argparse namespace.

    Returns:
        argparse.Namespace: The argparse Namespace object containing all
            command line arguments found.

    Authors:
        Attila Kovacs
    """

    parser = configure_arguments()
    return parser.parse_args()
