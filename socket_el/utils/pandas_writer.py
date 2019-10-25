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
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from socket_el.stage.stage import Stage


class PandasWriter:
    """
    Will recursively find all latest files and read + write them out to the
    specified persistent layer.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self,
                 connection_string: str,
                 table: str,
                 schema: str,
                 stage: Stage) -> None:

        self._connection_string = connection_string
        self._schema = schema
        self._stage = stage
        self._table = table
        self._stage = stage

        self._cached_files = set()

        self._engine = None

    @property
    def engine(self) -> Engine:

        if not self._engine:
            self._engine = create_engine(self._connection_string)

        return self._engine

    def run(self) -> None:
        """
        Write the files from stage to the specified location using pandas
        """

        while True:
            self.logger.info('Writing data to postgres.')
            self._stage.get().to_sql(self._table,
                                     self.engine,
                                     schema=self._schema,
                                     if_exists='append',
                                     index=False)
