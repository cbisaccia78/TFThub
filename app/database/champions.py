from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app import db
from app.database.assoc_table import champion_trait
from app.database.traits import Trait
from sqlalchemy_json import MutableJson


class Champion(Model):
    __tablename__ = "champions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    champion_id = Column(String, nullable=False)
    traits = relationship(
        "Trait",
        secondary=champion_trait,
        back_populates="champions")
    cost = Column(Integer)
    abilities = Column(MutableJson)

    def __repr__(self):
        return f"{self.name}"

    def get_traits(self):
        return [trait.name for trait in self.traits]

    def get_origins(self):
        if self.traits:
            return [trait.name for trait in self.traits if trait.type == 'origin']

    def get_classes(self):
        if self.classes:
            return [trait.name for trait in self.traits if trait.type == 'classe']

    @staticmethod
    def add(
            name=None, champion_id=None, cost=None, ability=None
    ):
        champion = Champion(
            name=name,
            champion_id=champion_id,
            cost=cost,
            ability=ability
        )
        db.session.add(champion)
        db.session.commit()
        return champion

    def as_dict(self):
        data = {
            'name': self.name,
            'champion_id': self.champion_id,
            'cost': self.cost,
            'abilities': self.abilities
        }
        return data

    @staticmethod
    def from_dict(data):
        new_item = Champion(
            name=data.get('name'),
            champion_id=data.get('champion_id'),
            cost=data.get('cost'),
            abilities=data.get('abilities')
        )
        return new_item

    @staticmethod
    def get_fields():
        fields = [
            'name',
            'champion_id',
            'cost',
            'abilities'
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
