
import typing
import attrs
import psycopg2

from dataclasses import dataclass


@dataclass
class MetaInformation:
    name: str
    location: str
    context: str


@attrs.define
class MetaStore:
    _params = attrs.field(factory = dict, type = dict[str, str])


    def __init__(self, host: str, database: str, user: str, password: str, port: str) -> None:
        self._params["host"]     = host
        self._params["database"] = database
        self._params["user"]     = user
        self._params["password"] = password
        self._params["port"]     = port

        self._create_table()


    def push_metainformation(self, info: MetaInformation):
        self._check_info(info)

        connection = self._connect_to_psql_db()
        cursor     = connection.cursor()
        cursor.execute(f"insert into metadata (name, location, context) values ({info.name}, {info.location}, {info.context});")
        cursor.close()


    def _create_table(self) -> None:
        connection = self._connect_to_psql_db()
        cursor     = connection.cursor()
        cursor.execute("select exists(select * from information_schema.tables where table_name='metadata');")
        table_exists = bool(cursor.fetchone()[0])
        if not table_exists:
            cursor.execute("""
            create table metadata(
                id int primary key not null,
                name varchar(30) not null check (name <> ''),
                timestamp timestamptz not null default now(),
                location varchar(30) not null check (location <> ''),
                context varchar(30) not null check (context <> '')
                );
            """)
        cursor.close()


    def _connect_to_psql_db(self) -> typing.Any:
        return psycopg2.connect(**self._params)


    def _check_info(self, info) -> bool:
        pass