"""
TestMetaConsumer
----------------
Testing MetaConsumer if the values get pushed correctly 
and if one can loop over the MetaConsumer
"""

import enum
import pytest

from metaqueue.client.consumer import MetaConsumer


@pytest.fixture()
def topics():
    class Topics(enum.Enum):
        FIRST  = enum.auto()
        SECOND = enum.auto()
    
    yield Topics


class TestMetaConsumer:
    def test_initialization_s01(self, topics: enum.Enum):
        metaconsumer = MetaConsumer(topic = topics.FIRST)
        act_topic    = metaconsumer.topic

        assert act_topic == topics.FIRST


    def test_consumption_s01(self, topics: enum.Enum):
        metaconsumer = MetaConsumer(topic = topics.FIRST)
        metaconsumer.push(item = 2)
        metaconsumer.push(item = 5)
        metaconsumer.push(item = 10)
        metaconsumer.push(item = 12)

        act_data = []
        for item in metaconsumer:
            act_data.append(item)

        exp_data = [2, 5, 10, 12]

        assert act_data == exp_data