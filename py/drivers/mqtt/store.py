class ParameterStorage:
    def __init__(self):
        self.main = dict()

    def add_device(self, uuid):
        if uuid not in self.main.keys():
            self.main[uuid] = dict()

    def add_parameter(self, uuid, name):
        self.add_device(uuid)
        if name not in self.main[uuid].keys():
            self.main[uuid][name] = None

    def update_parameter(self, uuid, pair):
        self.add_device(uuid)
        self.add_parameter(uuid, pair[0])
        if self.main[uuid][pair[0]] != pair[1]:
            self.main[uuid][pair[0]] = pair[1]
            return True
        return False