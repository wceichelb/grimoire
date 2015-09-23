from app import app
from flask import render_template, g, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/spell')
def spell():
    return render_template('spell.html')

@app.route('/spellbook')
@app.route('/spellbook/<user>')
def spellbook(user=None):
    return render_template('spellbook.html', user=user)
