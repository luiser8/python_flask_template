from flask import Blueprint, request, jsonify
from middleware.tokenJWTUtils import tokenJWTUtils
from middleware.verifyAuth import authorize
from services.authSrv import authSrv

auth = Blueprint('auth', __name__)

class authCtrl():

    @auth.route('/api/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        payload = { "email": data.get("email"), "password": data.get("password") }
        response = authSrv().loginSrv(payload)
        return jsonify(response), response["status"]

    @auth.route('/api/auth/logout', methods=['POST'])
    @authorize
    def logout():
        response = None
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        response = authSrv().destroySrv(user_id)
        return jsonify(response), response["status"]

    @auth.route('/api/auth/refresh', methods=['POST'])
    @authorize
    def refresh():
        response = None
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        response = authSrv().refreshSrv(user_id)
        return jsonify(response), response["status"]