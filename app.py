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
from sqlalchemy.exc import IntegrityError
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
#T O D O Make sure to add logic in Curiosity template to show proper homepage
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
    

@app.route("/<int:user_id>/homepage")
def show_logged_in_homepage(user_id):
    """route to display logged-in homepage"""
    today = datetime.utcnow()
    user = User.query.get_or_404(user_id)
    widget_response = requests.get(f"https://api.nasa.gov/insight_weather/?api_key={WAPIKEY}&Last_UTC={today}&feedtype=json&ver=1.0")
    data = widget_response.json()
    sol_day_of_curr_date = data["sol_keys"][6]
    celsius_on_mars = data[sol_day_of_curr_date]["AT"]["av"]
        
    if not g.user:
        flash("Please login.")
        return redirect("/")

    return render_template('logged_in_homepage.html', celsius_on_mars=celsius_on_mars, user=user)

@app.route("/mission-info", methods=['GET'])
def show_mission_info():
    """route to display more information about photos and rovers"""
    return render_template('mission_info.html')
    

#___________________________________________________
#routes for rover photos
#___________________________________________________
@app.route("/curiosity/photos", methods=['GET', 'POST'])
def show_curiosity_photos():
    """route to display Curiosity info and photos"""
    
    mission_info_resp = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={APIKEY}')

    data = mission_info_resp.json()
    photo_data = data["latest_photos"]
    for datum in photo_data:
        photo = datum["img_src"]
        
        new_photo = Photos(image_url=photo)
        db.session.add(new_photo)
        db.session.commit()
    
    return render_template("curiousity_photos.html", photos=photo_data)

#___________________________________________________
#route for onboarding user 
#___________________________________________________
@app.route('/user/signup', methods=['GET', 'POST'])
def create_new_user():
    """sign up here"""
    
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()
        
        except IntegrityError:
            flash("Please pick a unique username", "error") 
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect(f"/{user.id}/homepage")

    else:
        return render_template('signup.html', form=form)

#___________________________________________________
#routes for user capabilities
#___________________________________________________
@app.route("/<int:user_id>/edit")
def show_editpage(user_id):
    """show edit page"""
    user = User.query.get_or_404(user_id)
    if not g.user:
        flash("Please login.", "error")
        return redirect("/")

    form = UserEditForm()
    return render_template('edit.html', form=form, user=user)

@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """handle form submission for updating user"""
    user = User.query.get_or_404(user_id)
    form = UserEditForm()
    
    if not g.user:
        flash("Please login.", "error")
        return redirect("/")
    
    return render_template(f'/{user.id}/edit', form=form, user=user)

@app.route("/user/<int:user_id>")
def show_user_page(user_id):
    """show user info"""
    user = User.query.get_or_404(user_id)

    if not g.user:
        flash("Please login.", "error")
        return redirect("/")

    return render_template('user_info.html', user=user)

@app.route("/<int:user_id>/delete", methods=['GET'])
def show_delete_page(user_id):
    """show page for deleting user"""
    user = User.query.get_or_404(user_id)
    return render_template('delete_page.html', user=user)

@app.route("/<int:user_id>/delete", methods=['POST'])
def delete(user_id):
    """delete user."""
    user = User.query.get_or_404(user_id)

    if not g.user:
        flash("Please login.")
        return redirect("/")

        do_logout()
        #figure out how to do alert here for are you sure?
        db.session.delete(g.user)
        db.session.commit()

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
            return redirect(f"/{user.id}/homepage")

        flash("Check your username/password.", 'danger')

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

    user = User.query.get_or_404(user_id)

    return render_template('favorites.html', user=user, favorites=user.favorites)

@app.route('/photos/<int:photo_id>/favorite', methods=['GET', 'POST'])
def toggle_favorite(photo_id):
    """route for toggling a favorite in and out of user's faves"""

    if not g.user:
        flash("Please login.")
        return redirect("/")

    favorited_photo = Photos.query.get_or_404(photo_id)
    if favorited_photo.user_id == g.user.id:
        return abort(403)

    user_faves = g.user.favorites

    if favorited_photo in user_faves:
        g.user.favorites =[fave for favorite in user_faves if fave != favorited_photo] 

    else:
        g.user.favorites.append(favorited_photo)

        db.session.commit()

        return redirect("/favorites")
    


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


