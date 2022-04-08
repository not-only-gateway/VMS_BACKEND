from flask import request, jsonify
from api.api import ApiView
from app import app
from app import db
from vm.models import VM, NetworkAdapter, HardDrive, HostVM

api = ApiView(class_instance=VM, identifier_attr='id', relationships=[{
    "key": "host",
    "instance": HostVM
}], db=db)
apiNW = ApiView(class_instance=NetworkAdapter, identifier_attr='id', relationships=[{
    "key": "vm",
    "instance": VM
}], db=db)
apiHD = ApiView(class_instance=HardDrive, identifier_attr='id', relationships=[{
    "key": "vm",
    "instance": VM
}], db=db)

apiH = ApiView(class_instance=HostVM, identifier_attr='name', relationships=[], db=db)

@app.route('/api/host/<e_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/host', methods=['POST'])
def host(e_id=None):
    if request.method == 'GET':
        return apiH.get(entity_id=e_id)
    elif request.method == 'PUT':
        return apiH.put(entity_id=e_id, package=request.json)
@app.route('/api/list/host', methods=['GET'])
def list_host():
    return apiH.list(data=request.args)


@app.route('/api/vm/<e_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/vm', methods=['POST'])
def vm(e_id=None):
    if request.method == 'GET':
        return api.get(entity_id=e_id)
    elif request.method == 'PUT':
        return api.put(entity_id=e_id, package=request.json)


@app.route('/api/list/vm', methods=['GET'])
def list_vm():
    return api.list(data=request.args)




@app.route('/api/rede_vm/<id_vm>', methods=['GET'])
def rede_vm(id_vm=None):
    return apiNW.get(id_vm)


@app.route('/api/disco_vm/<id_vm>', methods=['GET'])
def disco_vm(id_vm=None):
    return apiHD.get(id_vm)


@app.route('/api/list/rede_vm/<id_vm>', methods=['GET'])
def rede_vm_list(id_vm=None):
    print(id_vm)
    return apiNW.list(request.args, [{
        'key': 'vm',
        'value': id_vm,
        'type': 'object',

    }])


@app.route('/api/list/disco_vm/<id_vm>', methods=['GET'])
def disco_vm_list(id_vm=None):
    return apiHD.list(request.args, [{
        'key': 'vm',
        'value': id_vm,
        'type': 'object'
    }])
