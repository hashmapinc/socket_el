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

import threading
import logging
import traceback
from typing import List

from socket_el.consumers.consumers_factory import ConsumersFactory
from socket_el.producers.producers_factory import ProducersFactory


def get_consumers() -> List:
    return ConsumersFactory.get()


def get_producers() -> List:
    return ProducersFactory.get()


logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:

    logger.info('Creating threads.')
    consumer_threads = [threading.Thread(target=consumer.run) for consumer in get_consumers()]
    producer_threads = [threading.Thread(target=producer.run) for producer in get_producers()]
    logger.info('Threads created.')

    logger.info('Starting threads.')
    [thread.start() for thread in consumer_threads]
    [thread.start() for thread in producer_threads]
    logger.info('Threads started.')

except Exception as e:
    print(traceback.format_exc())
    logger.info('Exception has occurred and ingestion pipeline has terminated.')
