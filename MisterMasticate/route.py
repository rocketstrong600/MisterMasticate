from flask import render_template, url_for, flash, redirect, request
from MisterMasticate import app, db
from MisterMasticate.models import User, Stat, Modifier, Property, Item, Spell
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@login_required
def index():
    return render_template('Main.html', player=current_user)


@app.route('/cform', methods=["GET", "POST"])
def cform():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cname = request.form['cname']
        level = request.form['level']
        xp = request.form['xp']
        xpreq = request.form['xpreq']
        newuser = User(username=username, password=password, charactername=cname, gamemaster=False, level=int(level), xp=int(xp), xpreq=int(xpreq))
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('cform'))
    return render_template("CharacterForm.html")

@app.route('/iform', methods=["GET", "POST"])
@login_required
def iform():
    if request.method == 'POST':
        iname = request.form['iname']
        idescription = request.form['idescription']
        newitem = Item(name=iname, description=idescription, user_id=current_user.id)
        db.session.add(newitem)
        db.session.commit()
        return redirect(url_for('iform'))
    return render_template("ItemForm.html", player=current_user)

@app.route('/sform', methods=["GET", "POST"])
@login_required
def sform():
    if request.method == 'POST':
        bar = request.form['bar']
        sname = request.form['sname']
        intrinsic = request.form['intrinsic']
        if bar == "False":
            newstat = Stat(name=sname, intrinsic=int(intrinsic), equipment=int(0), user_id=current_user.id, bar=False)
            db.session.add(newstat)
            db.session.commit()
        else:
            current = request.form['current']
            colour_low = request.form['colour_low']
            colour_mid = request.form['colour_mid']
            colour_high = request.form['colour_high']
            mid_percent = request.form['mid_percent']
            high_percent = request.form['high_percent']
            newstat = Stat(name=sname, intrinsic=int(intrinsic), user_id=current_user.id, bar=True, current=int(current),
                           colour_low=colour_low, colour_mid=colour_mid, colour_high=colour_high,
                           mid_percent=int(mid_percent), high_percent=int(high_percent))
            db.session.add(newstat)
            db.session.commit()
        return redirect(url_for('sform'))
    return render_template("StatForm.html", player=current_user)


@app.route('/action_editor', methods=["GET", "POST"])
@login_required
def action_editor():
    thing = request.args.get('thing')
    things_id = request.args.get('id')
    if request.method == 'POST':
        action_script = request.data
        if thing == "player":
            User.query.get(int(things_id)).action_script = action_script
        elif thing == "item":
            Item.query.get(int(things_id)).action_script = action_script
        else:
            Spell.query.get(int(things_id)).action_script = action_script
        db.session.commit()
    else:
        if current_user.gamemaster:
            if thing == "player":
                action_script = User.query.get(int(things_id)).action_script
            elif thing == "item":
                action_script = Item.query.get(int(things_id)).action_script
            else:
                action_script = Spell.query.get(int(things_id)).action_script
            return render_template('ActionEditor.html', ActionScript=action_script, player=current_user)
        else:
            return "Gamemaster Area"


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
