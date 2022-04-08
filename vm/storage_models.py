from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from app import db

class Storage(db.Model):
    __tablename__ = 'volume'

    id = db.Column('codigo_id', db.BigInteger,primary_key=True)
    name = db.Column('nome', db.String, nullable=False, unique=True)
    pure_id = db.Column('pure_id', db.String, nullable=False, unique=True)

    space = db.Column('espaco', db.BigInteger, nullable=False, default=0)
    used_space = db.Column('espaco_usado', db.BigInteger, nullable=False, default=0)

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
