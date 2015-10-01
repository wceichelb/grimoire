from flask import render_template, flash, redirect, g, url_for, session, \
     request
from flask.ext.login import login_user, logout_user, current_user, \
     login_required
from datetime import datetime
from app import app, db, lm
from .forms import LoginForm, EditForm
from .models import User, Spell
from auth import OAuthSignIn
from config import SPELLS_PER_PAGE

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    print current_user
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
    # print oauth.callback()
    username, email = oauth.callback()
    if email is None:
        flash('Authentication failed')
        return redirect(url_for('index'))
    user = User.query.filter_by(email=email).first()
    if not user:
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]
        user = User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for('edit'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.char_name = form.char_name.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('edit'))
    elif request.method != "POST":
        form.nickname.data = g.user.nickname
        form.char_name.data = g.user.char_name
    return render_template('edit.html', form=form)
