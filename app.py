from flask import Flask, request, redirect, render_template, flash, session, jsonify, g
from models import db, connect_db, User, Favorites, Photos
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm, UserEditForm
from flask_bcrypt import Bcrypt
from key import SECRET, APIKEY, WAPIKEY
from datetime import date, datetime
import requests
import json
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
#T O D O make it so mission info page has well written copy, maybe info from API calls. 
# Make sure to add logic in mission_info.html to catch if user is logged in to return them to the proper homepage
#T O D O make it so rover photos routes display images from API. Make sure to add logic in templates to show proper homepage
#T O D O remember to add delete btn functionality in edit.html route
#T O D O render Mars photo on rover pages and favorites page
#T O D O return to logged-in-homepage route once you've got the signup route complete



#___________________________________________________
# route for adding user to global, login and logout methods
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
def show_homepage():
    """route to display initial homepage"""
    today = datetime.utcnow()
    
    widget_response = requests.get(f"https://api.nasa.gov/insight_weather/?api_key={WAPIKEY}&Last_UTC={today}&feedtype=json&ver=1.0")
    data = widget_response.json()
    sol_day_of_curr_date = data["sol_keys"][6]
    celsius_on_mars = data[sol_day_of_curr_date]["AT"]["av"]
    return render_template("homepage.html", celsius_on_mars=celsius_on_mars) 
    

@app.route("/homepage")
def show_logged_in_homepage():
    """route to display logged-in homepage"""
    today = datetime.utcnow()
    resp = requests.get()

    widget_response = requests.get(f"https://api.nasa.gov/insight_weather/?api_key={WAPIKEY}&Last_UTC={today}&feedtype=json&ver=1.0")
    data = widget_response.json()
    sol_day_of_curr_date = data["sol_keys"][6]
    celsius_on_mars = data[sol_day_of_curr_date]["AT"]["av"]
        
    if not g.user:
        flash("Please login.")
        return redirect("/")

    return render_template('logged_in_homepage.html', celsius_on_mars=celsius_on_mars)

@app.route("/mission-info", methods=['GET'])
def show_mission_info():

    return render_template('mission_info.html')
    """route to display more information about photos and rovers"""

#___________________________________________________
#routes for rover photos
#___________________________________________________
@app.route("/curiosity/photos", methods=['GET', 'POST'])
def show_curiosity_photos():
    """route to display Curiosity info and photos"""
    
    mission_info_resp = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={APIKEY}')

    data = mission_info_resp.json()
    photos = data["latest_photos"]
    for photo in photos:
        photo_dict = photo["img_src"]
        #figure out why dict is returned here
        # new_photo = Photos(image_url=photo_url)
        # db.session.add(new_photo)
        # db.session.commit()
    
    return render_template("curiousity_photos.html", photos=photo_dict)
    # return jsonify(data["latest_photos"])

# def trying_other_way():
#     today = date.today()
#     mission_info_resp = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={today}&camera=pancam&api_key={APIKEY}')
#     data = mission_info_resp.json()
#     return jsonify(data)  returns dict w key of "photos" and empty array
#___________________________________________________
#route for onboarding user 
#___________________________________________________
@app.route('/user/signup', methods=["GET"])
def new_user_form():
    """sign up here"""
    form = SignUpForm()
    return render_template('signup.html', form=form)

@app.route("/user/signup", methods=["POST"])
def create_new_user():
    """form submission for creating a new user"""
    form = SignUpForm()
    return redirect('/logged_in_homepage.html', form=form)

#___________________________________________________
#routes for user capabilities
#___________________________________________________
@app.route("/<int:user_id>/edit")
def show_editpage(user_id):
    """show edit page"""

    if not g.user:
        flash("Please login.")
        return redirect("/")

    form = UserEditForm()
    return render_template('edit.html', form= form)

@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    if not g.user:
        flash("Please login.")
        return redirect("/")
    """handle form submission for updating user"""
    form = UserEditForm()
    return redirect('/<int:user_id>/edit', form=form)

@app.route("/user/<int:user_id>")
def show_user_page(user_id):
    """show user info"""
    if not g.user:
        flash("Please login.")
        return redirect("/")
    return render_template('user_info.html')



@app.route("/<int:user_id>/delete")
def delete(user_id):
    """delete user."""
    if not g.user:
        flash("Please login.")
        return redirect("/")
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

    return render_template('login.html', form=form)


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
    if not g.user:
        flash("Please login.")
        return redirect("/")
    return render_template('favorites.html')

@app.route("/<int:user_id>/favorites", methods=['DELETE'])
def delete_favorites(user_id):
    if not g.user:
        flash("Please login.")
        return redirect("/")
    """route for deleting a fave"""
    return redirect('favorites.html')

@app.route('/photos/<int:photo_id>/favorite', methods=['POST'])
def add_favorite(photo_id):
    if not g.user:
        flash("Please login.")
        return redirect("/")
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


