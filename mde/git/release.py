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
import subprocess

# Dependency Imports
import github

# MDE Imports
from mde.constants import MDE_LOGGER_NAME, REPOSITORY_NAME, DIST_PATH
from mde.utils.version import get_version_string, get_version_num, bump_version_number
from mde.git.commit import get_git_commit_hash
from mde.utils.snapshot import create_snapshot
from mde.utils.constantsfile import create_constants_file
from mde.packaging.wheel import create_wheel
from mde.documentation.documentation import build_documentation, package_documentation

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
    release_message = tag_message

    draft = False
    if arguments.release_draft:
        draft = True
        logger.debug('    Marking the release as draft.')

    # Merge the current development branch to the release branch
    checkout_command = ['git', 'checkout', 'release']
    merge_command = ['git', 'merge', 'development']

    try:
        subprocess.check_call(checkout_command)
    except subprocess.CalledProcessError as error:
        logger.error('Failed to checkout the release branch.')
        raise SystemExit from error

    try:
        subprocess.check_call(merge_command)
    except subprocess.CalledProcessError as error:
        logger.error('Failed to merge the development branch into the release '
                     'branch.')
        raise SystemExit from error

    # Create the release tag
    tag_command = ['git', 'tag', '-a', 'f{tag}', '-m', 'f{tag_message}']

    try:
        subprocess.check_call(tag_command)
    except subprocess.CalledProcessError as error:
        logger.error('Failed to tag the release branch with the new release '
                     'tag.')
        raise SystemExit from error

    # Update GitHub
    push_command = ['git', 'push']

    try:
        subprocess.check_call(push_command)
    except subprocess.CalledProcessError as error:
        logger.error('Failed to push the release changes to the repository.')
        raise SystemExit from error

    # Get the current HEAD as a GitHub commit object
    commit_hash = get_git_commit_hash()
    commit = repository.get_commit(sha=commit_hash)

    if not commit_hash:
        logger.error(f'Failed to retrieve commit {commit_hash} from GitHub.')

    # Force a release build even if it wasn't specified
    arguments.build_type = 'release'

    # Create the Python wheel
    bump_version_number()
    create_constants_file()
    create_wheel(arguments=arguments)

    # Create a snapshot of the source code
    tar_path = create_snapshot()
    if not tar_path:
        logger.error(
            'Cannot create release without a valid repository snapshot.')
        raise SystemExit

    logger.debug(f'Creating git release {release_name} for object {obj}...')

    # Create documentation
    build_documentation()
    documentation_archive_path = package_documentation()
    if not documentation_archive_path:
        logger.error('Cannot create release without a valid documentation '
                     'package.')
        raise SystemExit

    # Create the  the release on GitHub
    release = repository.create_git_release(
        tag=tag,
        name=release_name,
        message=release_message,
        draft=draft,
        prerelease=False,
        target_commitish=commit)

    # Upload the Python wheel as a release asset
    logger.debug(f'Uploading Python wheel as release asset for {tag}...')
    wheel_path = os.path.abspath(os.path.expanduser(
        f'{DIST_PATH}/murasame-{get_version_num()}-py3-none-any.whl'))
    release.upload_asset(path=wheel_path)
    logger.debug('Python wheel uploaded.')

    # Upload the repository snapshot as a release asset.
    logger.debug(f'Uploading repository snapshot as release asset for {tag}...')
    release.upload_asset(path=tar_path)
    logger.debug('Snapshot uploaded.')

    # Upload the documentation as a release asset.
    logger.debug(f'Uploading documentation as release asset for {tag}...')
    release.upload_asset(path=documentation_archive_path)
    logger.debug('Documentation uploaded.')

    # Go back to the development branch
    checkout_command = ['git', 'checkout', 'development']
    try:
        subprocess.check_call(checkout_command)
    except subprocess.CalledProcessError:
        logger.error('Failed to switch back to the development branch.')

    logger.debug('GitHub release created successfully.')