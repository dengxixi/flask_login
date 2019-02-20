from flask import Flask
from flask import render_template
from flask import request, session, make_response, redirect, url_for, flash
import time
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

conn = get_db()
cur = conn.cursor()
app = Flask(__name__)


@app.route('/')
def index():
    if 'user' in session:
        return render_template('hello.html', name=session['user'])
    else:
        return redirect(url_for('login'), 302)


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        error = None
        if not name:
            error = 'user name is None'
        elif not password:
            error = 'password is None'
        else:
            cur.execute(
                'select * from users where name=%s and password=%s', (name, password)
            )
            dummy = cur.fetchone()
            if dummy is not None:
                error = 'User {} was already register.'.format(name)

        if error is None:
            cur.execute(
                'insert into users (name, password) VALUES (%s, %s)', (name, password)
            )
            conn.commit()
            session['user'] = name
            flash('register ok!')
            return redirect(url_for('index'))
        else:
            flash(error)
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cur.execute(
            'select * from users where name=%s', (name,)
        )
        user = cur.fetchone()
        if user is None:
            error = 'No such user'
        elif user[1] != password:
            error = 'password error'
        else:
            session['user'] = request.form['name']
            flash('Login successful', 'info')
            return redirect(url_for('index'))

            # response = make_response('Admin login successfully!')
            # response.set_cookie('login_time', time.strftime('%Y-%m-%d %H:%M:%S'), 900)
        flash(error)
        return redirect(url_for('login'))
    else:
        return render_template('login.html')
    #     if 'user' in session:
    #         login_time = request.cookies.get('login_time')
    #         response = make_response('Hello %s, you logged in on %s' % (session['user'], login_time))
    #     else:
    #         title = request.args.get('title', 'Default')
    #         response = make_response(render_template('login.html', title=title), 200)
    #
    # return response


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


@app.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = make_response(error.message)
    response.status_code = error.status_code
    response = make_response('No such user')

    return response


@app.route('/exception')
def exception():
    raise InvalidUsage('No!!!!!', status_code=404)


app.secret_key = '123456'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
