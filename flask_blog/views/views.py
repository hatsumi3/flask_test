from functools import wraps

from flask import request, redirect, url_for, render_template, session, flash
from flask import Blueprint
from flask import current_app as app

view = Blueprint('view', __name__)

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('view.login'))
        return func(*args, **kwargs)
    return inner


@view.route('/login',methods={'GET','POST'})
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('username is differense.')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('password is differense.')
        else:
            session['logged_in'] = True
            flash('logged in')
            return redirect(url_for('entry.show_entries'))
    
    return render_template('login.html')


@view.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('logged out')
    return redirect(url_for('entry.show_entries'))

@view.app_errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('view.login'))