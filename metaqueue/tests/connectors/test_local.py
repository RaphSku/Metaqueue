"""
TestStoreToLocalhost
--------------------
Testing whether the metadata is correctly
stored on the local filesystem
"""

import os
import re
import pytest

from metaqueue.queue      import Metadata
from metaqueue.connectors import StoreToLocalhost


@pytest.fixture
def path():
    yield f"{os.path.dirname(os.path.abspath(__file__))}/log.txt"


@pytest.fixture
def metadata():
    yield Metadata(data = {'test': [1, 4, 2, 3], 'attr': ["going", "here"]}, name = "meta_test", location = "test", context = "test")


def teardown():
    path = f"{os.path.dirname(os.path.abspath(__file__))}/log.txt"
    if os.path.exists(path):
        os.remove(path)
    

class TestStoreToLocalhost:
    def test_initialisation_s01(self, path):
        store_to_localhost = StoreToLocalhost(path = path)
        act_path = store_to_localhost.path

        assert act_path == path


    def test_storing_s01(self, path, metadata):
        store_to_localhost = StoreToLocalhost(path = path)
        store_to_localhost.store(metadata)

        with open(path, "r") as file:
            act_content = file.read()

            act_metadata_name = re.search(r"\w*?(?={)", act_content)[0]
            act_metadata_data = re.search(r",.*(?=})", act_content)[0][1:]

            assert act_metadata_name == "meta_test"
            assert act_metadata_data == "{'test': [1, 4, 2, 3], 'attr': ['going', 'here']}"

        teardown()

    
    def test_storing_s02(self, path):
        metadata = Metadata(data = 28.52532, name = "meta_test", location = "test", context = "test")
        store_to_localhost = StoreToLocalhost(path = path)
        store_to_localhost.store(metadata)

        with open(path, "r") as file:
            act_content = file.read()

            act_metadata_name = re.search(r"\w*?(?={)", act_content)[0]
            act_metadata_data = re.search(r",.*(?=})", act_content)[0][1:]

            assert act_metadata_name == "meta_test"
            assert act_metadata_data == "28.52532"
        
        teardown()


    def test_storing_s03(self, path):
        metadata = Metadata(data = [24.24, 23, 247.25799], name = "meta_test", location = "test", context = "test")
        store_to_localhost = StoreToLocalhost(path = path)
        store_to_localhost.store(metadata)

        with open(path, "r") as file:
            act_content = file.read()

            act_metadata_name = re.search(r"\w*?(?={)", act_content)[0]
            act_metadata_data = re.search(r",.*(?=})", act_content)[0][1:]

            assert act_metadata_name == "meta_test"
            assert act_metadata_data == "[24.24, 23, 247.25799]"
        
        teardown()