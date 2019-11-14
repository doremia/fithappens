from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect,session
from flask_debugtoolbar import DebugToolbarExtension


from model import db, connect_to_db, User 


app = Flask(__name__)

app.secret_key = "MuahMuahMuah"

app.jinja_env.undefined = StrictUndefined

###################""CREATE AN USER""#######################

@app.route('/')
def index():
    """Homepage"""

    return render_template("Homepage.html")

@app.route('/' , methods=['POST'])
def redirect_register():
    """Redirect user based on action"""

    useraction = request.form['useraction']

    if useraction == "signin":

        return redirect("/register")

    elif useraction == "login":

        return redirect("/login")


@app.route('/register', methods=['GET'])
def show_register_type():
    """Show options for an user to sign up as a trainer or a trainee"""
    
    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_type():
    """Process the option to sign up as a trainer or a trainee"""
    
    user_type = request.form['usertype']

    if user_type == "trainer":

        return redirect("/register_trainer")

    else:

        return redirect("/register_trainee")


@app.route('/register_trainer', methods=['GET'])
def register_trainer():
    """Show register form for trainer"""

    return render_template("trainer_form.html")


@app.route('/register_trainer', methods=['POST'])
def register_trainer_process():
    """Process registration of a trainer."""

    user_id = request.form["user_id"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    img_url = request.form["img_url"]

    user = User(user_id=user_id, 
                fname=fname, 
                lname=lname, 
                password_hash=password,
                email=email,
                trainer_img_url=img_url,
                user_type="trainer")

    db.session.add(user)
    db.session.commit()

    return redirect("/")

@app.route('/register_trainee', methods=['GET'])
def register_trainee_form():
    """Show registration form of trainee"""

    return render_template("trainee_form.html")


@app.route('/register_trainee', methods=['POST'])
def register_trainee_process():
    """Process trainee registration."""

    user_id = request.form["user_id"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    trainer_membership = request.form["membership_plan"]
    trainer_id = request.form["trainer_id"] 

    user = User(user_id=user_id, 
                fname=fname, 
                lname=lname,
                password_hash=password,
                email=email,
                trainee_trainer_id=trainer_id,
                user_type="trainee")

    db.session.add(user)
    db.session.commit()


    return redirect("/")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    user_id = request.form["user_id"]
    password = request.form["password"]

    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        flash("I don't know you.")
        return redirect("/login")

    if user.password != password:
        flash("Hey! you fed me a wrong password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

@app.route('/user/{user.user_id}')
def show_profile():

    return render_template

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
