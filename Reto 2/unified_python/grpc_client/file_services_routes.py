from flask import Blueprint
from flask_restful import Api
from resources import FilesFindResource, FilesListResource

file_services_bp = Blueprint('file_services', __name__)
api = Api(file_services_bp)

api.add_resource(FilesListResource, '/list')
api.add_resource(FilesFindResource, '/find/<string:name>')