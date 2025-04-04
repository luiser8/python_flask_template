from flask import Blueprint, request
from services.authSrv import authSrv

auth = Blueprint('auth', __name__)

class authCtrl():

    @auth.route('/auth/login', methods=['POST'])
    def login():
        payload = { "email": request.form["email"], "password": request.form["password"] }
        return authSrv().loginSrv(payload)
