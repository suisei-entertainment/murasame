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
Contains the implementation for the example daemon application.
"""

from murasame.utils import CliProcessor
from murasame.application import Application, BusinessLogic

# CLI commands supported by the application
CLI_COMMANDS = \
[

]

CLI_DESCRIPTION_STRING = ''

CLI_USAGE_STRING = ''

CLI_EPILOGUE_STRING = ''

def process_cli() -> 'argparse.Namespace':

    return  None

if __name__ == '__main__':

    cli = CliProcessor(command_map=CLI_COMMANDS,
                       description_string=CLI_DESCRIPTION_STRING,
                       usage_string=CLI_USAGE_STRING,
                       epilog_string=CLI_EPILOGUE_STRING)
    
    cli.process(cb_argument_processor=process_cli())