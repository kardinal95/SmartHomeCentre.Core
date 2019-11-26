import sys
from uuid import UUID

from dynaconf import settings, Validator, ValidationError
from loguru import logger

from py.core import MainHub
from py.core.binder import BinderSrv
from py.core.db import DatabaseSrv
from py.core.executor import ExecutorSrv
from py.core.redis import RedisSrv
from py.drivers.service import DriverSrv


def settings_validation():
    settings.validators.register(
        Validator('SQL_ENGINE', 'SQL_HOST', 'SQL_DBNAME', must_exist=True)
    )
    settings.validators.validate()


def configure():
    # Configuration of logger
    logger.remove()
    if settings.ENV_FOR_DYNACONF == 'production':
        logger.add('core.log', level='INFO', rotation='10 MB', backtrace=False, diagnose=False)
        logger.add(sys.stdout, level='INFO', colorize=True, backtrace=False, diagnose=False)
    if settings.ENV_FOR_DYNACONF == 'development':
        logger.add(sys.stdout, colorize=True, backtrace=True, diagnose=True)
        logger.add('debug.log', backtrace=True, diagnose=True)

    logger.debug('Running the program in {mode} environment...', mode=settings.ENV_FOR_DYNACONF)


def register_services():
    # TODO Move logging to services
    # Service loading
    MainHub.register(RedisSrv(), RedisSrv)
    logger.info('Redis service registered')
    MainHub.register(DatabaseSrv(settings['SQL_ENGINE']), DatabaseSrv)
    logger.info('Database service registered')
    MainHub.register(BinderSrv(MainHub.retrieve(RedisSrv)), BinderSrv)

    MainHub.register(ExecutorSrv(), ExecutorSrv)

    # Exit if not connected
    if MainHub.retrieve(DatabaseSrv).connection is None:
        logger.critical('Cannot work without connection to database! Closing...')


if __name__ == '__main__':
    configure()
    try:
        settings_validation()
        register_services()
    except ValidationError as e:
        logger.exception(e)
    except KeyError as e:
        logger.exception(e)

    MainHub.register(DriverSrv(), DriverSrv)

    #MainHub.retrieve(DriverSrv).instances[UUID('63edb3aa-7e13-4900-8d46-3e39cd9047d0')].process_data_to_ep(UUID('e57e5c77-7797-41e9-a633-bde686ed51de'), {'red': 255})
    while True:
        pass