"""
MetaStore and MetaInformation
-----------------------------
MetaInformation are information related to the Metadata, Metainformation
are stored in a PostgreSQL database named "meta" by default inside of a relation
called "metadata". The database name can be changed when providing a different
database name for the first time, MetaStore will create the database and the relation
if it does not exist yet. The MetaStore is responsible for inserting MetaInformation
into the appropriate relation.
"""
import typing
import attrs
import psycopg2

from dataclasses import dataclass


@dataclass
class MetaInformation:
    """
    Metainformation related to the Metadata collected
    by the MetadataEngines

    Parameters
    ----------
    name: str
        Name of the associated metadata
    location: str
        The location where the metadata is stored or was
        written to
    context: str
        Describes under which context the metadata was created
    """
    name: str
    location: str
    context: str


@attrs.define
class MetaStore:
    """
    Manages the metastore which stores metainformation
    about metadata, its the single source of truth 
    to query for information related to metadata.

    Parameters
    ----------
    host: str
        Host of the database
    database: str
        Name of the database
    user: str
        User needed to login to the database
    password: str
        Needed as credential for interacting with the psql db
    port: str, default = 5432
        Port under which the db is running, defaults to the default port
        for Postgres databases
    """
    host     = attrs.field(factory = str)
    database = attrs.field(factory = str)
    user     = attrs.field(factory = str)
    password = attrs.field(factory = str)
    port     = attrs.field(default = "5432")
    _params  = attrs.field(factory = dict[str, str])


    def __init__(self, host: str, database: str, user: str, password: str, port: str = "5432") -> None:
        self._params             = {}
        self._params["host"]     = host
        self._params["database"] = database
        self._params["user"]     = user
        self._params["password"] = password
        self._params["port"]     = port

        self._create_table()


    def push_metainformation(self, info: MetaInformation) -> None:
        """
        Metainformation is pushed to the Postgres database

        Paramaters
        ----------
        info: MetaInformation
            `info` is pushed to the specified database inside the relation `metadata`
        """
        self._check_info(info)

        connection = self._connect_to_psql_db()
        cursor     = connection.cursor()
        cursor.execute(f"""insert into metadata (name, location, context) values ('{info.name}', '{info.location}', '{info.context}');
                           commit;""")
        cursor.close()


    def _create_table(self) -> None:
        """
        When instantiating MetaStore for the first time, it will create
        the relation `metadata` inside of the database if it does not exist
        beforehand. If even the database was not created yet, it will be 
        created by this method            
        """
        try:
            connection = self._connect_to_psql_db()
        except psycopg2.OperationalError:
            connection = psycopg2.connect(host     = self._params["host"],
                                          database = "postgres",
                                          user     = self._params["user"],
                                          password = self._params["password"],
                                          port     = self._params["port"])
            cursor     = connection.cursor()
            cursor.execute(f"create database {self._params['database']};")
            cursor.close()

            connection = self._connect_to_psql_db()
        cursor     = connection.cursor()
        cursor.execute("select exists(select * from information_schema.tables where table_name='metadata');")
        table_exists = bool(cursor.fetchone()[0])
        if not table_exists:
            cursor.execute("""
            create table metadata(
                id bigserial primary key,
                name varchar(30) not null check (name <> ''),
                timestamp timestamptz not null default now(),
                location varchar(30) not null check (location <> ''),
                context varchar(30) not null check (context <> '')
                );
            commit;
            """)
        cursor.close()


    def _connect_to_psql_db(self) -> typing.Any:
        """
        Connects to the Postgres database with the specified credentials

        Returns
        -------
        Any
            A connection object from which the cursor can be accessed
        """
        return psycopg2.connect(**self._params)


    def _check_info(self, info: MetaInformation) -> None:
        """
        Checks whether `info` is an instance of MetaInformation

        Raises
        ------
        TypeError
            When `info` is not an instance of MetaInformation
        """
        if not isinstance(info, MetaInformation):
            raise TypeError(f"info needs to be an instance of MetaInformation")