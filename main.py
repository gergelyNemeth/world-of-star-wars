from flask import Flask, render_template, request, redirect, url_for, session
import requests
import data_manager
import werkzeug.security

app = Flask(__name__)
app.secret_key = '\xbd\x82\x83\xcf\xda}{\xff\xd5\xb8\n\x0cs\xe4\x8e\nU\xfc5\xec0$k\xcc'


@app.route('/', methods=["GET", "POST"])
def planets(url="https://swapi.co/api/planets/"):
    login_message, login_status = session_status()
    if request.method == "POST":
        if request.form['url'] != "None":
            url = request.form['url']
    response = requests.get(url).json()
    planets = response["results"]
    prev_page = response["previous"]
    next_page = response["next"]

    return render_template("star_wars.html", planets=planets, len=len, int=int, format=format,
                           prev_page=prev_page, next_page=next_page,
                           login_message=login_message, login_status=login_status)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    login_message, login_status = session_status()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        pass_hash = werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        data_manager.write_user(username, pass_hash)
        return redirect(url_for('planets'))

    return render_template("register_login.html", form="register",
                           login_message=login_message, login_status=login_status)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_message, login_status = session_status()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pass_hash_data = data_manager.read_user_password(username)
        if pass_hash_data:
            if werkzeug.security.check_password_hash(pass_hash_data, password):
                session['username'] = username
                return redirect(url_for('planets'))
            else:
                return 'Wrong password.'
        else:
            return 'You did not register yet.'

    return render_template("register_login.html", form="login", login_message=login_message)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('planets'))


def session_status():
    status = {}
    if 'username' in session:
        login_message = 'Logged in as {}'.format(session['username'])
        status['logged_in'] = True
    else:
        login_message = 'You are not logged in'
        status['logged_in'] = False

    return login_message, status['logged_in']


if __name__ == '__main__':
    app.run(debug=True)
