"""
MetaBroker
----------
Responsible for the scheduling
and management of MetadataEngines and the 
delegation of inserting associated MetaInformation
to the MetaStore.
"""

import time
import attrs
import numpy as np

from metaqueue.engine               import MetadataEngine
from metaqueue.store                import MetaStore, MetaInformation
from metaqueue.connectors.interface import IFConnector


@attrs.define
class MetaBroker:
    """
    MetadataEngines collect Metadata and store them inside
    of queues called MetaQueues. The stored metadata are retrieved 
    from the MetadataEngines in order to store them at their appropriate
    destination.

    Parameters
    ----------
    metadataengines: list[MetadataEngine]
        The metadataengines which should be managed by the MetaBroker
    metastore: MetaStore
        Metainformation is given to the MetaStore such that it can be 
        stored inside of a Postgres database
    """
    metadataengines = attrs.field(factory = list)
    metastore       = attrs.field(factory = MetaStore)
    connector       = attrs.field(factory = IFConnector)


    def __init__(self, metadataengines: list[MetadataEngine], metastore: MetaStore, connector: IFConnector) -> None:
        self.metadataengines = metadataengines
        self.metastore       = metastore
        self.connector       = connector


    def run(self, timeout: int) -> None:
        """
        Metadata is as long queried as long the timeout
        is not exceeded or all the metadataengines are empty.

        Parameters
        ----------
        timeout: int
            Time in seconds since the epoch as a integer, when the timeout is
            exceeded the MetaBroker will stop querying for metadata
        """
        capacity_of_queues = np.zeros(len(self.metadataengines))
        while True:
            stopwatch = time.time()
            for index, mdengine in enumerate(self.metadataengines):
                current_capacity          = mdengine.get_queue_capacity()
                capacity_of_queues[index] = current_capacity
                if current_capacity > 0:
                    metadata = mdengine.retrieve_data_from_queue()
                    metainfo = MetaInformation(name = metadata.name, location = metadata.location, context = metadata.context)
                    self.metastore.push_metainformation(metainfo)
                    self.connector.store(metadata = metadata)

            if (time.time() - stopwatch) >= timeout:
                break

            is_empty = [True if capacity == 0 else False for capacity in capacity_of_queues]
            if np.all(is_empty):
                break
