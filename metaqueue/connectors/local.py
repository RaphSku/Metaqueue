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
    """
    Metadata is stored to a file on the local filesystem

    Parameters
    ----------
    path: str
        Path to the file where the metadata is persisted
    """
    path =  attrs.field(factory = str)


    def __init__(self, path: str) -> None:
        self.path = path


    def store(self, metadata: Metadata) -> None:
        """
        Storing the metadata in append mode to the appropriate file

        Parameters
        ----------
        metadata: Metadata
            Metadata which should be stored in a file in a format
            which resembles the open metrics format
        """
        metadata_as_string = self._parse_metadata(metadata)

        with open(self.path, "a") as file:
            file.write(metadata_as_string)
            file.write("\n")


    def _parse_metadata(self, metadata: Metadata):
        """
        Parses the content of the metadata into a string

        Parameters
        ----------
        metadata: Metadata
            Metadata which should be parsed into a string in the format:
            metadata_name{timestamp,metadata_data}
        """
        timestamp = datetime.datetime.now()
        
        return f"{metadata.name}{{{timestamp},{metadata.data}}}"
        