
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask import request
from flask import jsonify
import csv, io, json
import re

import env

AUTH_KEY = 'chave-auth'

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = env.DATABASE + '://' + env.USER + ':' + env.PASSWORD + '@' + env.HOST_NAME + '/' + env.DATABASE_NAME
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
from vm.storage_models import Storage
import vm.storage_views
from vm.group_models import Group
import vm.group_views
from vm.models import HostVM, VM, HardDrive, NetworkAdapter
import vm.views


def contains(l, f):
    for x in l:
        if f(x):
            return True
    return False


def find(arr, compare):
    res = None
    for i in arr:
        if compare(i) and res is None:
            res = i

    return res


@app.route('/api/load', methods=['POST'])
def load():
    if request.headers.get('authorization', None) == AUTH_KEY:
        try:
            decoded = request.data.decode('latin-1').replace("'", '"')
        except UnicodeDecodeError:
            decoded = request.data.decode('utf8').replace("'", '"')

        try:
            data = json.loads(decoded)

        except json.JSONDecodeError:
            data = None


        if data is not None:
            host_m = HostVM.query.get(data.get('CsName', None))
            disk_size = data.get('Disk', [])
            if len(disk_size) > 0:
                disk_size = disk_size[0].get('Size', 0)
            else:
                disk_size = 0

            if host_m is None:
                HostVM({
                    "name": data.get('CsName', None),
                    "cores": data.get("CsNumberOfLogicalProcessors", 0) / 2,
                    "threads": data.get("CsNumberOfLogicalProcessors", None),
                    "ram": data.get("OsTotalVisibleMemorySize", None),
                    "disk": disk_size
                })
            else:

                host_m.update({
                    "name": data.get('CsName', None),
                    "cores": data.get("CsNumberOfLogicalProcessors", 0) / 2,
                    "threads": data.get("CsNumberOfLogicalProcessors", None),
                    "ram": data.get("OsTotalVisibleMemorySize", None),
                    "disk": disk_size
                })

            for vm in data.get('VMs', {}).get('value', []):
                current = VM.query.get(vm.get('VMId'))
                date_regex = re.search(r'\(([0-9]+)\)', vm.get('CreationTime'))
                network_ad = vm.get('NetworkAdapters')
                if len(network_ad) > 0:
                    network_ad = network_ad[0]
                else:
                    network_ad = {"IPAddresses": None, "MacAddress": None}
                obj = {
                    'id': vm.get('VMId', None),
                    'name': vm.get('Name', None),
                    'created_on': date_regex.group(1),
                    'description': vm.get('Notes', None),

                    'physical_host': vm.get('ComputerName', None),
                    'path': vm.get('Path', None),

                    'cores': vm.get('ProcessorCount', None),
                    'ram': vm.get('MemoryAssigned', 0),
                    # 'operating_system': vm.get('VMId', None),
                    'up_time_days': vm.get('Uptime', {}).get('Days', 0),
                    'up_time_hours': vm.get('Uptime', {}).get('Hours', 0),

                    'total_days': vm.get('Uptime', {}).get('TotalDays', 0),
                    'total_hours': vm.get('Uptime', {}).get('TotalHours', 0),
                    'status_description': vm.get('PrimaryStatusDescription'),
                    'disabled': vm.get('IsDeleted'),
                    "host": data.get('CsName', None),
                    "ip": network_ad.get('IPAddresses', None),
                    "mac": network_ad.get('MacAddress', None)
                }
                if current is None:
                    VM(obj)
                else:
                    current.update(obj)

                for hdd in vm.get('HardDrives', []):
                    hd = HardDrive.query.get(hdd.get('Id', None))
                    hd_data = hdd.get('Data', [])
                    if len(hd_data) > 0:
                        hd_data = hd_data[0]
                    else:
                        hd_data = {"Size": 0, "FileSize": 0}
                    obj = {
                        'id': hdd.get('Id', None),
                        'name': hdd.get('ComputerName', None),
                        'path': hdd.get('Path', None),
                        'space': hd_data.get("Size", 0),
                        'used_space': hd_data.get("FileSize", 0),
                        'vm': vm.get('VMId', None)
                    }
                    if hd is not None:
                        hd.update(obj)
                    else:
                        HardDrive(obj)

                for nwa in vm.get('NetworkAdapters'):
                    nw = NetworkAdapter.query.get(nwa.get('Id', None))
                    obj = {

                        'id': nwa.get('Id', None),
                        'name': nwa.get('Name', None),

                        'mac_address': nwa.get('MacAddress', None),
                        'ip_address': nwa.get('IPAddresses', None),
                        'pool_name': nwa.get('PoolName', None),

                        'status_description': nwa.get('StatusDescription', None),
                        'vm': vm.get('VMId', None)
                    }
                    if nw is not None:
                        nw.update(obj)
                    else:
                        NetworkAdapter(obj)

            return jsonify({'status': 'success', 'description': 'ok', 'code': 200}), 200
        else:
            return jsonify({'status': 'error', 'description': 'Data not valid', 'code': 400}), 400
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1025)

