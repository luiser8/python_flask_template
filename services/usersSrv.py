from flask import flash
from repository.repoSQL import repoSQL
from middleware.hashPass import hash_password

class usersSrv():
    def __init__(self):
        self.query_service = repoSQL('users', ['id', 'firstname', 'lastname', 'email', 'password', 'status'])

    def getAllSrv(self):
        return self.query_service.get_all()

    def getByIdSrv(self, id):
        return self.query_service.get_by_id(id)

    def postSrv(self, payload):
        if payload:
            user_data = {
                "firstname": payload["firstname"],
                "lastname": payload["lastname"],
                "email": payload["email"],
                "password": hash_password(payload["password"])
            }
            if "id" in payload:
                user_data["id"] = payload["id"]
            if "status" in payload:
                user_data["status"] = payload["status"]
            result = self.query_service.insert(user_data)
            if result:
                flash('Usuario agregada exitosamente')
            else:
                flash('Error al agregar el usuario')
            return result

    def putSrv(self, id, payload):
        if payload:
            user_data = {
                "firstname": payload["firstname"],
                "lastname": payload["lastname"],
                "email": payload["email"],
                "password": hash_password(payload["password"])
            }
            if "id" in payload:
                user_data["id"] = payload["id"]
            if "status" in payload:
                user_data["status"] = payload["status"]
            result = self.query_service.update(id, user_data)
            if result:
                flash('Usuario actualizada exitosamente')
            else:
                flash('Error al actualizar el usuario')
            return result

    def deleteSrv(self, id):
        if id:
            result = self.query_service.delete(id)
            if result:
                flash('Usuario eliminado exitosamente')
            else:
                flash('Error al eliminado el usuario')
            return result