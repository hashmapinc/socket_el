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

import asyncio

from socket_el.producers.producer import Producer
from socket_el.stage.stage_factory import StageFactory
from socket_el.utils.pandas_writer import PandasWriter
from socket_el.utils.profile_reader import ProfileReader


class Postgres(Producer):
    """
    Postgres producer: writes staged data to a postgres database
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._stage_configs = self._config['stages']

        db_config = ProfileReader.parse_config(self._config['profile'])
        self._connection_string = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
            user=db_config['user'],
            host=db_config['host'],
            port=db_config['port'],
            password=db_config['password'],
            database=db_config['database']
        )

        self._schema = db_config['schema']

    @property
    def connection_string(self) -> str:
        return self._connection_string

    def run(self) -> None:
        """
        Asynchronously execute the producer.
        """

        self.logger.info('Starting Postgres logger.')

        # Create list of writers
        writers = [PandasWriter(connection_string=self.connection_string,
                                schema=self._schema,
                                table=stage['name'],
                                stage=StageFactory.get(**stage['stage_config'])).run() for stage in self._stage_configs]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(
                *writers
            )
        )
