from flask_appbuilder import BaseView, expose


class TeamComp(BaseView):

    @expose('/teamcomps/', methods=["GET", "POST"])
    def team_comps(self):
        return