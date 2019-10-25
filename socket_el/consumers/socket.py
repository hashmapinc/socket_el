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
import websockets

from socket_el.consumers.consumer import Consumer
from socket_el.stage.stage_factory import StageFactory


class Socket(Consumer):

    """
    Consumer class for websockets. Writes the files to a staging location which can be
        local
        (more to come)

    The ingestion is asynchronous and will continue until manually terminated.
    """

    def __init__(self, **kwargs):
        """
        Socket consumer requires fields called
        Args:
            **kwargs:
        """

        super().__init__(**kwargs)
        self._socket_path = self._config['uri']
        self._batch_size = self._config['batch_configuration']['size']

        self._spool = []

        self._stage_config = self._config['stage']
        self._stage_config['file_name_base'] = self._config['uri'].replace('ws://', '')\
            .replace('wss://', '')\
            .replace('/', '_')\
            .replace('.', '_')

        self._stage = StageFactory.get(**self._stage_config)

    @property
    def socket_path(self) -> str:
        """
        Returns: websocket connection uri

        """

        return self._socket_path

    @property
    def batch_size(self) -> int:
        """
        Returns: size of batch at which the connection will flush to stage

        """

        return self._batch_size

    async def get(self) -> None:
        """
        Executes the asynchronous ingestion of data from the socket.
        """

        async with websockets.connect(self.socket_path) as websocket:
            async for message in websocket:
                self.publish(message)

    def publish(self, message: str) -> None:
        """
        Writes message to a spool (queue) and will flush the messages to stage when the spool size has reached capacity.

        Args:
            message: packet of data - assumed to be JSON - from the websocket.

        """

        self._spool.append(message)
        if len(self._spool) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        """
        Execute the flush of messages to stage.
        """

        try:
            self._stage.put(data='\n'.join(self._spool))

        except Exception as _:
            self.logger.info('Error while writing data to the stage')
            raise Exception('Error while writing batched/spooled data to stage location.')

        finally:
            self._spool.clear()

    def run(self) -> None:
        """
        Executes the ingestion process and handles controlled termination
        """

        self.logger.info('Starting Socket consumer.')

        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.get_event_loop().run_until_complete(self.get())
