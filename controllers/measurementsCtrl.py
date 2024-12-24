from flask import Blueprint, request, jsonify
from middleware.verifyAuth import authorize
from services.usersMeasurementsSrv import usersMeasurementsSrv
from middleware.tokenJWTUtils import tokenJWTUtils

measurements = Blueprint('measurements', __name__)

class publicationsCtrl():
    @measurements.route('/api/measurements/get', methods=['GET'])
    @authorize
    def getAll():
        return jsonify(usersMeasurementsSrv().getAllSrv())

    @measurements.route('/api/measurements/get/<int:id>', methods=['GET'])
    @authorize
    def getById(id):
        return jsonify(usersMeasurementsSrv().getByIdSrv(id))

    @measurements.route('/api/measurements/post', methods=['POST'])
    @authorize
    def post():
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        data = request.get_json()
        payload = { "user_id": user_id, "date": data.get("date"), "hour": data.get("hour"), "value": data.get("value") }
        save = usersMeasurementsSrv().postSrv(payload)
        if save:
            return jsonify(save), 201
        else:
            return jsonify(save), 500

    @measurements.route('/api/measurements/put/<int:id>', methods=['PUT'])
    @authorize
    def put(id):
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        data = request.get_json()
        payload = { "user_id": user_id, "date": data.get("date"), "hour": data.get("hour"), "value": data.get("value") }
        save = usersMeasurementsSrv().putSrv(id, payload)
        if save:
            return jsonify(save), 200
        else:
            return jsonify(save), 500

    @measurements.route('/api/measurements/delete/<int:id>', methods=['DELETE'])
    @authorize
    def delete(id):
        save = usersMeasurementsSrv().deleteSrv(id)
        if save:
            return jsonify(save), 200
        else:
            return jsonify(save), 500