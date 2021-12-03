# Copyright 2021 Research Institute of Systems Planning, Inc.
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

from typing import List, Optional

from caret_analyze.infra.interface import RecordsProvider

from ..record.record import RecordsInterface
from .path_base import PathBase
from .publisher import Publisher
from .subscription import Subscription
from .callback import CallbackBase
from ..value_objects import MessageContext, NodePathStructValue
from ..common import CustomDict


class NodePath(PathBase):
    def __init__(
        self,
        node_path_value: NodePathStructValue,
        records_provider: RecordsProvider,
        subscription: Optional[Subscription],
        publisher: Optional[Publisher],
        callbacks: Optional[List[CallbackBase]]
    ) -> None:
        super().__init__()
        self._val = node_path_value
        self._provider = records_provider
        self._pub = publisher
        self._sub = subscription
        self._callbacks = callbacks

    @property
    def node_name(self) -> str:
        return self._val.node_name

    @property
    def callbacks(self) -> Optional[List[CallbackBase]]:
        return self._callbacks

    @property
    def message_context(self) -> Optional[MessageContext]:
        return self._val.message_context

    @property
    def summary(self) -> CustomDict:
        return self._val.summary

    def _to_records_core(self) -> RecordsInterface:
        records = self._provider.node_records(self._val)
        if len(records.columns) > 0:
            records.sort(records.columns[0])
        return records

    @property
    def publisher(self) -> Optional[Publisher]:
        return self._pub

    @property
    def publish_topic_name(self) -> Optional[str]:
        return self._val.publish_topic_name

    @property
    def subscription(self) -> Optional[Subscription]:
        return self._sub

    @property
    def subscribe_topic_name(self) -> Optional[str]:
        return self._val.subscribe_topic_name
