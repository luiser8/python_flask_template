class responseHttpUtils:
    def __init__(self):
        self.message = None
        self.status = None
        self.data = None

    def response(self, message = None, status = None, data = None):
        self.message = message
        self.status = status
        self.data = data

        if (self.message is None and self.status is None and self.data is not None):
            return self.data

        if (self.data is None and self.status is None and self.message is not None):
            return self.message

        if (self.data is None and self.message is None and self.status is not None):
            return self.status

        return {
            "message": self.message,
            "status": self.status,
            "data": self.data
        }