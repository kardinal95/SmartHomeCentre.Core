from loguru import logger

from py.core.notifications import NotificationSeverityEnum


class LoggingNotificationTarget:
    mapping = {
        NotificationSeverityEnum.CRITICAL: logger.critical,
        NotificationSeverityEnum.ERROR: logger.error,
        NotificationSeverityEnum.WARNING: logger.warning,
        NotificationSeverityEnum.INFO: logger.info,
        NotificationSeverityEnum.DEBUG: logger.debug
    }

    def __init__(self, severity, prefix=None):
        self.severity = severity
        self.prefix = prefix

    def send(self, title, comment, severity=None, **kwargs):
        if severity is not None:
            func = self.mapping[severity]
        else:
            func = self.mapping[self.severity]

        if self.prefix is not None:
            if comment is not None:
                func('[{}] {}: {}'.format(self.prefix, title, comment))
            else:
                func('[{}] {}'.format(self.prefix, title))
        else:
            if comment is not None:
                func('{}: {}'.format(title, comment))
            else:
                func('{}'.format(title))