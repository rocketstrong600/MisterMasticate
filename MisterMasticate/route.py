from flask import render_template, url_for, flash, redirect, request
from MisterMasticate import app, db
from MisterMasticate.models import User, Stat, Modifier, Property, Item, Spell
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@login_required
def index():
#    player=User.query.filter_by(username=current_user.username)
    return render_template('Main.html', player=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next_page = request.args.get('next')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            return render_template("login.html", message="Login Failed")
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
