import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/register', methods=('GET','POST')) # defines route for URL path '/register' & specifies that can handle 'GET' & 'POST' HTTP methods
def register():  # defines register view function which handles requests to '/register' route
    if request.method == 'POST': # checks if  request method is 'POST' (form submitted)
        username = request.form['username'] # retrieves username from submitted data
        password = request.form['password'] # retrieves password
        db = get_db() # Gets db connection
        error = None # error value will be flashed if problems

        if not username: # if no user name
            error = "Username is required."
        elif not password: # if no password
            error = "Password is required."
        
        if error is None: # username & password present, attempt to insert new user
            try: #  attempts to insert, go to except if any issues
                db.execute( # SQL command to insert new user w/ provided username & pwd
                    "INSERT INTO user (username,password) VALUES (?,?)",
                    (username, generate_password_hash(password)),                                                               
                )
                db.commit() # commits transaction to database
            except db.IntegrityError: # username already exists
                error = f"User {username} is already register."
            else:
                return redirect(url_for("auth.login")) # if no errors, redirect user to login page
        flash(error)
    return render_template('auth/register.html') # renders auth/register.html tempalte


@bp.route('/login', methods=('GET', 'POST')) # defines route for '/login' URL path, accepts GET & POST HTTP
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        # check if user in database, if not then is None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password): # check if provided passowrd is correct
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request # decorator the registers load_logged_in_user func to run b4 every request
def load_logged_in_user():
    user_id = session.get('user_id') #attempts to retrieve user_is from session

    if user_id is None:
        g.user = None # indicates no user logged in
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,) # fetch one row from user_id & assigns to g.user
        ).fetchone()


bp.route('/logout') # define route for URL path '/logout'
def logout():
    session.clear() #clears all data from session, effectively logs user out
    return redirect(url_for('index')) #redirect to index page after log out

def login_required(view): # decorator used to protect views that only accessible to logged-in users
    @functools.wraps(view) #decorator that updates wrapped_view function to look like view
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login')) # returns to login if no user logged in
        return view(**kwargs) # if user logs in, calls og view func w/ any args passed to wrapped_view

    return wrapped_view

