from app import db
from flask.ext.login import UserMixin

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), nullable=False)
    char_name = db.Column(db.String(64), index=True, nullable=True)
    email = db.Column(db.String(64), nullable=True)
    spellbook = db.relationship('Spellbook', backref="user")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Spellbook(db.Model):
    __tablename__ = 'spellbook'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Spellbook %r>" % (self.user.char_name)

class Spell(db.Model):
    __tablename__ = 'spell'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    spell_name = db.Column(db.String)
    school = db.Column(db.String)
    casting_time = db.Column(db.String)
    range = db.Column(db.String)
    components = db.Column(db.String)
    duration = db.Column(db.String)
    # additional_compenents = db.Column(db.String)
    description = db.Column(db.String)
    caster_class = db.Column(db.String)

    def __repr__(self):
        return "<Spell %r>" % (self.spell_name)
