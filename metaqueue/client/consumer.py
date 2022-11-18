"""
MetaConsumer
------------
Consumes metadata values from a specific topic
"""

import attrs
import enum

from typing import Any


@attrs.define
class MetaConsumer:
    """
    The Metabroker is pushing metadata values to the
    corresponding MetaConsumer according to the topic

    Parameters
    ----------
    topic: enum.Enum
        Topic bundles metadata into a categorical group
    """
    __data = attrs.field(factory = list)
    topic  = attrs.field(factory = enum.Enum)


    def __init__(self, topic: enum.Enum) -> None:
        self.topic  = topic
        self.__data = []

    
    def push(self, item: Any) -> None:
        """
        The value of the metadata gets pushed to the corresponding consumer

        Parameters
        ----------
        item: Any
            Item corresponds to the value of the metadata
        """
        self.__data.append(item)


    def __iter__(self):
        for item in self.__data:
            yield item