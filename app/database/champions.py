from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app import db
from app.database.assoc_table import champion_classe, champion_origin
from app.database.origins import Origin
from app.database.classes import Classe
from sqlalchemy_json import MutableJson
import random


class Champion(Model):
    __tablename__ = "champions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    origins = relationship(
        "Origin",
        secondary=champion_origin,
        back_populates="champions")
    classes = relationship(
        "Classe",
        secondary=champion_classe,
        back_populates="champions")
    cost = Column(Integer)
    abilities = Column(MutableJson)

    def __repr__(self):
        return f"{self.name}"

    def get_origins(self):
        if self.origins:
            return [origin.name for origin in self.origins]

    def get_classes(self):
        if self.classes:
            return [classe.name for classe in self.classes]

    @staticmethod
    def add(
            origin_ids=None,
            classes_id=None,
            name=None,
            asset_tag=None,
            info=None,
    ):
        # add a hardware
        champion = Champion(

        )
        db.session.add(champion)
        db.session.commit()
        return champion

    def as_dict(self):
        data = {
            'name': self.name,
            'origins': self.get_origins(),
            'classes': self.get_classes(),
            'cost': self.cost,
            'abilities': self.abilities
        }
        return data

    @staticmethod
    def csv_to_dict(row):
        data = {
        }
        return data

    @staticmethod
    def from_dict(data):
        new_item = Champion(
        )
        return new_item

    @staticmethod
    def get_fields():
        fields = [

        ]
        return fields

    @staticmethod
    def get_all():
        champions = db.session.query(Champion).all()
        return champions

    @staticmethod
    def get(champion_id):
        champ = db.session.query(Champion).filter_by(id=champion_id).first()
        return champ

    @staticmethod
    def get_by_origin(origin_id):
        q = db.session.query()
        return (
            db.session.query(Champion)
                .filter_by(origin_id=origin_id)
                .all()
        )
