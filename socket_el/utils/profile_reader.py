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

import pathlib
import posixpath
from typing import Dict

from socket_el.utils.config_reader import ConfigReader


class ProfileReader(ConfigReader):
    """
    Read users profiles to create a ConfigReader
    """

    _config_file = str(posixpath.join(str(pathlib.Path.home()), '.socket_streamer/profile.yml'))

    @classmethod
    def parse_config(cls, profile, **kwargs) -> Dict:
        """

        Args:
            profile: name of profile
            **kwargs: optional arguments

        Returns: parsed configuration

        """

        return super().parse_config()[profile]
