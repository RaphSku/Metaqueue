import attrs
import enum


@attrs.define
class MetaConsumer:
    __data = attrs.field(factory = list)
    topic  = attrs.field(factory = enum.Enum)


    def __init__(self, topic: enum.Enum) -> None:
        self.topic = topic

    
    def push(self, item):
        self.__data.append(item)


    def __iter__(self):
        while True:
            for item in self.__data:
                yield item