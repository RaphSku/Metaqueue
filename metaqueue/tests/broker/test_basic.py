"""
TestBasicMetaBroker
-------------------
Testing the Metabroker whether the running 
of the metadataengines works and if the metadata
is stored correctly at their appropriate destination.
"""

import os
import pytest 
import enum
import dotenv

from metaqueue.queue  import MetaQueue
from metaqueue.engine import MetadataEngine
from metaqueue.broker import MetaBroker
from metaqueue.store  import MetaStore


@pytest.fixture
def metastore():
    dotenv.load_dotenv("config.env")

    yield MetaStore(host = os.getenv("HOST"), 
                    database = os.getenv("DATABASE"), 
                    user = os.getenv("USER"), 
                    password = os.getenv("PASSWORD"), 
                    port = os.getenv("PORT"))
    

@pytest.fixture
def metadataengines():
    class Topics(enum.Enum):
        topic1 = enum.auto()
        topic2 = enum.auto()

    metaqueue_1 = MetaQueue(buffer_size = 2, dtype = str)
    metaqueue_2 = MetaQueue(buffer_size = 2, dtype = int)
    metadataengine_1 = MetadataEngine(topic = Topics.topic1, queue = metaqueue_1)
    metadataengine_2 = MetadataEngine(topic = Topics.topic2, queue = metaqueue_2)

    yield [metadataengine_1, metadataengine_2]


class TestBasicMetaBroker:
    def test_running_s01(self, metastore, metadataengines):
        metabroker = MetaBroker(metadataengines = metadataengines, metastore = metastore)
        metabroker.run(timeout = 10)