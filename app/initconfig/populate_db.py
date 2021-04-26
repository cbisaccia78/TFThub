import json
from app import db
from app.database.champions import Champion
from app.model.ChampionsModel import create_champion_model, ChampionModel
from app.model.TraitsModel import create_trait_model, TraitModel


def pop_champs():
    filepath = "conf/champions.json"
    with open(filepath, 'r') as myfile:
        data = myfile.read()
    json_data = json.loads(data)
    datamodel = create_champion_model()
    datamodel.import_data(data=json_data.get("champions"))  # coming in as an array of dicts


def pop_traits():
    filepath = "conf/traits.json"
    with open(filepath, 'r') as myfile:
        data = myfile.read()
    json_data = json.loads(data)
    datamodel = create_trait_model()
    datamodel.import_data(data=json_data.get("traits"))  # coming in as an array of dicts


def run():
    db.create_all()
    pop_traits()
    pop_champs()
    print(Champion.get_all()[0].get_traits())

