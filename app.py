import flask
import flask_login
from flask import render_template

#https://pypi.org/project/Flask-Login/

app = flask.Flask(__name__)
app.secret_key = 'supersecretstring'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'m@mail.com': {'password': 'secret'}}

#----------------------------------
#We also need to tell Flask-Login how to load a user from a Flask request and from
# its session. To do this we need to define our user object, a user_loader callback,
# and a request_loader callback.
class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user
#------------------------------------------
#Now we're ready to define our views. We can start with a login view, which will
# populate the session with authentication bits. After that we can define a view
# that requires authentication.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        #This stores the user’s ID (user.id) in the Flask session
        #login_user(user) adds the user ID to the session cookie.
		# (specifically in a signed cookie), so the login state persists between requests.
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'
#----------------------------------------------------------------------------
@app.route('/')
def index():
    return 'Welcome! Go to /login to log in.'
#--------------------------------------------------------
# This tells Flask to run the protected() function when the user visits /protected on
# your app. @flask_login.login_required i is a decorator ensures that only authenticated
# (logged-in) users can access this route. If the user is not logged in, they will be
# redirected to the login page (Flask-Login handles this automatically).
# flask_login.current_user.id - This is where Flask-Login retrieves the currently logged-in
# user's ID (which is stored in the session). It’s essentially the email you assigned
# to the user in the login function.
@app.route('/protected')
@flask_login.login_required
def protected():
    return render_template('protected.html', email=flask_login.current_user.id)
#--------------------------------------------------------
#Finally we can define a view to clear the session and log users out:
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('login'))  # or 'index'


if __name__ == '__main__':
    app.run(debug=True)

#---------------------------------------------------------------
#We now have a basic working application that makes use of session-based
# authentication.





