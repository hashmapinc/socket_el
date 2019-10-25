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

from socket_el.stage.local_fs_stage import LocalFS
from socket_el.stage.s3 import S3
from socket_el.stage.stage import Stage


class StageFactory:
    """
    Factory to create Stage child classes
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @classmethod
    def get(cls, **kwargs) -> Stage:
        """
        Takes a type and stage descriptor configuration and returns a Stage of the appropriate type

        Returns: Stage object

        Raises:
            ValueError when stage 'type' is unknown

        """

        stage_type = kwargs.get('type')
        if stage_type.lower() == 'local':
            cls.logger.info('Creating LocalFS Stage.')
            return LocalFS(**kwargs)
        elif stage_type.lower() == 's3':
            cls.logger.info('Creating S3 Stage.')
            return S3(**kwargs)
        else:
            error_message ='{stage_type} is not known'.format(stage_type=stage_type)
            cls.logger.error(error_message)
            raise ValueError(error_message)
