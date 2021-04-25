from flask_appbuilder import Model
from app import db
from sqlalchemy import Column, Integer, ForeignKey, Table

champion_trait = Table('association', db.metadata,
    Column('champion_id', Integer, ForeignKey('champion.id')),
    Column('trait_id', Integer, ForeignKey('trait.id'))
)
