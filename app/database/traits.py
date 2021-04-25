from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app import db
from app.database.assoc_table import champion_trait
from sqlalchemy_json import MutableJson
import random


class Trait(Model):
    __tablename__ = "traits"
    id = Column(Integer, primary_key=True)
    champions = relationship(
        "Champion",
        secondary=champion_trait,
        back_populates="traits")
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)
