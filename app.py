from flask import Flask, request, redirect, render_template, flash, session, g
from models import db, connect_db, User, Favorites, Photos
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm, UserEditForm
from flask_bcrypt import Bcrypt
from key import SECRET
app = Flask(__name__)

CURR_USER_KEY = "curr_user"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mars'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.drop_all()
db.create_all()
#T O D O create tests for models and views
#T O D O make it so logged in hompage route only shows when user is logged in
#T O D O make it so mission info page has well written copy, maybe info from API calls. 
# Make sure to add logic in mission_info.html to catch if user is logged in to return them to the proper homepage
#T O D O make it so rover photos routes display images from API. Make sure to add logic in templates to show proper homepage
#T O D O remember to render form in signup.html and in edit.html, add delete btn
#___________________________________________________
# route for adding user to global, login and logout methods
#___________________________________________________
@app.before_request #messed with to show homepage, NEED TO FIX
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
def show_homepage():
    """route to display initial homepage"""
    return render_template('homepage.html')

@app.route("/homepage")
def show_logged_in_homepage():
    """route to display logged-in homepage"""
    return render_template('logged_in_homepage.html')

@app.route("/mission-info", methods=['GET'])
def show_mission_info():
    return render_template('mission_info.html')
    """route to display more information about photos and rovers"""

#___________________________________________________
#routes for rover photos
#___________________________________________________
@app.route("/curiousity/photos", methods=['GET', 'POST'])
def show_curiousity_photos():
    """route to display Curiousity info and photos"""
    return render_template('curiousity_photos.html')

@app.route("/opportunity/photos", methods=['GET', 'POST'])
def show_opportunity_photos():
    """route to display Opportunity info and photos"""
    return render_template('opportunity_photos.html')

@app.route("/spirit/photos", methods=['GET', 'POST'])
def show_spirit_photos():
    """route to display Spirit info and photos"""
    return render_template('spirit_photos.html')

#___________________________________________________
#route for onboarding user 
#___________________________________________________
@app.route('/user/signup', methods=["GET"])
def new_user_form():
    """sign up here"""
    return render_template('signup.html')

@app.route("/user/signup", methods=["POST"])
def create_new_user():
    """form submission for creating a new user"""
    return redirect('/logged_in_homepage.html')

#___________________________________________________
#routes for user capabilities
#___________________________________________________
@app.route("/<int:user_id>/edit")
def show_editpage(user_id):
    """show edit page"""
    return render_template('edit.html')

@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """handle form submission for updating user"""
    return redirect('/<int:user_id>/edit')

@app.route("/user/<int:user_id>")
def show_user_page(user_id):
    """show user info"""
    return render_template('user_info.html')



@app.route("/<int:user_id>/delete")
def delete(user_id):
    """delete user."""
    return redirect('/')
#___________________________________________________
#login/logout routes
#___________________________________________________
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

    return render_template('/login.html', form=form)


@app.route('/logout')

def logout():
    """handle user logout, using method from Springboard warbler project."""
    do_logout()
    flash("successful logout")
    return redirect('/login')

#___________________________________________________
#routes for adding/deleting/editing user favorites
#___________________________________________________
@app.route("/<int:user_id>/favorites")
def show_favoritespage(user_id):
    """show favorites page for viewing and deleting faves"""
    return render_template('favorites.html')

@app.route("/<int:user_id>/favorites", methods=['DELETE'])
def delete_favorites(user_id):
    """route for deleting a fave"""
    return redirect('favorites.html')

@app.route('/photos/<int:photo_id>/favorite', methods=['POST'])
def add_favorite(photo_id):
    """route for adding a favorite to user's favorites"""
    return redirect('/favorites')


@app.route("/photos/<int:photo_id>")
def show_photo():
    """routes for viewing a particular photo"""
    return render_template('photo.html')

#________________________________________________________
#after request borrowed from warbler Springboard exercise
#________________________________________________________
@app.after_request 
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


