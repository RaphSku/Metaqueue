"""
TestMetaStore
-------------
Testing the MetaStore whether it creates a 
database with a relation and the insertion
of metainformation into the relation
"""

import os
import psycopg2
import pytest
import dotenv

from metaqueue.store  import MetaStore, MetaInformation


@pytest.fixture
def load_db_info():
    dotenv.load_dotenv("config.env")

    yield [os.getenv("HOST"), os.getenv("DATABASE"), os.getenv("USER"), os.getenv("PASSWORD"), os.getenv("PORT")]


@pytest.fixture
def metainformation():
    yield MetaInformation(name = "e407d43e-f075-47ce-ad1a", location = "Generate", context = "Bound")


def teardown_metainformation():
    connection = psycopg2.connect(host = "localhost", database = "meta", user = "raphael", password = "test1", port = "5432")
    cursor     = connection.cursor()
    cursor.execute(f"delete from metadata where name='e407d43e-f075-47ce-ad1a'; commit;")
    cursor.close()


class TestMetaStore:
    def test_initialisation_s01(self, load_db_info):
        MetaStore(host = load_db_info[0], 
                  database = load_db_info[1], 
                  user = load_db_info[2],
                  password = load_db_info[3], 
                  port = load_db_info[4])
        
        connection = psycopg2.connect(host = load_db_info[0], 
                                      database = load_db_info[1],
                                      user = load_db_info[2], 
                                      password = load_db_info[3], 
                                      port = load_db_info[4])
        cursor     = connection.cursor()
        cursor.execute(f"select exists(select * from information_schema.tables where table_name='metadata');")
        act_record = cursor.description
        cursor.close()

        assert act_record[0].name == "exists"


    def test_push_s01(self, load_db_info, metainformation):
        metastore = MetaStore(host = load_db_info[0], 
                              database = load_db_info[1], 
                              user = load_db_info[2], 
                              password = load_db_info[3], 
                              port = load_db_info[4])
        metastore.push_metainformation(info = metainformation)

        connection = psycopg2.connect(host = load_db_info[0], 
                                      database = load_db_info[1], 
                                      user = load_db_info[2], 
                                      password = load_db_info[3], 
                                      port = load_db_info[4])
        cursor     = connection.cursor()
        cursor.execute(f"select name, location, context from metadata;")
        act_record = cursor.fetchone()
        cursor.close()

        assert act_record[0] == "e407d43e-f075-47ce-ad1a"
        assert act_record[1] == "Generate"
        assert act_record[2] == "Bound"

        teardown_metainformation()