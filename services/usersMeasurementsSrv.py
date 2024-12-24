from flask import flash
from repository.repoSQL import repoSQL

class usersMeasurementsSrv():
    def __init__(self):
        self.query_service = repoSQL('users_measurements', ['id', 'user_id', 'date', 'hour', 'value'])

    def getAllSrv(self):
        return self.query_service.get_all()

    def getByIdSrv(self, id):
        return self.query_service.get_by_id(id)

    def postSrv(self, payload):
        if payload:
            meas_data = {
                'user_id': payload["user_id"],
                "date": payload["date"],
                "hour": payload["hour"],
                "value": payload["value"]
            }
            if "user_id" in payload:
                meas_data["user_id"] = payload["user_id"]

            result = self.query_service.insert(meas_data)
            if result:
                flash('Measurement add')
            else:
                flash('Error at measurement')
            return result

    def putSrv(self, id, payload):
        if payload:
            meas_data = {
                'user_id': payload["user_id"],
                "date": payload["date"],
                "hour": payload["hour"],
                "value": payload["value"]
            }
            if "id" in payload:
                meas_data["id"] = payload["id"]

            result = self.query_service.update(id, meas_data)
            if result:
                flash('Measurement upgrade')
            else:
                flash('Error measurement')
            return result

    def deleteSrv(self, id):
        if id:
            result = self.query_service.delete(id)
            if result:
                flash('Measurement deleted')
            else:
                flash('Error delete measurement')
            return result