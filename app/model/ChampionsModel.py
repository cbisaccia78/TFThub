from app import db
from app.custom.functions import write_json, read_json
from app.model.TraitsModel import create_trait_model
from flask_appbuilder.models.sqla.interface import SQLAInterface


def create_champion_model():
    return ChampionModel(Champion, db.session)


class ChampionModel(SQLAInterface):
    trait_datamodel = create_trait_model()


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
        for champion in data.get('champions'):
            self.origin_datamodel.import_data(champion=champion, data=champion.get('origins'))
            self.classes_datamodel.import_data(champion=champion, data=champion.get('classes'))
        self.import_data(data.get('champions'))

    @staticmethod
    def get_all():
        return None

