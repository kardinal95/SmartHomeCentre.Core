import sqlalchemy as db
from dynaconf import settings, Validator
from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class DatabaseSrv:
    def __init__(self, engine_type):
        self.engine = None
        self.connection = None
        self.session = None
        self.init_db(engine_type)

    def init_db(self, engine_type):
        mapping = {
            'psql': self.init_psql
        }

        try:
            mapping[engine_type]()
        except KeyError as e:
            raise KeyError('Incorrect sql engine!') from e

    def init_psql(self):
        settings.validators.register(
            Validator('psql_user', 'psql_pass', must_exist=True)
        )
        settings.validators.validate()

        self.engine = db.create_engine('postgresql+psycopg2://{user}:{password}@{hostname}/{dbname}'.format(
                                                     user=settings.PSQL_USER, password=settings.PSQL_PASS,
                                                     hostname=settings.SQL_HOST, dbname=settings.SQL_DBNAME))
        try:
            self.connection = self.engine.connect()
            self.session = sessionmaker(bind=self.engine)
        except OperationalError as e:
            logger.exception(e)
            self.connection = None
