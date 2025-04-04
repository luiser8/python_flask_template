from flask import Blueprint, redirect, render_template, request
from services.usersSrv import usersSrv

users = Blueprint('users', __name__)

class usersCtrl():
    @users.route('/users/all', methods=['GET'])
    def getAll():
        users = usersSrv().getSrv()
        return render_template('users/index.html', users=users)

    @users.route('/users/id/<int:id>', methods=['GET'])
    def getById(id):
        return render_template("/users/userDetail.html", user=usersSrv().getSrv(id))

    @users.route('/users/new', methods=['GET'])
    def new():
        return render_template('users/newUser.html')

    @users.route('/users/save', methods=['POST'])
    def post():
        payload = { "rol_id": request.form['rol_id'], "firstname": request.form['firstname'], "lastname": request.form['lastname'], "email": request.form['email'], "password": request.form['password'] }
        usersSrv().postSrv(payload)
        return redirect("/users/all")

    @users.route('/users/update/<int:id>', methods=['POST'])
    def put(id):
        payload = { "rol_id": request.form['rol_id'], "firstname": request.form['firstname'], "lastname": request.form['lastname'], "email": request.form['email'], "password": request.form['password'], "status": request.form["status"] }
        if id and payload:
            usersSrv().putSrv(id, payload)
        return redirect("/users/all")

    @users.route('/users/delete/<int:id>', methods=['GET'])
    def delete(id):
        if id:
            usersSrv().deleteSrv(id)
        return redirect("/users/all")
