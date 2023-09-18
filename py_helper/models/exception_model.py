class ExceptionModel(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def print(self):
        print(self.message)