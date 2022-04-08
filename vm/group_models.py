from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from app import db

class Group(db.Model):
    __tablename__ = 'grupo'

    id = db.Column('codigo_id', db.BigInteger,primary_key=True)
    name = db.Column('nome', db.String, nullable=False, unique=True)
    description = db.Column('descricao', db.String)
    service = db.Column('servico', db.String)
    creation = db.Column('data_criacao', db.DateTime, default=datetime.utcnow)


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
