from app import db
from app.custom.functions import write_json, read_json
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
        data = {"champions": []}
        for item in items:
            if not item:
                continue
            champion_data = item.to_json()
            data["champions"].append(champion_data)
        return data

    def export_json(self, items: list):
        data = {"name": "champions", "version": appversion()}
        hardware_data = self.export_items(items)
        data.update(hardware_data)
        outfile = write_json(data)
        filename = f"Champion-Export.json"
        return outfile, filename

    def import_data(self, data=None):
        if data:
            for champion in data:
                new_champ = Champion.from_dict(champion)
                self.add(new_champ)

    def import_json(self, json_data):
        data = read_json(json_data)
        self.origin_datamodel.import_data(data=data.get('origins'))
        self.classes_datamodel.import_data(data=data.get('classes'))

    @staticmethod
    def get_all():
        return None

