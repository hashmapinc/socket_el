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

import logging
from _ast import List

from socket_el.consumers.consumer import Consumer
from socket_el.consumers.socket import Socket
from socket_el.utils.config_reader import ConfigReader


class ConsumersFactory:
    """
    Factory method to create Consumers
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @classmethod
    def get(cls) -> list:
        """
        Given configuration will return a configured Consumers of the appropriate types.
        Returns: configured consumers list

        """

        config = ConfigReader.parse_config()
        consumer_info = [(runner['variety'], runner) for runner in config['runners'] if runner['type'] == 'consumer']

        consumers = list()
        for consumer in consumer_info:
            if consumer[0].lower() == 'socket':
                cls.logger.info('Creating a Socket Consumer')
                consumers.append(Socket(**consumer[1]))

            else:
                cls.logger.error('No Consumer of type matching {}'.format(consumer_info[0]))

        return consumers
