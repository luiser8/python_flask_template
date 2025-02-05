import os
from middleware.tokenJWTUtils import tokenJWTUtils
from repository.repoSQL import repoSQL
from middleware.hashPass import hash_password
from services.usersAuth import usersAuthSrv

class authSrv:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.secret_key_algorithm = os.getenv("ALGORITHM")
        self.expires_in = int(os.getenv("EXPIRES_IN"))
        self.query_service = repoSQL('users', ['id', 'email', 'firstname', 'lastname', 'status'])
        self.users_auth_service = usersAuthSrv()
        self.generate_token = tokenJWTUtils()

    def loginSrv(self, payload):
        if payload:
            email = payload["email"]
            password = hash_password(payload["password"])
            result = self.query_service.get_by_conditions({
                "email": email,
                "password": password
            })
            if result:
                tokens = self.generate_token.generate(result)
                if tokens and result:
                    self.users_auth_service.postSrv({
                        "user_id": result[0]["id"],
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"]
                    })
                    return tokens
            else:
                return "User not found"

    def destroySrv(self, user_id):
        if user_id:
            return self.users_auth_service.deleteSrv(user_id)

    def refreshSrv(self, user_id):
        if user_id:
            result = self.query_service.get_by_id(user_id)
            if result:
                tokens = self.generate_token.generate(result)
                if tokens and result:
                    self.users_auth_service.postSrv({
                        "user_id": result[0]["id"],
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"]
                    })
                return tokens