from middleware.responseHttpUtils import responseHttpUtils
from middleware.timeUtils import timeUtils
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
            result = self.query_service.get_by_conditions({
                "email": payload["email"]
            })
            if result and len(result) > 0:
                return responseHttpUtils().response("Email already exists", 400, None)
            else:
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
                    return responseHttpUtils().response("User added successfully", 201, result)
                else:
                    return responseHttpUtils().response("Error adding user", 400, result)

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
                return "User updated successfully"
            else:
                return "Error updating user"

    def forgotPasswordSrv(self, payload):
        if payload:
            result = self.query_service.get_by_conditions({
                "email": payload
            })
            if result and len(result) > 0 and result[0]["status"] == True:
                exists = self.users_forgot_service.getByIdSrv(result[0]["id"])
                self.code = self.mailer_send_service.sendSrv(result[0]["email"])
                if exists and any(exist["status"] for exist in exists):
                    intime_expired_code = timeUtils().getTime(exists[0]["createdat"])
                    if intime_expired_code is True:
                        self.users_forgot_service.putSrv(exists[0]["id"], {
                            "user_id": result[0]["id"],
                            "code": exists[0]["code"],
                            "status": False
                        })
                        return "Recovery code expired"
                    return "The access code has been sent to your email"
                self.users_forgot_service.postSrv({
                    "user_id": result[0]["id"],
                    "code": self.code
                })
            else:
                return "Email not found"
            return self.code

    def changePasswordSrv(self, payload):
        if payload:
            result = self.query_service.get_by_conditions({
                "email": payload["email"]
            })
            if result and len(result) > 0:
                exists = self.users_forgot_service.getByCodeSrv(payload["code"])
                if exists and any(exist["status"] for exist in exists):
                    intime_expired_code = timeUtils().getTime(exists[0]["createdat"])
                    if intime_expired_code is False:
                        self.users_forgot_service.putSrv(exists[0]["id"], {
                            "user_id": result[0]["id"],
                            "code": payload["code"],
                            "status": False
                        })
                        user_data = {
                            "password": hash_password(payload["newpassword"])
                        }
                        self.query_service.update(result[0]["id"], user_data)
                        return "Recovery password changed"
                    return "Recovery code not expired"
                else :
                    return "Recovery code not found"
            else:
                return "Email not found"

    def deleteSrv(self, id):
        if id:
            result = self.query_service.delete(id)
            if result:
                return "User successfully deleted"
            else:
                return "User deleted error"