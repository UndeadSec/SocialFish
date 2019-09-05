from flask import Flask
import click

def create_app():
    app = Flask(__name__)

    return app