from repository.usersRepo import usersRepo
from middleware.hashPass import hash_password

class usersSrv():
    def __init__(self):
        self.users_repo = usersRepo()

    def getSrv(self, id=0):
        return self.users_repo.selectAllOrById(id)

    def postSrv(self, payload):
        if payload:
            result = self.users_repo.get_by_conditions({
                "email": payload["email"]
            })
            if result and len(result) > 0:
                return "Email already exists"
            else:
                user_data = {
                    "firstname": payload["firstname"],
                    "lastname": payload["lastname"],
                    "email": payload["email"],
                    "password": hash_password(payload["password"])
                }
                return self.users_repo.insert(user_data, payload["rol_id"])

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
            return self.users_repo.update(id, user_data)

    def deleteSrv(self, id):
        if id:
            return self.users_repo.delete(id)
