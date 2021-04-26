import logging

import click
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views


@app.cli.command("initdb")
def initdb():
    from app.initconfig import populate_db
    errors = populate_db.run()
    if not errors:
        click.echo(
            click.echo(click.style(f"Populate lookup tables. Done.", fg="green"))
        )
    else:
        click.echo(
            click.echo(click.style(f"Populate lookup finished with errors.", fg="red"))
        )

