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


from caret_analyze.architecture import Architecture
from caret_analyze.architecture.architecture_loaded import ArchitectureLoaded
from caret_analyze.architecture.architecture_reader_factory import \
    ArchitectureReaderFactory
from caret_analyze.architecture.graph_search import NodePathSearcher
from caret_analyze.architecture.reader_interface import ArchitectureReader
from caret_analyze.exceptions import InvalidArgumentError, ItemNotFoundError
from caret_analyze.value_objects import (CommunicationStructValue,
                                         ExecutorStructValue, NodeStructValue,
                                         NodePathStructValue, PathStructValue)

import pytest


class TestArchiteture:

    def test_empty_architecture(self, mocker):
        reader_mock = mocker.Mock(spec=ArchitectureReader)
        loaded_mock = mocker.Mock(spec=ArchitectureLoaded)

        mocker.patch.object(loaded_mock, 'nodes', [])
        mocker.patch.object(loaded_mock, 'paths', [])
        mocker.patch.object(loaded_mock, 'communications', [])
        mocker.patch.object(loaded_mock, 'executors', [])

        mocker.patch('caret_analyze.architecture.architecture_loaded.ArchitectureLoaded',
                     return_value=loaded_mock)

        reader_mock = mocker.Mock(spec=ArchitectureReader)
        mocker.patch.object(ArchitectureReaderFactory,
                            'create_instance', return_value=reader_mock)

        loaded_mock = mocker.Mock(spec=ArchitectureLoaded)
        mocker.patch('caret_analyze.architecture.architecture_loaded.ArchitectureLoaded',
                     return_value=loaded_mock)

        mocker.patch.object(loaded_mock, 'nodes', [])
        mocker.patch.object(loaded_mock, 'communications', [])
        mocker.patch.object(loaded_mock, 'executors', [])
        mocker.patch.object(loaded_mock, 'paths', [])
        arch = Architecture('file_type', 'file_path')

        assert len(arch.nodes) == 0
        assert len(arch.executors) == 0
        assert len(arch.paths) == 0
        assert len(arch.communications) == 0

    def test_get_node(self, mocker):
        reader_mock = mocker.Mock(spec=ArchitectureReader)
        mocker.patch.object(ArchitectureReaderFactory,
                            'create_instance', return_value=reader_mock)

        loaded_mock = mocker.Mock(spec=ArchitectureLoaded)
        mocker.patch('caret_analyze.architecture.architecture_loaded.ArchitectureLoaded',
                     return_value=loaded_mock)

        node_mock = mocker.Mock(spec=NodeStructValue)
        mocker.patch.object(node_mock, 'node_name', 'node_name')

        mocker.patch.object(loaded_mock, 'paths', ())
        mocker.patch.object(loaded_mock, 'nodes', (node_mock,))
        mocker.patch.object(loaded_mock, 'communications', ())

        searcher_mock = mocker.Mock(spec=NodePathSearcher)
        mocker.patch('caret_analyze.architecture.graph_search.NodePathSearcher',
                     return_value=searcher_mock)

        arch = Architecture('file_type', 'file_path')
        node = arch.get_node('node_name')
        assert node == node_mock

        with pytest.raises(ItemNotFoundError):
            arch.get_node('node_not_exist')

    def test_full_architecture(self, mocker):
        reader_mock = mocker.Mock(spec=ArchitectureReader)
        loaded_mock = mocker.Mock(spec=ArchitectureLoaded)

        node_mock = mocker.Mock(spec=NodeStructValue)
        executor_mock = mocker.Mock(spec=ExecutorStructValue)
        path_mock = mocker.Mock(spec=PathStructValue)
        comm_mock = mocker.Mock(spec=CommunicationStructValue)

        mocker.patch.object(loaded_mock, 'nodes', [node_mock])
        mocker.patch.object(loaded_mock, 'paths', [path_mock])
        mocker.patch.object(loaded_mock, 'communications', [comm_mock])
        mocker.patch.object(loaded_mock, 'executors', [executor_mock])
        mocker.patch.object(path_mock, 'path_name', 'path')

        mocker.patch('caret_analyze.architecture.architecture_loaded.ArchitectureLoaded',
                     return_value=loaded_mock)

        mocker.patch.object(ArchitectureReaderFactory,
                            'create_instance', return_value=reader_mock)

        searcher_mock = mocker.Mock(spec=NodePathSearcher)
        mocker.patch('caret_analyze.architecture.graph_search.NodePathSearcher',
                     return_value=searcher_mock)

        arch = Architecture('file_type', 'file_path')

        assert len(arch.nodes) == 1
        assert arch.nodes[0] == node_mock

        assert len(arch.executors) == 1
        assert arch.executors[0] == executor_mock

        assert len(arch.paths) == 1
        assert arch.paths[0] == path_mock

        assert len(arch.communications) == 1
        assert arch.communications[0] == comm_mock

    def test_path(self, mocker):
        reader_mock = mocker.Mock(spec=ArchitectureReader)
        loaded_mock = mocker.Mock(spec=ArchitectureLoaded)

        path = PathStructValue('path0', ())

        mocker.patch.object(loaded_mock, 'nodes', [])
        mocker.patch.object(loaded_mock, 'paths', [path])
        mocker.patch.object(loaded_mock, 'communications', [])
        mocker.patch.object(loaded_mock, 'executors', [])

        mocker.patch('caret_analyze.architecture.architecture_loaded.ArchitectureLoaded',
                     return_value=loaded_mock)

        mocker.patch.object(ArchitectureReaderFactory,
                            'create_instance', return_value=reader_mock)

        arch = Architecture('file_type', 'file_path')

        # remove
        assert len(arch.paths) == 1
        arch.remove_path('path0')
        assert len(arch.paths) == 0
        with pytest.raises(InvalidArgumentError):
            arch.remove_path('path0')

        # add
        arch.add_path('path1', path)
        assert len(arch.paths) == 1
        with pytest.raises(InvalidArgumentError):
            arch.add_path('path1', path)

        # get
        with pytest.raises(InvalidArgumentError):
            arch.get_path('path0')
        path_ = arch.get_path('path1')

        # update
        arch.update_path('path2', path_)
        arch.get_path('path2')
        with pytest.raises(InvalidArgumentError):
            arch.update_path('path2', path_)

    def test_search_paths(self, mocker):
        reader_mock = mocker.Mock(spec=ArchitectureReader)
        loaded_mock = mocker.Mock(spec=ArchitectureLoaded)

        start_node_mock = mocker.Mock(spec=NodeStructValue)
        end_node_mock = mocker.Mock(spec=NodeStructValue)

        mocker.patch.object(start_node_mock, 'node_name', 'start_node')
        mocker.patch.object(end_node_mock, 'node_name', 'end_node')

        mocker.patch.object(loaded_mock, 'nodes', [start_node_mock, end_node_mock])
        mocker.patch.object(loaded_mock, 'paths', [])
        mocker.patch.object(loaded_mock, 'communications', [])
        mocker.patch.object(loaded_mock, 'executors', [])

        mocker.patch('caret_analyze.architecture.architecture_loaded.ArchitectureLoaded',
                     return_value=loaded_mock)
        mocker.patch.object(ArchitectureReaderFactory,
                            'create_instance', return_value=reader_mock)

        searcher_mock = mocker.Mock(spec=NodePathSearcher)
        mocker.patch('caret_analyze.architecture.graph_search.NodePathSearcher',
                     return_value=searcher_mock)
        path_mock = mocker.Mock(spec=PathStructValue)
        mocker.patch.object(searcher_mock, 'search', return_value=[path_mock])

        arch = Architecture('file_type', 'file_path')

        with pytest.raises(ItemNotFoundError):
            arch.search_paths('not_exist', 'not_exist')

        path = arch.search_paths('start_node', 'end_node')
        assert path == [path_mock]

    def test_search_paths_three_nodes(self, mocker):
        reader_mock = mocker.Mock(spec=ArchitectureReader)
        loaded_mock = mocker.Mock(spec=ArchitectureLoaded)

        node_mock_0 = mocker.Mock(spec=NodeStructValue)
        node_mock_1 = mocker.Mock(spec=NodeStructValue)
        node_mock_2 = mocker.Mock(spec=NodeStructValue)

        mocker.patch.object(node_mock_0, 'node_name', '0')
        mocker.patch.object(node_mock_1, 'node_name', '1')
        mocker.patch.object(node_mock_2, 'node_name', '2')

        node_path_mock_0 = mocker.Mock(spec=NodePathStructValue)
        mocker.patch.object(node_path_mock_0, 'subscribe_topic_name', None)
        mocker.patch.object(node_path_mock_0, 'node_name', '0')
        mocker.patch.object(node_path_mock_0, 'publish_topic_name', '0->1')
        node_path_mock_1 = mocker.Mock(spec=NodePathStructValue)
        mocker.patch.object(node_path_mock_1, 'subscribe_topic_name', '0->1')
        mocker.patch.object(node_path_mock_1, 'node_name', '1')
        mocker.patch.object(node_path_mock_1, 'publish_topic_name', '1->2')
        node_path_mock_2 = mocker.Mock(spec=NodePathStructValue)
        mocker.patch.object(node_path_mock_2, 'subscribe_topic_name', '1->2')
        mocker.patch.object(node_path_mock_2, 'node_name', '2')
        mocker.patch.object(node_path_mock_2, 'publish_topic_name', None)

        mocker.patch.object(node_mock_0, 'paths', [node_path_mock_0])
        mocker.patch.object(node_mock_1, 'paths', [node_path_mock_1])
        mocker.patch.object(node_mock_2, 'paths', [node_path_mock_2])

        comm_mock_0 = mocker.Mock(spec=CommunicationStructValue)
        comm_mock_1 = mocker.Mock(spec=CommunicationStructValue)

        mocker.patch.object(comm_mock_0, 'publish_node_name', '0')
        mocker.patch.object(comm_mock_0, 'subscribe_node_name', '1')
        mocker.patch.object(comm_mock_0, 'topic_name', '0->1')

        mocker.patch.object(comm_mock_1, 'publish_node_name', '1')
        mocker.patch.object(comm_mock_1, 'subscribe_node_name', '2')
        mocker.patch.object(comm_mock_1, 'topic_name', '1->2')

        mocker.patch.object(loaded_mock, 'nodes', [node_mock_0, node_mock_1, node_mock_2])
        mocker.patch.object(loaded_mock, 'paths', [])

        mocker.patch.object(loaded_mock, 'communications', [comm_mock_0, comm_mock_1])
        mocker.patch.object(loaded_mock, 'executors', [])

        mocker.patch('caret_analyze.architecture.architecture_loaded.ArchitectureLoaded',
                     return_value=loaded_mock)
        mocker.patch.object(ArchitectureReaderFactory,
                            'create_instance', return_value=reader_mock)

        arch = Architecture('file_type', 'file_path')

        paths = arch.search_paths('0', '2')
        assert len(paths) == 1

        paths = arch.search_paths('0', '1', '2')
        assert len(paths) == 1
