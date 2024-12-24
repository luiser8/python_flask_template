from flask import flash
from repository.repoSQL import repoSQL

class usersAuthSrv():
    def __init__(self):
        self.result = None
        self.query_service = repoSQL('users_auth', ['id', 'user_id', 'access_token', 'refresh_token'])

    def getByIdSrv(self, id):
        return self.query_service.get_by_conditions({
                "user_id": id
            })

    def postSrv(self, payload):
        if not payload:
            raise ValueError("Payload is required")

        user_data = {
            "user_id": payload["user_id"],
            "access_token": payload["access_token"],
            "refresh_token": payload["refresh_token"]
        }

        user_exists = self.getByIdSrv(payload["user_id"])

        if user_exists:
            if payload["user_id"] == user_exists[0]["user_id"]:
                self.result =self.query_service.update(user_exists[0]["id"], user_data)
            else:
                raise ValueError("User ID does not match stored user")
        else:
            self.result =self.query_service.insert(user_data)

        return self.result

    def deleteSrv(self, id):
        if id:
            user = self.getByIdSrv(id)
            result = self.query_service.delete(user[0]["id"])
            if result:
                flash('Tokens de Usuario eliminado exitosamente')
            else:
                flash('Error al eliminar los tokens del usuario')
            return result