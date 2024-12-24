from flask import Blueprint, render_template
import os

home = Blueprint('home', __name__, template_folder='app/templates/api')

class homeCtrl():

    @home.route('/')
    def Home():
        app_name = os.getenv("APP_NAME")
        app_name_description = os.getenv("APP_NAME_DESCRIPTION")
        return render_template('api/api.html', app_name=app_name, app_name_description=app_name_description)
