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
Contains utility functions related to GitHub releases.
"""

# Runtime Imports
import os
import logging

# Dependency Imports
import github

# MDE Imports
from mde.constants import MDE_LOGGER_NAME, REPOSITORY_NAME, DIST_PATH
from mde.utils.version import get_version_string, get_version_num
from mde.git.commit import get_git_commit_hash

def do_github_release(arguments: 'argparse.Namespace') -> None:

    """Creates a new release on GitHub.

    Args:
        arguments (argparse.Namespace): The parsed command line arguments.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger(MDE_LOGGER_NAME)
    logger.debug('Creating release on GitHub...')

    # Get a GitHub access token to use. This is either specified through the
    # command line, or stored in the environment variable GITHUB_ACCESS_TOKEN
    # on the host system.
    access_token = arguments.github_token

    if access_token is None:
        logger.debug('      GitHub access token not specified through the '
                     'command line, attempting to retrieve from the '
                     'environment.')
        try:
            access_token = os.environ['GITHUB_ACCESS_TOKEN']
        except KeyError:
            logger.error('      No GitHub access token could be retrieved from '
                        'the environment')
            raise SystemExit

    # Access GitHub and retrieve the repository
    git = github.Github(access_token)
    repository = git.get_repo(REPOSITORY_NAME)

    if not repository:
        logger.error(f'    Failed to retrieve repository {REPOSITORY_NAME}.')
        raise SystemExit

    # Configure release parameters
    tag = get_version_string()
    tag_message = f'Murasame release version {get_version_string()} created '\
                  'by MDE.'
    release_name = get_version_string()
    obj = get_git_commit_hash()
    release_type = 'commit'
    release_message = tag_message

    draft = False
    if arguments.release_draft:
        draft = True
        logger.debug('    Marking the release as draft.')

    prerelease = False
    if arguments.release_prerelease:
        prerelease = True
        logger.debug('    Marking the release as pre-release.')

    logger.debug(f'Creating git release {release_name} for object {obj}...')

    # Create the release tag and the release on GitHub
    release = repository.create_git_tag_and_release(
        tag=tag,
        tag_message=tag_message,
        release_name=release_name,
        release_message=release_message,
        object=obj,
        type=release_type,
        draft=draft,
        prerelease=prerelease
    )

    # Upload the Python wheel as a release asset
    wheel_path = os.path.abspath(os.path.expanduser(
        f'{DIST_PATH}/murasame-{get_version_num()}-py3-none-any.whl'))
    release.upload_asset(path=wheel_path)

    logger.debug('GitHub release created successfully.')