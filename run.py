import sys

from loguru import logger
from dynaconf import settings, Validator, ValidationError

from py.drivers.master import DriverMaster
from py.main.db import init_db, DatabaseObjects


def settings_validation():
    settings.validators.register(
        Validator('SQL_ENGINE', 'SQL_HOST', 'SQL_DBNAME', must_exist=True)
    )
    settings.validators.validate()


def initialize():
    # Configuration of logger
    logger.remove()
    if settings.ENV_FOR_DYNACONF == 'production':
        logger.add('main.log', level='INFO', rotation='10 MB', backtrace=False, diagnose=False)
        logger.add(sys.stdout, level='INFO', colorize=True, backtrace=False, diagnose=False)
    if settings.ENV_FOR_DYNACONF == 'development':
        logger.add(sys.stdout, colorize=True, backtrace=True, diagnose=True)
        logger.add('debug.log', backtrace=True, diagnose=True)

    logger.debug('Running the program in {mode} environment...', mode=settings.ENV_FOR_DYNACONF)


if __name__ == '__main__':
    initialize()
    try:
        settings_validation()
        init_db()
    except ValidationError as e:
        logger.exception(e)
    except KeyError as e:
        logger.exception(e)

    # Exit if not connected
    if DatabaseObjects.connection is None:
        logger.critical('Cannot work without connection to database! Closing...')

    master = DriverMaster()