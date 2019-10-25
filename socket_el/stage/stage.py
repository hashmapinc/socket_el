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
from typing import Dict

import pandas as pd
import logging


class Stage:
    """
    Base class for Stage objects
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self, **kwargs):
        pass

    def put(self, data: Dict, **kwargs) -> None:
        """
        Should at minimum take a 'dict' of objects (dataset rows...) and write to a staging location

        Args:
            data: dict of data objects
            **kwargs: optional arguments

        Returns:

        """
        raise NotImplementedError('Base class method - please implement')

    def get(self) -> pd.DataFrame:
        """
        Will look at stage and extract the
        Returns:

        """
        raise NotImplementedError('Base class method - please implement')
