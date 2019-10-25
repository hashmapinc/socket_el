<!---
# Modifications © 2019 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
-->

# socket_el

This is a basic, threaded & asynchronous EL engine. Its purpose is to ingest data by polling a data source, store the data in a staging location (flat files, parquet, etc...) in one process, and then in another process ingest the data from the stage location and push it to the targeted sink location.

## About



## API


### Consumer


### Producer


### Stage


### utils


### engine - running the code


### profile.yml


### config.yml


## Setting Up Project

The following section will cover how to setup and use this project.

### database profiles
this project uses local credential management in a 'hidden' subdirectory in the users root directory. You will need to create it with the following command
```bash
mkdir .socket_el
``` 
Within this directory you should have a profile.yml file that has entries as such:
```yaml
postgres:
  user: postgres
  password: password
  database: test
  host: 127.0.0.1
  port: 5432
  schema: test
```
It is likely that you could end up with many of these such files. They can be referenced from within a configuration by the key (postgres above) for the entry in the profile.yml file.

### pipenv
pipenv is used as the virtual environment tool of choice for this project. Please read the appropriate documentation on setting pipenv up and using it within your project. I would recommend using pycharm as it integrates very well with pipenv.

Once pipenv is installed, you can open to this project root and type
```bash
pipenv install
```
and the dependencies will be installed.

### docker

Docker will be useful if you are hosting a local database server to test from and don't wish to have a permanent install on your machine.
 
Follow the best recommendations to install docker for your working environment. 
