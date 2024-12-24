from flask import Blueprint, request, jsonify
from services.usersSrv import usersSrv
from middleware.verifyAuth import authorize

users = Blueprint('users', __name__)

class usersCtrl():
    @users.route('/api/users/get', methods=['GET'])
    @authorize
    def getAll():
        return jsonify(usersSrv().getAllSrv())

    @users.route('/api/users/get/<int:id>', methods=['GET'])
    @authorize
    def getById(id):
        return jsonify(usersSrv().getByIdSrv(id))

    @users.route('/api/users/post', methods=['POST'])
    @authorize
    def post():
        data = request.get_json()
        payload = { "firstname": data.get("firstname"), "lastname": data.get("lastname"), "email": data.get("email"), "password": data.get("password") }
        save = usersSrv().postSrv(payload)
        if save:
            return jsonify(save), 201
        else:
            return jsonify(save), 500

    @users.route('/api/users/put/<int:id>', methods=['PUT'])
    @authorize
    def put(id):
        data = request.get_json()
        payload = { "firstname": data.get("firstname"), "lastname": data.get("lastname"), "email": data.get("email"), "password": data.get("password"), "status": data.get("status") }
        save = usersSrv().putSrv(id, payload)
        if save:
            return jsonify(save), 200
        else:
            return jsonify(save), 500

    @users.route('/api/users/delete/<int:id>', methods=['DELETE'])
    @authorize
    def delete(id):
        save = usersSrv().deleteSrv(id)
        if save:
            return jsonify(save), 200
        else:
            return jsonify(save), 500