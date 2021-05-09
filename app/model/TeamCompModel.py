from app import db
from app.database.champions import Champion
from app.model.ChampionsModel import ChampionModel
from app.model.TraitsModel import TraitModel
from flask_appbuilder.models.sqla.interface import SQLAInterface


def create_team_comp_model():
    return TeamCompModel(Champion, db.session)


class TeamCompModel(SQLAInterface):

    @staticmethod
    def get_all():
        ChampionModel.
