import sys

from dynaconf import *
from loguru import logger

from py.api import FlaskSrv
from py.core import MainHub
from py.core.notifications import NotificationSrv, NotificationSeverityEnum
from py.core.notifications.log_target import LoggingNotificationTarget
from py.core.trigger import TriggerService
from py.core.db import DatabaseSrv
from py.core.executor import ExecutorSrv
from py.core.redis import RedisSrv
from py.drivers.service import DriverSrv
from py.models.user import UserMdl


def settings_validation():
    settings.validators.register(
        Validator('SQL_ENGINE', 'SQL_HOST', 'SQL_DBNAME', must_exist=True)
    )
    settings.validators.validate()


def configure():
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
    MainHub.register(DatabaseSrv(settings['SQL_ENGINE']), DatabaseSrv)
    MainHub.register(TriggerService(MainHub.retrieve(RedisSrv)), TriggerService)
    MainHub.register(ExecutorSrv(), ExecutorSrv)

    MainHub.register(NotificationSrv(), NotificationSrv)
    MainHub.retrieve(NotificationSrv).add_target(LoggingNotificationTarget(NotificationSeverityEnum.WARNING, prefix='ALARM'))

    MainHub.register(FlaskSrv(), FlaskSrv)

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
    MainHub.retrieve(FlaskSrv).run()