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

The library has five main components: 
1. Consumer
    * Components of this kind are to be used to ingest (extract) data from a source and store to a Stage
1. Producer
    * Components of this kind are to be used to egest (load) data from a Stage into a source location
1. Stage
    * Stage components contain the logic to write out and read into a pandas dataframe data as the intermediate transport cache.
1. utils
    * This module contains code that helps with other operations.
1. engine
    * This is the piece of code used to execute the pipeline.

## API
The API of this project has been intentionally kept to a minimum. The interface of each of the module base classes will be discussed in greater detail below.

### Consumer

```python
class Consumer:
    def __init__(self, **kwargs)
    def run(self) -> None
    def flush(self) -> None
```

The constructor 'init' method takes a variable number of arguments. All arguments that are to be passed into here should be available within the configuration file. Implementations should reference the values from the configuration file.
 
The 'run' method is will execute the source to stage pipeline. The current examples in this project execute asynchronous processes.

The 'flush' method pushes the data into the stage

### Producer

```python
class Producer:
    def __init__(self, **kwargs)
    def run(self) -> None
```

The constructor 'init' method takes a variable number of arguments. All arguments that are to be passed into here should be available within the configuration file. Implementations should reference the values from the configuration file.

The 'run' method will execute the stage to sink pipeline. The current examples in the project execute asynchronous processes.

### Stage

```python
class Stage:
    def __init__(self, **kwargs)
    def put(self, data: Dict, **kwargs) -> None
    def get(self) -> pd.DataFrame
```

The constructor 'init' method takes a variable number of arguments. All arguments that are to be passed into here should be available within the configuration file. Implementations should reference the values from the configuration file. Each Consumer will have the stage configuration.

The 'put' method takes a field called data, which must be a dict (or comparable) that contains the data being written to the stage. It may also take additional arguments that must be provided on a per implementation need and read from the kwargs.

### engine - running the code

This code is generic and should work in most situations.

### config.yml

The following is a sample configuration file
```yaml
runners:
  - name: websocket_1
    variety: socket
    type: consumer
    uri: wss://ws.coincap.io/trades/binance
    stage:
      type: local
      path: 'tmp'
    batch_configuration:
      size: 100

  - name: websocket_2
    variety: socket
    type: consumer
    uri: wss://ws.coincap.io/trades/huobi
    stage:
      type: local
      path: 'tmp'
    batch_configuration:
      size: 100

  - name: postgres
    variety: postgres
    depends_on:
      - websocket_1
      - websocket_2
    type: producer
    profile: postgres
```

The main part of the configuration is a 'runners' grouping. Within this are all the producers and consumers. The configuration should be pretty clean-cut, however lets discuss the configuration of a consumer and a producer.

A consumer has the following:
* name - unique identifier for that specific consumer
* variety - is the name of the class that is to be created. Used within the factory method
* type = consumer
* uri - this is specific to the socket consumer and is the URI for the websocket connection
* stage - configuration for the stage to that will be used
* batch_configuration - describes how batching is executed

A producer has the following:
* name - unique identifier for the 
* variety - name of class that this producer will have
* depends_on - list of consumers (by name) that the producer is responsible for processing stages of.
* type = producer
* profile - reference to the profile that is stored in the profile.yaml

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

## Future Direction

It is envisioned that this code will eventually be turned into a python package. What functionality that is to be supported remains to be seen.