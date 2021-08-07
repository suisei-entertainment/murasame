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
Contains the default configuration of the log system.
"""

DEFAULT_LOG_CONFIG = \
{
    "rootpath": '~/.murasame/logs',
    "channels":
    [
        {
            "name": "murasame.application",
            "defaultloglevel": "INFO",
            "targets":
            [
                {
                    'type': 'console',
                    'coloredlogs': 'true',
                },
                {
                    'type': 'file',
                    'filename': 'murasame.application.log'
                }
            ]
        },
        {
            "name": "murasame.configuration",
            "defaultloglevel": "INFO",
            "targets":
            [
                {
                    'type': 'console',
                    'coloredlogs': 'true',
                },
                {
                    'type': 'file',
                    'filename': 'murasame.configuration.log'
                }
            ]
        },
        {
            "name": "murasame.exceptions",
            "defaultloglevel": "INFO",
            "targets":
            [
                {
                    'type': 'console',
                    'coloredlogs': 'true',
                },
                {
                    'type': 'file',
                    'filename': 'murasame.exceptions.log'
                }
            ]
        },
        {
            "name": "murasame.localizer",
            "defaultloglevel": "INFO",
            "targets":
            [
                {
                    'type': 'console',
                    'coloredlogs': 'true',
                },
                {
                    'type': 'file',
                    'filename': 'murasame.localizer.log'
                }
            ]
        },
        {
            "name": "murasame.pal",
            "defaultloglevel": "INFO",
            "targets":
            [
                {
                    'type': 'console',
                    'coloredlogs': 'true',
                },
                {
                    'type': 'file',
                    'filename': 'murasame.pal.log'
                }
            ]
        },
        {
            "name": "murasame.pal.networking.socket",
            "defaultloglevel": "INFO",
            "targets":
            [
                {
                    'type': 'console',
                    'coloredlogs': 'true',
                },
                {
                    'type': 'file',
                    'filename': 'murasame.pal.networking.socket.log'
                }
            ]
        },
        {
            "name": "murasame.pal.vfs",
            "defaultloglevel": "INFO",
            "targets":
            [
                {
                    'type': 'console',
                    'coloredlogs': 'true',
                },
                {
                    'type': 'file',
                    'filename': 'murasame.pal.vfs.log'
                }
            ]
        },
        {
            "name": "murasame.utils",
            "defaultloglevel": "INFO",
            "targets":
            [
                {
                    'type': 'console',
                    'coloredlogs': 'true',
                },
                {
                    'type': 'file',
                    'filename': 'murasame.utils.log'
                }
            ]
        }
    ]
}
