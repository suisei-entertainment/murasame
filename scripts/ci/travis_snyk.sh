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

. ./before.sh

# Install Snyk
npm install -g snyk

# Run Snyk both for development and production dependencies
snyk monitor --project-name=murasame --org=suisei-entertainment --file=./requirements.txt --package-manager=pip
snyk test --project-name=murasame --org=suisei-entertainment --file=./requirements.txt --package-manager=pip

snyk monitor --project-name=murasame-dev --org=suisei-entertainment --file=./requirements-dev.txt --package-manager=pip
snyk test --project-name=murasame-dev --org=suisei-entertainment --file=./requirements-dev.txt --package-manager=pip
