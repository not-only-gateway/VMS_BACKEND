from flask import request
from api.api import ApiView
from app import app
from app import db
from vm.group_models import Group

api = ApiView(class_instance=Group, identifier_attr='id', relationships=[], db=db)


@app.route('/api/list/group', methods=['GET'])
def list_group():
    return api.list(request.args)


@app.route('/api/group/<e_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/group', methods=['POST'])
def group(e_id=None):
    if request.method == 'GET':
        return api.get(entity_id=e_id)
    elif request.method == 'POST':
        return api.post(package=request.json)
    elif request.method == 'PUT':
        return api.put(entity_id=e_id, package=request.json)
    elif request.method == 'DELETE':
        return api.delete(entity_id=e_id)
