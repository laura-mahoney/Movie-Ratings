"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db, add_new_user, check_email, check_user


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "dfiagiellkbeaio54869yjnhrgit4"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def register_form():
    """Allows user to register."""

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Redirects user to homepage if username is not taken."""

    email = request.form.get('email')
    password = request.form.get('password')


    email_confirm = check_email(email)

    if email_confirm == False:
        add_new_user(email, password)
        return redirect("/")
    else:
        return redirect("/login")


@app.route('/login', methods=["GET", "POST"])
def auth_user():
    """Checks if username matches password in database. """

    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        if check_email(email) is True:
            authenticate = check_user(email, password)

            if authenticate:
                session['user'] = authenticate
                flash('Log in successful')
                return redirect("/")
            else:
                flash('That was the wrong password, try again.')
        else:
            return redirect("/register")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
