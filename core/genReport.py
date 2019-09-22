from .. import db
from .. models import Creds
import click

def genReport(subject, user, company, date_range, target):
	date_range = date_range.replace(' ', '')
	date_range = date_range.replace('/','-')
	date_range = date_range.split('_')
	date_start = date_range[0]
	date_end = date_range[1]
	results = db.session.query(Creds.pdate).filter(Creds.pdate >= date_start).filter(Creds.pdate <= date_end).all()
	click.echo(results)