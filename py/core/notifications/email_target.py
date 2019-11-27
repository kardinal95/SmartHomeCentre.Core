class EmailNotificationTarget:
    def __init__(self, address, theme):
        self.address = address
        self.theme = theme

    def send(self, title, comment, severity=None, **kwargs):
        pass