from flask_appbuilder import BaseView, expose, ModelView

from app.model.ChampionsModel import create_champion_model
from app.model.TeamCompModel import create_team_comp_model
from app.model.TraitsModel import create_trait_model


class TeamComp(ModelView):
    datamodel = create_team_comp_model()
    trait_datamodel = create_trait_model()
    champion_datamodel = create_champion_model()
    @expose('/teamcomps/', methods=["GET", "POST"])
    def team_comps(self):
        return