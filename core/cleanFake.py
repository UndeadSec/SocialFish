import shutil
import os

import click
from flask import current_app
from flask.cli import with_appcontext

def cleanFake():
	templates_path = os.path.join(current_app.root_path, current_app.template_folder)
	try:
		fake_folder = os.path.join(templates_path, 'fake')
		shutil.rmtree(fake_folder)
	except:
		pass


@click.command('clean-fake', help="Clear fake templates")
@with_appcontext
def clean_fake_command():
	"""Clear fake templates"""
	cleanFake()
	click.echo("Clear fake templates completed!")