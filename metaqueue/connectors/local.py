"""
StoreToLocalhost
----------------
Connector who stores metadata to a log file
on the localhost under user-specific path.
"""

import attrs
import datetime

from metaqueue.queue import Metadata
from metaqueue.connectors.interface import IFConnector


@attrs.define
class StoreToLocalhost(IFConnector):
    path =  attrs.field(factory = str)


    def __init__(self, path: str) -> None:
        self.path = path


    def store(self, metadata: Metadata) -> None:
        metadata_as_string = self._parse_metadata(metadata)

        with open(self.path, "a") as file:
            file.write(metadata_as_string)


    def _parse_metadata(self, metadata: Metadata):
        timestamp = datetime.datetime.now()
        
        return f"{metadata.name}{{{timestamp},{metadata.data}}}"
        