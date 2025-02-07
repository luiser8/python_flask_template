from functools import wraps
from flask import request, jsonify, g
import jwt
import os
from services.usersAuth import usersAuthSrv
from middleware.responseHttpUtils import responseHttpUtils

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        users_auth_service = usersAuthSrv()
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split()[1]

        if not token:
            jsonify(responseHttpUtils().response("Not authorized", 401, None)), 401

        try:
            secret_key = os.getenv("SECRET_KEY")
            secret_key_algorithm = os.getenv("ALGORITHM")
            data = jwt.decode(jwt=token, key=secret_key, algorithms=[secret_key_algorithm])
            g.user = data

            if not users_auth_service.getByIdSrv(g.user["id"]):
                return jsonify(responseHttpUtils().response("Not authorized", 401, None)), 401

        except jwt.ExpiredSignatureError:
            return jsonify(responseHttpUtils().response("Token expired", 401, None)), 401
        except jwt.InvalidTokenError:
            jsonify(responseHttpUtils().response("Invalid token", 401, None)), 401

        return f(*args, **kwargs)

    return decorated_function
