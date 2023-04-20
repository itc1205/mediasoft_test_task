import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL
import sqlalchemy.ext.declarative as dec
from _types.database_types import _DB_TYPE

import os
from dotenv import load_dotenv

load_dotenv()

DB = os.getenv("DB_TYPE")
USER = os.getenv("USER")
DB_NAME = os.getenv("DB_NAME")

SqlAlchemyBase = dec.declarative_base()


__factory = None

def global_init(db_file: str = None) -> None:
    global __factory

    if __factory:
        return
    
    if not db_file or not db_file.strip():
        raise Exception("Не указан файл базы данных!")
    connection_url = ""
    
    if DB == _DB_TYPE.PostgreSQL:
        connection_url = URL.create(
            drivername="postgresql",
            username=USER,
            host="/run/postgresql/",
            database=DB_NAME
        )
    else:
        connection_url = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    print(f"Подключение к базе данных по адресу {connection_url}")

    engine = sa.create_engine(connection_url, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models
    
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory