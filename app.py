from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Favorites, Photos
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mars'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!" #Todo-- LOOK THIS UP AND DO IT RIGHT
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.drop_all()
db.create_all()
#T O D O create LoginForm, forms in general. This will have an effect on login/logout routes, so consult them when yo do this


#___________________________________________________
#login and logout methods, adding user to global
#___________________________________________________
@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

#___________________________________________________
#routes for displaying general homepage and homepage for logged-in users, as well as the info page
#___________________________________________________
@app.route("/")
"""route to display initial homepage"""
def show_homepage():
    return render_template('homepage.html')

@app.route("/homepage")
"""route to display logged-in homepage"""

@app.route("/mission-info", methods=['GET'])
"""route to display more information about photos and rovers"""

#___________________________________________________
#routes for rover photos
#___________________________________________________
@app.route("/curiousity/photos", methods=['GET', 'POST'])
"""route to display Curiousity info and photos"""
@app.route("/opportunity/photos", methods=['GET', 'POST'])
"""route to display Opportunity info and photos"""
@app.route("/spirit/photos", methods=['GET', 'POST'])
"""route to display Spirit info and photos"""

#___________________________________________________
#routes for onboarding user 
#___________________________________________________
@app.route('/user/signup', methods=["GET"])
def new_user_form():
    """sign up here"""
@app.route("/user/signup", methods=["POST"])
def create_new_user():
    """form submission for creating a new user"""

#___________________________________________________
#routes for user capabilities
#___________________________________________________
@app.route("/<int:user_id>/edit")
def show_editpage(user_id):
    """show edit page"""
@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """handle form submission for updating user"""
@app.route("/<int:user_id>/favorites")
def show_favoritespage(user_id):
    """show favorites page for viewing and deleting faves"""
@app.route("/<int:user_id>/favorites", methods=['DELETE'])
def delete_favorites(user_id):
    """route for deleting a fave"""
@app.route("/<int:user_id>/delete")
def delete(user_id):
    """delete user."""

@app.route('/login', methods=["GET", "POST"])
def login():
    """handle user login, using method from Springboard warbler project"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')

def logout():
    """handle user logout, using method from Springboard warbler project."""
    do_logout()
    flash("successful logout")
    return redirect('/login')

#___________________________________________________
#routes for adding/deleting/editing user favorites
#___________________________________________________
@app.route('/users/<int:user_id>/favorites', methods=["GET"])
"""route for showing user's fave page"""
def show_favorites_page(user_id):

@app.route('/photos/<int:photo_id>/favorite', methods=['POST'])
"""route for adding a favorite to user's favorites"""
def add_favorite(photo_id):

@app.route("/photos/<int:photo_id>")
"""routes for viewing a particular photo"""


#after request borrowed from warbler Springboard exercise
@app.after_request 
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


