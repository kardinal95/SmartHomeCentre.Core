import enum


class NotificationSeverityEnum(enum.Enum):
    CRITICAL = enum.auto(),
    ERROR = enum.auto(),
    WARNING = enum.auto(),
    INFO = enum.auto(),
    DEBUG = enum.auto()


class NotificationTargetTypeEnum(enum.Enum):
    log = enum.auto(),
    email = enum.auto()


class NotificationSrv:
    def __init__(self):
        self.targets = list()

    def send(self, title, comment=None, severity=None, **kwargs):
        for target in self.targets:
            target.send(title, comment, severity, **kwargs)

    def add_target(self, target):
        self.targets.append(target)
