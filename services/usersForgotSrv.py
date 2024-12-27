from repository.repoSQL import repoSQL

class usersForgotSrv():
    def __init__(self):
        self.result = None
        self.query_service = repoSQL('users_forgot_password', ['id', 'user_id', 'code'])

    def getByIdSrv(self, id):
        return self.query_service.get_by_conditions({
                "user_id": id
            })

    def postSrv(self, payload):
        if not payload:
            raise ValueError("Payload is required")

        user_data = {
            "user_id": payload["user_id"],
            "code": payload["code"]
        }

        user_forgot_exists = self.getByIdSrv(payload["user_id"])

        if user_forgot_exists:
            raise ValueError("User ID match stored user")
        else:
            self.result =self.query_service.insert(user_data)

        return self.result

    def deleteSrv(self, id):
        if id:
            user = self.getByIdSrv(id)
            return self.query_service.delete(user[0]["id"])