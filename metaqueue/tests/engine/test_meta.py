"""
TestMetadataEngine
------------------
Testing the MetadataEngine with respect to its
functionalities such as pushing and retrieving 
metadata from the MetaQueue.
"""

import enum
import pytest

from metaqueue.queue  import MetaQueue, Metadata
from metaqueue.engine import MetadataEngine


@pytest.fixture()
def topics():
    class Topics(enum.Enum):
        topic1 = enum.auto()
        topic2 = enum.auto()
    
    yield Topics


class TestMetadataEngine:
    def test_initialisation_s01(self, topics: enum.Enum):
        mq = MetaQueue(buffer_size = 3, dtype = int)
        mdengine  = MetadataEngine(topic = topics.topic1, queue = mq)
        act_topic = mdengine.topic
        exp_topic = topics.topic1

        assert act_topic == exp_topic


    def test_publish_and_retrieval_s01(self, topics: enum.Enum):
        mq = MetaQueue(buffer_size = 3, dtype = str)
        mdengine = MetadataEngine(topic = topics.topic1, queue = mq)
        
        mdengine.publish_to_topic(Metadata(data = "test", name = "test_name", location = "test_location", context = "test"))
        act_metadata = mdengine.retrieve_data_from_queue()
        exp_metadata = Metadata(data = "test", name = "test_name", location = "test_location", context = "test")

        assert act_metadata == exp_metadata


    def test_capacity_s01(self, topics: enum.Enum):
        mq = MetaQueue(buffer_size = 10, dtype = int)
        mdengine = MetadataEngine(topic = topics.topic1, queue = mq)
        
        mdengine.publish_to_topic(Metadata(data = 2, name = "test_name", location = "test_location", context = "test"))
        mdengine.publish_to_topic(Metadata(data = 4, name = "test_name", location = "test_location", context = "test"))
        act_capacity = mdengine.get_queue_capacity()
        exp_capacity = 2

        assert act_capacity == exp_capacity