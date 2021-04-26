from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship
from app import db
from app.database.assoc_table import champion_trait
from sqlalchemy_json import MutableJson
import random


class Trait(Model):
    __tablename__ = "trait"
    id = Column(Integer, primary_key=True)
    champions = relationship(
        "Champion",
        secondary=champion_trait,
        back_populates="traits")
    name = Column(String, nullable=False)
    key = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)
    sets = Column(MutableJson)

    def __repr__(self):
        return f"{self.name}"

    def get_champions(self):
        return [champion.name for champion in self.champions]

    @staticmethod
    def add(
        name=None, key=None, type=None, description=None, sets=None
    ):
        trait = Trait(
            name=name,
            key=key,
            type=type,
            description=description,
            sets=sets
        )
        db.session.add(Trait)
        db.session.commit()
        return trait

    def as_dict(self):
        data = {
            'name': self.name,
            'key': self.key,
            'type': self.type,
            'description': self.description,
            'sets': self.sets
        }
        return data

    @staticmethod
    def from_dict(data):
        new_item = Trait(
            name=data.get('name'),
            key=data.get('key'),
            type=data.get('type'),
            description=data.get('description'),
            sets={'sets': data.get('sets')}
        )
        return new_item

    @staticmethod
    def get_fields():
        fields = [
            'name',
            'key',
            'type',
            'description',
            'sets'
        ]
        return fields

    @staticmethod
    def get_all():
        traits = db.session.query(Trait).all()
        return traits

    @staticmethod
    def get_by_type(type):
        traits = db.session.query(Trait).filter_by(type=type).all()
        return traits
