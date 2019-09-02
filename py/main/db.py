from dynaconf import settings, Validator
from loguru import logger
import sqlalchemy as db
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


def init_db():
    mapping = {
        'psql': init_psql
    }

    try:
        mapping[settings.SQL_ENGINE]()
    except KeyError as e:
        raise KeyError('Incorrect sql engine!') from e


def init_psql():
    settings.validators.register(
        Validator('psql_user', 'psql_pass', must_exist=True)
    )
    settings.validators.validate()

    DatabaseObjects.engine = db.create_engine('postgresql+psycopg2://{user}:{password}@{hostname}/{dbname}'.format(
                                                 user=settings.PSQL_USER, password=settings.PSQL_PASS,
                                                 hostname=settings.SQL_HOST, dbname=settings.SQL_DBNAME))
    try:
        DatabaseObjects.connection = DatabaseObjects.engine.connect()
        DatabaseObjects.session = sessionmaker(bind=DatabaseObjects.engine)
    except OperationalError as e:
        logger.exception(e)
        DatabaseObjects.connection = None


class DatabaseObjects:
    engine = None
    connection = None
    session = None
