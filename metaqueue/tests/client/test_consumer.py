import enum
from metaqueue.client.consumer import MetaConsumer


class TestMetaConsumer:
    def test_initialization_s01(self):
        class Topics(enum.Enum):
            FIRST  = enum.auto()
            SECOND = enum.auto()

        metaconsumer = MetaConsumer(topic = Topics.FIRST)
        act_topic    = metaconsumer.topic

        assert act_topic == Topics.FIRST