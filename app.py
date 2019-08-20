from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
import binascii


app = Flask(__name__)
app.config['SECRET_KEY'] = "change me"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = ""

    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(user_id):
    user = User(int(binascii.hexlify(user_id.encode("utf-8")), 16))
    user.username = user_id
    return user


def verify_user(username, password):
    return True


@app.route('/')
@login_required
def index():
    return render_template('Main.html', Username=current_user.username)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            user = User(int(binascii.hexlify(username.encode("utf-8")), 16))
            user.username = username
            login_user(user)
            return redirect("/", code=303)
        else:
            return render_template("login.html", message="Login Failed")
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/login", code=303)


if __name__ == '__main__':
    app.run()
