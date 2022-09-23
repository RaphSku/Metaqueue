"""
MetadataEngine
--------------
Efficient engine which manages queues in which metadata
can be passed to the metadata-store from which metadata gets
distributed to its target location
"""

import enum
import attrs

from metaqueue.queue import MetaQueue, Metadata


@attrs.define
class MetadataEngine:
    """
    Manages the respective metadata queue and is responsible
    for pushing the data into the metadata store

    Parameters
    ----------
    topic: enum.Enum
        Every metadataengine has a topic it serves, the topic
        subsummes all the metadata which are related
        by the topic
    queue: MetaQueue
        For this use-case queue data structure which
        holds metadata
    """
    topic  = attrs.field(factory = enum.Enum)
    _queue = attrs.field(factory = MetaQueue)


    def __init__(self, topic: enum.Enum, queue: MetaQueue) -> None:
        self.topic  = topic
        self._queue = queue

    
    def publish_to_topic(self, metadata: Metadata) -> None:
        """
        The `metadata` will be pushed to the appropriate metadataqueue

        Parameters
        ----------
        metadata: Metadata
            Metadata dataclass instance which holds all the important
            information 
        """
        self._queue.push(metadata)


    def retrieve_data_from_queue(self) -> Metadata:
        """
        Retrieving metadata from the queue according to the FIFO principle

        Returns
        -------
        Metadata
            Metadata holds with its attributes all the important
            information abou the `metadata`
        """

        return self._queue.pop()


    def get_queue_capacity(self) -> int:
        """

        Returns
        -------
        int
            Returns the current queue length
        """

        return len(self._queue)
    