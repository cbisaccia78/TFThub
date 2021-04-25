from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import db
from app.database.traits import Trait


def create_trait_model():
    return TraitModel(Trait, db.session)


class TraitModel(SQLAInterface):

    @staticmethod
    def export_items(items):
        return

    def export_csv(self, items: list):
        return

    def export_json(self, items: list):
        return

    def import_data(self, data=None):
        return

    def import_json(self, json_data):
        return

    @staticmethod
    def get_all():
        return None