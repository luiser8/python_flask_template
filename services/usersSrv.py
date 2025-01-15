from flask import flash
from repository.repoSQL import repoSQL
from middleware.hashPass import hash_password
from services.usersForgotSrv import usersForgotSrv
from services.mailerSendSrv import mailerSendSrv

class usersSrv():
    def __init__(self):
        self.query_service = repoSQL('users', ['id', 'firstname', 'lastname', 'email', 'password', 'status'])
        self.mailer_send_service = mailerSendSrv()
        self.users_forgot_service = usersForgotSrv()
        self.code = None

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

    def forgotPasswordSrv(self, payload):
        if payload:
            result = self.query_service.get_by_conditions({
                "email": payload
            })
            if result and len(result) > 0 and result[0]["status"]:
                self.code = self.mailer_send_service.sendSrv(result[0]["email"])
                exists = self.users_forgot_service.getByIdSrv(result[0]["id"])
                if exists:
                    self.users_forgot_service.putSrv(exists[0]["id"], {
                        "user_id": result[0]["id"],
                        "code": self.code,
                        "status": False
                    })
                    return "El código de acceso ha sido enviado a su correo electrónico"
                self.users_forgot_service.postSrv({
                    "user_id": result[0]["id"],
                    "code": self.code
                })
                return self.code

    def deleteSrv(self, id):
        if id:
            result = self.query_service.delete(id)
            if result:
                flash('Usuario eliminado exitosamente')
            else:
                flash('Error al eliminado el usuario')
            return result