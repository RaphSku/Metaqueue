"""
TestIntegration
---------------
Integration Tests testing different domains of the the library,
e.g. testing whether the MetadataEngine works correctly together
with the MetaQueue and whether the tasks can be run concurrently
"""

import os
import re
import pytest
import enum
import psycopg2
import datetime

from metaqueue.queue                  import Metadata
from metaqueue.engine.meta            import MetadataEngine, MetaQueue
from metaqueue.instruments.concurrent import TaskRunner
from metaqueue.utilities.tools        import repeat
from metaqueue.broker                 import MetaBroker
from metaqueue.store                  import MetaStore
from metaqueue.connectors             import StoreToLocalhost


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


@pytest.fixture
def queues():
    task1_queue  = MetaQueue(buffer_size = 3, dtype = int)
    task2_queue  = MetaQueue(buffer_size = 3, dtype = str)
    task3_queue  = MetaQueue(buffer_size = 3, dtype = float)

    yield [task1_queue, task2_queue, task3_queue]


@pytest.fixture
def engines(queues):
    task1_engine = MetadataEngine(topic = Topics.task1, queue = queues[0])
    task2_engine = MetadataEngine(topic = Topics.task2, queue = queues[1])
    task3_engine = MetadataEngine(topic = Topics.task3, queue = queues[2])

    yield [task1_engine, task2_engine, task3_engine]


@pytest.fixture
def db_info():
    yield {'host': "localhost", 'database': "meta", 'user': "test", 'password': "test", 'port': "9050"}


class TestIntegration:
    @pytest.mark.asyncio
    async def test_basic_usage_of_engine(self, engines):
        task1_args = [(1, engines[0]), (2, engines[0]), (3, engines[0])]
        task2_args = [("tmp", engines[1]), ("str", engines[1]), ("something", engines[1])]
        task3_args = [(2.0, engines[2]), (1.0, engines[2]), (4.5, engines[2])]

        await TaskRunner.run(async_funcs = [*repeat(task1, 3), *repeat(task2, 3), *repeat(task3, 3)], 
                             args = [*task1_args, *task2_args, *task3_args])
        
        metadataengines = [engines[0], engines[1], engines[2]]
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


    @pytest.mark.asyncio
    async def test_broker_integration(self, engines, db_info):
        task1_args = [(1, engines[0]), (2, engines[0]), (3, engines[0])]
        task2_args = [("tmp", engines[1]), ("str", engines[1]), ("something", engines[1])]

        await TaskRunner.run(async_funcs = [*repeat(task1, 3), *repeat(task2, 3)], 
                             args = [*task1_args, *task2_args])

        connector  = StoreToLocalhost(path = "./log.txt")
        metastore  = MetaStore(**db_info)
        metabroker = MetaBroker(metadataengines = [engines[0], engines[1]], metastore = metastore, connector = connector)
        metabroker.run(timeout = 10)

        connection = psycopg2.connect(**db_info)
        cursor     = connection.cursor()
        cursor.execute(f"""select * from metadata;""")
        act_record = cursor.fetchone()
        cursor.close()

        connection = psycopg2.connect(**db_info)
        cursor     = connection.cursor()
        cursor.execute(f"truncate table metadata; commit;")
        cursor.close()
        
        with open('./log.txt', 'r') as file:
            content = file.read()
            print(content)

        if os.path.exists("./log.txt"):
            os.remove("./log.txt")

        assert act_record[1] == 'task1_value'
        assert isinstance(act_record[2], datetime.datetime)
        assert act_record[3] == 'Tmp1'
        assert act_record[4] == 'test'

        matches = re.findall(pattern = r"\w*{\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6},\w*}", string = content)
        assert len(matches) == 6
