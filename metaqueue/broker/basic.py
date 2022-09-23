"""

"""

import time
import attrs

from metaqueue.engine import MetadataEngine
from metaqueue.store  import MetaStore, MetaInformation


@attrs.define
class MetaBroker:
    _metadataengines = attrs.field(factory = list, type = list[MetadataEngine])
    _metastore       = attrs.field(factory = MetaStore)


    def __init__(self, metadataengines: list[MetadataEngine], metastore: MetaStore) -> None:
        self._metadataengines = metadataengines
        self._metastore       = metastore


    def run(self, timeout: int) -> None:
        stopwatch = time.clock()
        while True:
            if (time.clock() - stopwatch) >= timeout:
                break

            for mdengine in self._metadataengines:
                if mdengine.get_queue_capacity() > 0:
                    metadata = mdengine.retrieve_data_from_queue()
                    metainfo = MetaInformation(name = metadata["name"], location = metadata["location"])
                    self._metastore.push_metainformation(metainfo)
