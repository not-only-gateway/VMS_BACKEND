from flask import request
from api.api import ApiView
from app import app
from app import db
from vm.storage_models import Storage

api = ApiView(class_instance=Storage, identifier_attr='id', relationships=[], db=db)


@app.route('/api/list/storage', methods=['GET'])
def list_storage():
    return api.list(request.args)


@app.route('/api/storage/<e_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/storage', methods=['POST'])
def storage(e_id=None):
    if request.method == 'GET':
        return api.get(entity_id=e_id)
    elif request.method == 'POST':
        return api.post(package=request.json)
    elif request.method == 'PUT':
        return api.put(entity_id=e_id, package=request.json)
    elif request.method == 'DELETE':
        return api.delete(entity_id=e_id)
