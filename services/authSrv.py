from repository.authRepo import authRepo
from middleware.hashPass import hash_password

class authSrv:
    def __init__(self):
        self.auth_repo = authRepo()

    def loginSrv(self, payload):
        if payload:
            email = payload["email"]
            password = hash_password(payload["password"])
            result = self.auth_repo.selectLogin(email, password)
            if result:
                return {"message": "Login successful", "user_id": result}
            else:
                return {"message": "User not found"}
