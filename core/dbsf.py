import os
import sqlite3

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from .genToken import genToken, genQRCode
from .cleanFake import cleanFake

def initDB( username, password, drop_all):
    """
    param username: administrator username
    param password: administrator password
    """
    from .. import db
    from ..models import User, SocialFish
    
    if drop_all:
        "Drop all tables"
        db.drop_all()

    #Create all tables
    db.create_all()
    
    password_hash = generate_password_hash(password)
    admin = User(username=username, password=password)

    token = genToken()
    social_fish = SocialFish(clicks=0, attacks=0, token=token)

    db.session.add_all([admin, social_fish])
    db.session.commit()

    genQRCode(token)


@click.command('init-db', help="flask init-db -u username -p password")
@click.option('-u', '--username')
@click.option('-p', '--password')
@click.option('--drop-all', default=True)
@with_appcontext
def init_db_command(username, password, drop_all):
    DATABASE = current_app.config['SQLALCHEMY_DATABASE_URI']
    click.echo("Initializing database... %s" %DATABASE)
    if not username or not password:
        click.echo("Define a username and password from administrator!. Initializing database failed!")
    else:
        initDB(username, password, drop_all)
        click.echo("Database initialized!")
