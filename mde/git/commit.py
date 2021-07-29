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
Contains utility functions for handling Git commits.
"""

# Runtime Imports
import subprocess

def get_git_commit_hash() -> str:

    """Returns the commit hash of the current HEAD of the repository.

    Authors:
        Attila Kovacs
    """

    scm_id = None

    try:
        scm_id = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']).strip().decode('ascii')
    except subprocess.CalledProcessError:
        scm_id = None

    return scm_id