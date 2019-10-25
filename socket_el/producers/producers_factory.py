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

from typing import List
import logging

from socket_el.producers.postgres import Postgres
from socket_el.producers.producer import Producer
from socket_el.utils.config_reader import ConfigReader


class ProducersFactory:
    """
    Factory method for create Producer objects.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @classmethod
    def get(cls) -> list:
        """
        Return a Producer given the producers configuration and the configuration of all of its dependents
        Returns: Configured Producer object
        """

        config = ConfigReader.parse_config()
        producer_infos = [(runner['variety'], runner) for runner in config['runners'] if runner['type'] == 'producer']

        producers = list()

        for producer in producer_infos:
            # Link the producer to the consumers that it depends on.
            producer[1]['stages'] = cls._get_depends_on(producer=producer[1], configuration=config)

            if producer[0].lower() == 'postgres':
                logging.info('Creating a postgres producer')
                producers.append(Postgres(**producer[1]))

            else:
                cls.logger.info("")

        return producers

    @classmethod
    def _get_depends_on(cls, producer: dict, configuration: dict) -> List[dict]:
        """
        Construct the list of stages tha the producer is dependent on

        Args:
            producer: configuration of a producer
            configuration: overall configuration

        Returns: List of stages the producer is dependent on

        """

        logging.info('Linking stages from the dependency linked consumers to the producer.')
        consumers = [runner for runner in configuration['runners'] if runner['type'] == 'consumer']

        admissable_consumers = [consumer for consumer in consumers if consumer['name'] in producer['depends_on']]

        stages = [
            {
                'name': consumer['name'],
                'stage_config': consumer['stage'],
            }
            for consumer in admissable_consumers
        ]

        return stages
