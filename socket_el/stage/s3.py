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
import json
import os
from time import sleep
from typing import Dict, List

import boto3 as boto3
import pandas as pd

from socket_el.stage.local_fs_stage import LocalFS
from socket_el.stage.stage import Stage


class S3(Stage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_files = set()
        self._cached_files = set()
        self._access_key=kwargs.pop('access_key')
        self._secret_key=kwargs.pop('secret_key')
        self._bucket=kwargs.pop('bucket')
        self._put_offset = 0
        self._file_name_base = kwargs.get('file_name_base')
        self._client=self.s3_client()

    def s3_client(self):

        return boto3.resource(
            's3',
            region_name='us-east-1',
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key
        ).Bucket(self._bucket)

    def get(self) -> pd.DataFrame:

        if len(self._current_files) > 0:
            file = self._current_files.pop()
        else:
            self._get_files()
            file = self._current_files.pop()

        df = pd.read_json(file.get()["Body"], lines=True)

        self._cached_files.add(file)

        file.delete()

        return df

    def _get_files(self) -> List:
        """
        List of files that haven't been processed yet.

        Returns: list of file

        """

        self._current_files = set(list(self._client.objects.all()))

        unique_files = set(self._current_files) - set(self._cached_files)

        if len(unique_files) == 0:
            sleep(5)
            unique_files = self._get_files()

        return unique_files


    def put(self, data: Dict, *kwargs) -> None:
        filename='_'.join([self._file_name_base, str(self._put_offset)])+'.json'
        self._client.Object(key=filename).put(Body=json.dumps(data))
        self._put_offset += 1


