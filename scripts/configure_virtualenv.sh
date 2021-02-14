#!/bin/bash

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

#shellcheck disable=SC1090

VIRTUALENV_DIRECTORY="${HOME}/.murasame/.env"

echo "[MURASAME.SETUP] > Installing required packages inside the virtual environment..."
source "${VIRTUALENV_DIRECTORY}/bin/activate"
pip install -r requirements-dev.txt
pip install -r requirements.txt
echo "[MURASAME.SETUP] > Requirements installed."
