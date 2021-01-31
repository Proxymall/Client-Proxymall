# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./proxymall.db"
# # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/protech?"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


from contextvars import ContextVar

import peewee
from playhouse.mysql_ext import MySQLConnectorDatabase

db_state_default = {"closed": None, "conn": None,
                    "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]

# db = PostgresqlExtDatabase(
#     DATABASE_NAME,
#     user="postgres",
#     password="root",
#     host="127.1.0.0",
#     port="5432"
# )

# db = MySQLConnectorDatabase(
#     "proxcbvs_proxymall",
#     user="proxcbvs_backend",
#     password="@Proxymall2020",
#     host="198.54.116.211",
#     port="3306"
# )

db = peewee.SqliteDatabase("proxymall.db", check_same_thread=False)

db._state = PeeweeConnectionState()
