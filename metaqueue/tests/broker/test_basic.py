"""
TestBasicMetaBroker
-------------------
Testing the Metabroker whether the running 
of the metadataengines works and if the metadata
is stored correctly at their appropriate destination.
"""

import os
import psycopg2
import pytest 
import enum
import dotenv

from metaqueue.queue      import MetaQueue, Metadata
from metaqueue.engine     import MetadataEngine
from metaqueue.broker     import MetaBroker
from metaqueue.store      import MetaStore
from metaqueue.connectors import StoreToLocalhost


@pytest.fixture
def setUp():
    dotenv.load_dotenv("config.env")

    yield {'host': os.getenv("HOST"), 
           'database': os.getenv("DATABASE"), 
           'user': os.getenv("USER"), 
           'password': os.getenv("PASSWORD"), 
           'port': os.getenv("PORT")}


@pytest.fixture
def metastore(setUp):
    dotenv.load_dotenv("config.env")

    yield MetaStore(**setUp)
    

@pytest.fixture
def metadataengines():
    class Topics(enum.Enum):
        topic1 = enum.auto()
        topic2 = enum.auto()

    metadata_1  = Metadata(data = {'name': 'Mary', 'email': 'mary@test.test'}, name = "Test Person", location = "local", context = "test")
    metadata_2  = Metadata(data = 247, name = "total_requests", location = "local", context = "test")
    metaqueue_1 = MetaQueue(buffer_size = 2, dtype = dict)
    metaqueue_1.push(metadata_1)
    metaqueue_2 = MetaQueue(buffer_size = 2, dtype = int)
    metaqueue_2.push(metadata_2)
    metadataengine_1 = MetadataEngine(topic = Topics.topic1, queue = metaqueue_1)
    metadataengine_2 = MetadataEngine(topic = Topics.topic2, queue = metaqueue_2)

    yield [metadataengine_1, metadataengine_2]
    

def tearDown(db_info):
    connection = psycopg2.connect(**db_info)
    cursor     = connection.cursor()
    cursor.execute(f"delete from metadata where name='Test Person'; commit;")
    cursor.execute(f"delete from metadata where name='total_requests'; commit;")
    cursor.close()

    if os.path.exists("./log.txt"):
        os.remove("./log.txt")


class TestBasicMetaBroker:
    def test_running_s01(self, metastore, metadataengines, setUp):
        connector  = StoreToLocalhost(path = "./log.txt")
        metabroker = MetaBroker(metadataengines = metadataengines, metastore = metastore, connector = connector)
        metabroker.run(timeout = 10)

        tearDown(setUp)