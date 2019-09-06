from flask_login import LoginManager, UserMixin

login_manager = LoginManager()

class User(UserMixin):
    ...

users = {'admin': {'password': 'admin'}}