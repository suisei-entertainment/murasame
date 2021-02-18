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

WORKSPACE_DIRECTORY="${HOME}/.murasame"

# Create workspace directories
mkdir -p -m 777 "${WORKSPACE_DIRECTORY}"
mkdir -p -m 777 "${WORKSPACE_DIRECTORY}/build"
mkdir -p -m 777 "${WORKSPACE_DIRECTORY}/dist"
mkdir -p -m 777 "${WORKSPACE_DIRECTORY}/testfiles"
mkdir -p -m 777 "${WORKSPACE_DIRECTORY}/logs"
mkdir -p -m 777 "${WORKSPACE_DIRECTORY}/logs/unittest"
