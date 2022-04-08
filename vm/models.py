from sqlalchemy.exc import SQLAlchemyError

from app import db

class HostVM(db.Model):
    __tablename__ = 'host'

    name = db.Column('nome', db.String, nullable=False, primary_key=True)
    cores = db.Column('nucleos', db.Integer, nullable=False)
    threads = db.Column('threads', db.Integer, nullable=False)
    disk = db.Column('disco', db.BigInteger, nullable=False)
    ram = db.Column('ram', db.BigInteger, nullable=False)
    cluster = db.Column('cluster', db.String)
    storage = db.Column('volume', db.BigInteger, db.ForeignKey('volume.codigo_id', ondelete='CASCADE'))


    def update(self, data):
        try:
            for key in data.keys():
                setattr(self, key, data.get(key, None))
            db.session.commit()
        except SQLAlchemyError:
            pass

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()


class VM(db.Model):
    __tablename__ = 'vm'

    id = db.Column('codigo_id', db.String, primary_key=True)
    name = db.Column('nome', db.String, nullable=False)
    path = db.Column('caminho', db.String, nullable=False)
    created_on = db.Column('criado_em', db.BigInteger, nullable=False)
    description = db.Column('descricao', db.String)

    physical_host = db.Column('host_fisico', db.String, nullable=False)

    cores = db.Column('nucleos', db.Integer, nullable=False)
    ram = db.Column('ram', db.BigInteger, nullable=False)
    operating_system = db.Column('sistema_operacional', db.String)

    status_description = db.Column('status', db.String)

    up_time_days = db.Column('ativo_dias', db.Integer, nullable=True, default=0)
    up_time_hours = db.Column('ativo_horas', db.Integer, nullable=True, default=0)

    total_days = db.Column('total_ativo_dias', db.Integer, nullable=True, default=0)
    total_hours = db.Column('total_ativo_horas', db.Integer, nullable=True, default=0)
    disabled = db.Column('desativada', db.Boolean, nullable=True, default=False)
    ip = db.Column('ip', db.String)
    mac = db.Column('mac', db.String)

    group = db.Column('grupo', db.ForeignKey('grupo.codigo_id', ondelete='CASCADE'))
    host = db.Column('host_p', db.ForeignKey('host.nome', ondelete='CASCADE'))

    def update(self, data):
        try:
            for key in data.keys():
                setattr(self, key, data.get(key, None))
            db.session.commit()
        except SQLAlchemyError:
            pass

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()


class HardDrive(db.Model):
    __tablename__ = 'disco_rigido'

    id = db.Column('codigo_id', db.String, primary_key=True)
    name = db.Column('nome', db.String, nullable=False)
    path = db.Column('caminho', db.String, nullable=False)
    space = db.Column('espaco', db.BigInteger)
    used_space = db.Column('espaco_usado', db.BigInteger)

    vm = db.Column('vm', db.ForeignKey('vm.codigo_id', ondelete='CASCADE'), nullable=False)

    def update(self, data):
        try:
            for key in data.keys():
                setattr(self, key, data.get(key, None))
            db.session.commit()
        except SQLAlchemyError:
            pass

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()


class NetworkAdapter(db.Model):
    __tablename__ = 'adaptador_rede'

    id = db.Column('codigo_id', db.String, primary_key=True)
    name = db.Column('nome', db.String, nullable=False)

    mac_address = db.Column('mac', db.String)
    ip_address = db.Column('ip', db.String)
    pool_name = db.Column('pool', db.String)

    vm = db.Column('vm', db.ForeignKey('vm.codigo_id', ondelete='CASCADE'), nullable=False)
    status_description = db.Column('status', db.String)

    def update(self, data):
        try:
            for key in data.keys():
                setattr(self, key, data.get(key, None))
            db.session.commit()
        except SQLAlchemyError:
            pass

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()
