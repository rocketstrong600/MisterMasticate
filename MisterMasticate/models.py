from MisterMasticate import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    charactername = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    gamemaster = db.Column(db.Boolean, nullable=False, default=False)
    action_script = db.Column(db.Text, nullable=True)
    level = db.Column(db.Integer, nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    xpreq = db.Column(db.Integer, nullable=False)

    stats = db.relationship('Stat', backref='owner', lazy=True)
    items = db.relationship('Item', backref='owner', lazy=True)
    spells = db.relationship('Spell', backref='owner', lazy=True)

    def __repr__(self):
        return "User('"+"self.username"+"')"


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    colour_high = db.Column(db.String(10), nullable=True)
    colour_mid = db.Column(db.String(10), nullable=True)
    colour_low = db.Column(db.String(10), nullable=True)
    high_percent = db.Column(db.Integer, nullable=True, default='50')
    mid_percent = db.Column(db.Integer, nullable=True, default='25')
    bar = db.Column(db.Boolean, nullable=False, default=False)
    current = db.Column(db.Integer, nullable=True)
    intrinsic = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.Integer, nullable=True)
    buff_turns = db.Column(db.Integer, nullable=True)
    buff_amount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "Stat('"+"self.name"+"')"

    def total(self):
        return (self.intrinsic or 0) + (self.equipment or 0) + (self.buff_amount or 0)

    def percent(self):
        return (self.current or 0) / (self.total() or 0) * 100

    def colour(self):
        if self.percent() >= self.high_percent:
            color = self.colour_high
        elif self.percent() >= self.mid_percent:
            color = self.colour_mid
        else:
            color = self.colour_low
        return color


class Modifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    modifies_name = db.Column(db.String(100), nullable=False)
    modifier = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "Modifier('"+"self.name"+"', '"+"self.modifies_name"+"', '"+"self.modifier"+"')"


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "Modifier('"+"self.name"+"', '"+"self.modifies_name"+"', '"+"self.modifier"+"')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action_script = db.Column(db.Text, nullable=True)
    modifiers = db.relationship('Modifier', backref='owner', lazy=True)
    properties = db.relationship('Property', lazy=True)

    def __repr__(self):
        return "Item('"+"self.Name"+"')"


class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action_script = db.Column(db.Text, nullable=True)
    properties = db.relationship('Property', lazy=True)

    def __repr__(self):
        return "Spell('"+"self.name"+"')"

class Ability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action_script = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return "Spell('"+"self.name"+"')"
