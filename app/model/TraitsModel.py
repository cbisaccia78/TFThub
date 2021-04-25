from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import db
from app.custom.functions import write_json, read_json
from app.database.traits import Trait


def create_trait_model():
    return TraitModel(Trait, db.session)


class TraitModel(SQLAInterface):

    @staticmethod
    def export_items(items):
        data = {"traits": []}
        for item in items:
            if not item:
                continue
            trait_data = item.to_json()
            data["traits"].append(trait_data)
        return data

    def export_json(self, items: list):
        data = {"name": "traits", "version": appversion()}
        trait_data = self.export_items(items)
        data.update(trait_data)
        outfile = write_json(data)
        filename = f"Trait-Export.json"
        return outfile, filename

    def import_data(self, data=None):
        if data:
            for trait in data:
                new_trait = Trait.from_dict(trait)
                self.add(new_trait)

    def import_json(self, json_data):
        data = read_json(json_data)
        self.import_data(data)

    @staticmethod
    def get_all():
        return None

