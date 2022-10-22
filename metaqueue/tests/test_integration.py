"""
TestIntegration
---------------
Integration Tests testing different domains of the the library,
e.g. testing whether the MetadataEngine works correctly together
with the MetaQueue and whether the tasks can be run concurrently
"""

import pytest
import enum

from metaqueue.queue import Metadata
from metaqueue.engine.meta import MetadataEngine, MetaQueue
from metaqueue.instruments.concurrent import TaskRunner
from metaqueue.utilities.tools import repeat


class TestIntegration:
    @pytest.mark.asyncio
    async def test_basic_usage_of_engine(self):
        class Topics(enum.Enum):
            task1 = enum.auto()
            task2 = enum.auto()
            task3 = enum.auto()

        async def task1(value: int, metadataengine: MetadataEngine):
            metadataengine.publish_to_topic(Metadata(data = value, name = "task1_value", location = "Tmp1", context = "test"))
            return value ** 2

        async def task2(value: str, metadataengine: MetadataEngine):
            metadataengine.publish_to_topic(Metadata(data = value, name = "task2_value", location = "Tmp2", context = "test"))
            return f"{value}"

        async def task3(value: float, metadataengine: MetadataEngine):
            metadataengine.publish_to_topic(Metadata(data = value, name = "task3_value", location = "Tmp3", context = "test"))
            return 2.0 * value

        task1_queue  = MetaQueue(buffer_size = 3, dtype = int)
        task1_engine = MetadataEngine(topic = Topics.task1, queue = task1_queue)
        task2_queue  = MetaQueue(buffer_size = 3, dtype = str)
        task2_engine = MetadataEngine(topic = Topics.task2, queue = task2_queue)
        task3_queue  = MetaQueue(buffer_size = 3, dtype = float)
        task3_engine = MetadataEngine(topic = Topics.task3, queue = task3_queue)

        task1_args = [(1, task1_engine), (2, task1_engine), (3, task1_engine)]
        task2_args = [("tmp", task2_engine), ("str", task2_engine), ("something", task2_engine)]
        task3_args = [(2.0, task3_engine), (1.0, task3_engine), (4.5, task3_engine)]

        await TaskRunner.run(async_funcs = [*repeat(task1, 3), *repeat(task2, 3), *repeat(task3, 3)], 
                             args = [*task1_args, *task2_args, *task3_args])
        
        metadataengines = [task1_engine, task2_engine, task3_engine]
        inactive  = 0
        metadates = []
        while True:
            if inactive == len(metadataengines):
                break

            for mdengine in metadataengines:
                if mdengine.get_queue_capacity() > 0:
                    metadata = mdengine.retrieve_data_from_queue()
                    metadates.append(metadata)
                    continue
                inactive += 1

        assert metadates[0]  == Metadata(data = 1, name = 'task1_value', location = 'Tmp1', context = "test")
        assert metadates[1]  == Metadata(data = 'tmp', name = 'task2_value', location = 'Tmp2', context = "test")
        assert metadates[-1] == Metadata(data = 4.5, name = 'task3_value', location = 'Tmp3', context = "test")