from flask_login import LoginManager, UserMixin

login_manager = LoginManager()

class User(UserMixin):
    ...
@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user
    
users = {'admin': {'password': 'admin'}}