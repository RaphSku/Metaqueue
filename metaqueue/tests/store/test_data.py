"""
TestMetaStore
-------------
Testing the MetaStore whether it creates a 
database with a relation and the insertion
of metainformation into the relation
"""

import psycopg2
import pytest

from metaqueue.store  import MetaStore, MetaInformation


@pytest.fixture
def db_info():
    yield {'host': "localhost", 'database': "meta", 'user': "test", 'password': "test", 'port': "9050"}


@pytest.fixture
def metainformation():
    yield MetaInformation(name = "e407d43e-f075-47ce-ad1a", location = "Generate", context = "Bound")


def teardown_metainformation(host, database, user, password, port):
    connection = psycopg2.connect(host = host, 
                                  database = database, 
                                  user = user,
                                  password = password, 
                                  port = port)
    cursor     = connection.cursor()
    cursor.execute(f"delete from metadata where name='e407d43e-f075-47ce-ad1a'; commit;")
    cursor.close()


class TestMetaStore:
    def test_initialisation_s01(self, db_info):
        MetaStore(**db_info)
        
        connection = psycopg2.connect(**db_info)
        cursor     = connection.cursor()
        cursor.execute(f"select exists(select * from information_schema.tables where table_name='metadata');")
        act_record = cursor.description
        cursor.close()

        assert act_record[0].name == "exists"


    def test_push_s01(self, db_info, metainformation):
        metastore = MetaStore(**db_info)
        metastore.push_metainformation(info = metainformation)

        connection = psycopg2.connect(**db_info)
        cursor     = connection.cursor()
        cursor.execute(f"select name, location, context from metadata;")
        act_record = cursor.fetchone()
        cursor.close()

        assert act_record[0] == "e407d43e-f075-47ce-ad1a"
        assert act_record[1] == "Generate"
        assert act_record[2] == "Bound"

        teardown_metainformation(**db_info)