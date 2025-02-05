class responseHttpUtils:
    def __init__(self):
        self.message = None
        self.status = None
        self.data = None

    def response(self, message, status, data):
        self.message = message
        self.status = status
        self.data = data

        return {
            "message": self.message,
            "status": self.status,
            "data": self.data
        }