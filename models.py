from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class SocialFish(db.Model):
    __tablename__ = 'socialfish'
    id = db.Column(db.Integer, primary_key=True)
    clicks = db.Column(db.Integer, nullable=False)
    attacks = db.Column(db.Integer, nullable=False)
    token = db.Column(db.Text, nullable=False)


class Creds(db.Model):
    __tablename__ = 'creds'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    jdoc = db.Column(db.Text, nullable=False)
    pdate = db.Column(db.Text, nullable=False)
    browser = db.Column(db.Text, nullable=False)
    bversion = db.Column(db.Text, nullable=False)
    platform = db.Column(db.Text, nullable=False)
    rip = db.Column(db.Text, nullable=False)


class Sfmail(db.Model):
    __tablename__ = 'sfmail'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    smtp = db.Column(db.Text, nullable=False)
    port = db.Column(db.Text, nullable=False)


# Relacionamento de muitos-para-muitos entre Professionals e Companies
employees = db.Table('employees',
    db.Column('professional_id', db.Integer, db.ForeignKey('professionals.id')),
    db.Column('companies_id', db.Integer, db.ForeignKey('companies.id'))
    )

class Professionals(db.Model):
    __tablename__ = 'professionals'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    obs = db.Column(db.Text, nullable=False)
    companies = db.relationship('Companies',
                                secondary=employees,
                                backref=db.backref('professionals', lazy='dynamic'),
                                lazy='dynamic'
                                )

    def __repr__(self):
        return '<Professional %r>' %self.name


class Companies(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    site = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return '<Company %r>' %self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' %self.username