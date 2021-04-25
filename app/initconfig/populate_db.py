import json

from app.model.ChampionsModel import create_champion_model
from app.model.TraitsModel import create_trait_model


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


def run(tft_version, updated):
    if not updated:
       print('to_be_updated')
    pop_traits()
    pop_champs()


