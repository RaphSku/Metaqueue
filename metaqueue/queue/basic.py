"""
MetaQueue
--------------
Efficient queue which transports metadata from the scripts to the 
Metadata Engine
"""

import attrs

from typing import Any
from collections import deque
from dataclasses import dataclass

from metaqueue.exception.container import BufferOverflow


@dataclass
class Metadata:
    data: Any
    name: str
    location: str
    context: str


@attrs.define
class MetaQueue:
    """
    Efficient FIFO storage data structure

    Parameters
    ----------
    buffer_size: int
        Controls the number of data which can be pushed
        into the queue
    dtype: type
        Queue will only accept data from the type `dtype`
    """
    _data       = attrs.field(factory = deque)
    buffer_size = attrs.field(factory = int)
    dtype       = attrs.field(factory = type)
    _index      = attrs.field(factory = int)


    def __init__(self, buffer_size: int, dtype: type) -> None:
        self.buffer_size = buffer_size
        self._data       = deque(maxlen = buffer_size)
        self.dtype       = dtype
        self._index      = 0


    def push(self, metadata: Metadata) -> None:
        """
        Insert `metadata` into a queue

        Parameters
        ----------
        metadata: Metadata
            Dataclass instance for metadata representation

        Raises
        ------
            BufferOverflow
                When the queue is full and the producer tries to push more
                items to it, then this exception will be raised
            TypeError
                Raised when the dtype of the metadata is not compatible with the
                supported dtype of the queue
        """
        if self._index >= self.buffer_size:
            raise BufferOverflow("Queue is full!")
        if not isinstance(metadata.data, self.dtype):
            raise TypeError(f"Value is not of type {self.dtype}, cannot be inserted!")
        self._data.append(metadata)
        self._index += 1


    def pop(self) -> Any:
        """
        Returns
        -------
            Any
                Data is taken out of the queue and returned

        Raises
        ------
            ValueError
                When the Queue is empty, nothing can be removed
        """
        if self._index == 0:
            raise ValueError(f"Queue is empty, nothing to remove!")
        self._index -= 1
        return self._data.popleft()


    def __repr__(self) -> str:
        return f"{self._data}"


    def __len__(self) -> int:
        return len(self._data)
