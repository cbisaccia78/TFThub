from app import db
from app.database.champions import Champion
from app.model.OriginsModel import create_origin_model
from app.model.ClassesModel import create_classe_model
from flask_appbuilder.models.sqla.interface import SQLAInterface


def create_champion_model():
    return ChampionModel(Champion, db.session)


class ChampionModel(SQLAInterface):
    origin_datamodel = create_origin_model()
    classes_datamodel = create_classe_model()


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

