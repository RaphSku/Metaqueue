"""
IFConnector
-----------
Interface for the connectors, the connectors
should all at minimum implement the store method
which should store the metadata to the target
storage.
"""

import abc
from abc import abstractmethod

from metaqueue.queue import Metadata


class IFConnector(metaclass = abc.ABCMeta):
    """
    Interface for Connectors
    """
    
    @abstractmethod
    def store(self, metadata: Metadata) -> None:
        pass