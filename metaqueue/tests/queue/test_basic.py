"""
TestBasicQueue
--------------
Testing the queue and its characteristics such as
the representation, the length and the push and pop
functions.
"""

from metaqueue.queue import MetaQueue, Metadata


class TestBasicQueue:
    def test_initialisation_s01(self):
        mq = MetaQueue(buffer_size = 10, dtype = float)
        act_buffer_size = mq.buffer_size
        act_dtype       = mq.dtype

        assert act_buffer_size == 10
        assert act_dtype       == float


    def test_push_and_pop_s01(self):
        mq = MetaQueue(buffer_size = 3, dtype = str)
        mq.push(Metadata(data = "here", name = "tmp", location = "a1", context = "test"))
        mq.push(Metadata(data = "we", name = "tmp", location = "a1", context = "test"))
        act_result_1 = mq.pop()
        mq.push(Metadata(data = "go", name = "tmp", location = "a1", context = "test"))
        act_result_2 = mq.pop()

        assert act_result_1 == Metadata(data = "here", name = "tmp", location = "a1", context = "test")
        assert act_result_2 == Metadata(data = "we", name = "tmp", location = "a1", context = "test")


    def test_repr_s01(self):
        mq = MetaQueue(buffer_size = 2, dtype = int)
        mq.push(Metadata(data = 2, name = "tmp", location = "a1", context = "test"))
        mq.push(Metadata(data = 3, name = "tmp", location = "a1", context = "test"))

        act_repr = repr(mq)
        exp_repr = "deque([Metadata(data=2, name='tmp', location='a1', context='test'), " +\
                   "Metadata(data=3, name='tmp', location='a1', context='test')], maxlen=2)"

        assert act_repr == exp_repr


    def test_len_s01(self):
        mq = MetaQueue(buffer_size = 10, dtype = str)
        mq.push(Metadata(data = "here", name = "tmp", location = "a1", context = "test"))
        mq.push(Metadata(data = "we", name = "tmp", location = "a1", context = "test"))
        mq.pop()
        mq.push(Metadata(data = "go", name = "tmp", location = "a1", context = "test"))
        act_len = len(mq)
        exp_len = 2

        assert act_len == exp_len
