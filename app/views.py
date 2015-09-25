from flask import render_template, flash, redirect, g, url_for, session
from flask.ext.login import login_user, logout_user, current_user, \
     login_required
from datetime import datetime
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User, Spell
from config import SPELLS_PER_PAGE

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
    spells = Spell.query.paginate(page, SPELLS_PER_PAGE, False)
    return render_template('index.html',
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
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['char_name'])
    return render_template('login.html',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('invalid login, try again')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        char_name = resp.char_name
        if char_name is None or char_name == "":
            char_name = resp.email.split("@")[0]
        user = User(char_name=char_name, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
