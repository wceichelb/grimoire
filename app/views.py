from flask import render_template, flash, redirect, g, url_for, session, \
     request
from flask.ext.login import login_user, logout_user, current_user, \
     login_required
from datetime import datetime
from app import app, db, lm
from .forms import LoginForm
from .models import User, Spell
from auth import OAuthSignIn
from config import SPELLS_PER_PAGE

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

###############################################################################
###
### ROUTES
###
###############################################################################

@app.route('/')
@app.route('/index')
@app.route('/index<int:page>')
def index(page=1):
    user = g.user
    spells = Spell.query.paginate(page, SPELLS_PER_PAGE, False)
    return render_template('index.html',
                           user=user,
                           spells=spells
                           )

# @app.route('/spell')
# def spell():
#     return render_template('spell.html')

# @app.route('/spellbook')
# @app.route('/spellbook/<user>')
# def spellbook(user=None):
#     if user is None:
#         return render_template('spellbook.html', spell=session.query(User).all())
#     return render_template('spellbook.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    print oauth.callback()
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))
