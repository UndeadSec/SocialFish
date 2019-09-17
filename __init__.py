import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import click

from .core.view import head
from .core.cleanFake import cleanFake
from .core.dbsf import init_db_command
from .core.cleanFake import clean_fake_command

from .core.config import DATABASE


head()
login_manager = LoginManager()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping({
        'SEND_FILE_MAX_AGE_DEFAULT': 0,
        'SECRET_KEY': os.urandom(16),
        'SQLALCHEMY_DATABASE_URI': "sqlite:///" + os.path.join(app.instance_path, 'database.sqlite'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
    )

    #inicializa o gerenciador de login
    login_manager.init_app(app)
    #incializa o bootstrap
    Bootstrap(app)
    #inicializa SQLAlchemy
    db.init_app(app)

    # cria diretorio instance ex: mkdir ../instance
    # exist_ok - não levanta uma exceção caso o diretório já exista
    os.makedirs(app.instance_path, exist_ok=True)
    # adicionar comando init_db_command ex: flask init-db
    app.cli.add_command(init_db_command)
    app.cli.add_command(clean_fake_command)

    from .socialfish import socialbp # Blueprint
    app.register_blueprint(socialbp)
    return app