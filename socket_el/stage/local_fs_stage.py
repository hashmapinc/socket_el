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

import posixpath
from time import sleep
from typing import Dict, List

import pandas as pd
import logging
import os

from socket_el.stage.stage import Stage


class LocalFS(Stage):
    """
        Stage class that uses a local file system - relative to where the code was executed.

        Class is constructed given a desired directory (as path), and a file_name_base to use as the
        root of all filenames.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self._current_files = set()
        self._cached_files = set()
        self._target_path = posixpath.join(os.getcwd(), kwargs.get('path'))
        if os.path.exists(self._target_path):
            self._create_path()
        self._put_offset = 0
        self._file_name_base = kwargs.get('file_name_base')

    def _create_path(self) -> None:
        """
        Creates the path directory when needed.
        """

        if not os.path.exists(self._target_path):
            try:
                os.mkdir(self._target_path)
            except Exception as _:
                pass  # Intentional since another thread may have done this.

    def get(self) -> pd.DataFrame:
        """
        Returns a pandas dataframe from the staging location

        Returns: a new dataframe

        """

        self._create_path()

        if len(self._current_files) > 0:
            file = self._current_files.pop()
        else:
            self._get_files()
            file = self._current_files.pop()

        full_file = os.path.join(self._target_path, file)
        df = pd.read_json(full_file, lines=True)

        self._cached_files.add(file)

        os.remove(full_file)

        return df

    def _get_files(self) -> List:
        """
        List of files that haven't been processed yet.

        Returns: list of file

        """

        self._current_files = set(os.listdir(self._target_path))

        unique_files = set(self._current_files) - set(self._cached_files)

        if len(unique_files) == 0:
            sleep(5)
            unique_files = self._get_files()

        return unique_files

    def put(self, data: Dict, **kwargs) -> None:
        """
        Writes data to a stage location as a json file
        Args:
            data: json entries
            **kwargs: unused here
        """
        self.logger.info('Writing data to staging location with offset {}'.format(self._put_offset))

        self._create_path()
        print(data)
        with open(posixpath.join(self._target_path,
                                 '_'.join([self._file_name_base, str(self._put_offset)]) + '.json'), 'w') as stream:
            stream.writelines(data)
        self._put_offset += 1
