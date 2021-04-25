from flask_appbuilder import Model
from app import db
from sqlalchemy import Column, Integer, ForeignKey, Table

champion_classe = Table('association', db.metadata,
    Column('champion_id', Integer, ForeignKey('champion.id')),
    Column('classe_id', Integer, ForeignKey('classe.id'))
)

champion_origin = Table('association', db.metadata,
    Column('champion_id', Integer, ForeignKey('champion.id')),
    Column('origin_id', Integer, ForeignKey('origin.id'))
)