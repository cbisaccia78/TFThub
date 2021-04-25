import requests
import json

from app.model.HardwareModel import create_hardware_model


def pop_champs():
    filepath = "conf/champions.json"
    with open(filepath, 'r') as myfile:
        data = myfile.read()
    json_data = json.loads(data)
    datamodel = create_hardware_model()
    datamodel.import_data(data=json_data.get("champions"))

def run(tft_version, updated):
    if not updated:
        holder = {
            "name": "champions",
            "version": "4.5",
            "champions": [

            ]
        }
        r = requests.get("https://tftactics.gg/champions")
        with open('conf/champions.json', 'w+') as myfile:
            print('put the valeus into the file')

