from jinja2 import StrictUndefined

from flask import Flask, request, jsonify, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, User, Exercise, Menu, ExerciseMenu, Schedule, Session 

import random


app = Flask(__name__)

app.secret_key = "MuahMuahMuah"

app.jinja_env.undefined = StrictUndefined


##--CREATE AN USER--##

@app.route('/')
def index():
    """Show Homepage"""

    return render_template("Homepage.html")


@app.route('/register', methods=['GET'])
def show_register_type():
    """Show options for an user to sign up as a trainer or a trainee"""
    
    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_type():
    """Process the option to sign up as a trainer or a trainee"""
    
    user_type = request.form["usertype"]

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

    if session['user_id']:
        flash("Already logged in")
        return redirect('/')

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")

    return redirect("/")

# @app.route('/user/{user.user_id}')
# def show_profile():

#     return render_template

@app.route("/trainer_profiles")
def show_trainers():
    trainers= User.query.filter_by(user_type="trainer").all()
    print(trainers)
    expertise=[
        "Boxing", "Powerlifting", "Olympic Weightlifting","Endurance","Brazilian Combat","Thai Boxing", "Brzilian JiuJitsu", "Triathlon", "Hypertrophy"
        "Core", "Nutrition", "Weight Loss", "Weight Management", "Muscle", "Strength","H.I.I.T","Fat Loss", "Shred", "Athletic", "Speed", "Flexibility"
        "Muay Thai", "MMA", "Mobility Training", "Lean Muscle Development", "Corrective Exercise", "Stability", " Bodybuilding", "Circuits", "Spartan Race", 
        "Yoga", "Dance", "Toning", "Body Re-Composition", "Gymnastics", "CrossFit", "KickBoxing", "Martial Arts"
    ]
    styles=["Hell", "No mercy", "Best friends forever", "Gentle", "Like your mom", "Sweat is just your fat crying"]
    certificates=["NCCA", "ACE", "ACSM", "NASM", "ISSA"]
    img_urls= ["/static/jon.jpg","/static/tina.jpg","/static/bear.png","/static/masha.jpg","/static/queen.jpg"]
    sample_url=["/static/dog1.jpg","/static/dog2.jpg"]

    trainer_profiles={}
    #[{"1":[fname, lname, _exps, _stles, cft]},
    # {"2":[fname, lname, _exps, _stles, cft]},]
    for trainer in trainers:
        print(trainer.user_id)
        id= trainer.id  
        user_id = trainer.user_id
        if trainer.user_id == "Tina":
            trainer.trainer_img_url = img_urls[1]
            random_url = trainer.trainer_img_url
        if trainer.user_id == "Jon":
            trainer.trainer_img_url = img_urls[0]
            random_url = trainer.trainer_img_url
        if trainer.user_id =="Matt":
            trainer.trainer_img_url = img_urls[2]
            random_url = trainer.trainer_img_url
        if trainer.user_id =="Masha":
            trainer.trainer_img_url = img_urls[3]
            random_url = trainer.trainer_img_url
        if trainer.user_id =="Rich":
            trainer.trainer_img_url = img_urls[4]
            random_url = trainer.trainer_img_url

        # else:
        #     random_url = random.choice(sample_url)

        fname= trainer.fname
        print(fname)
        random_exps= random.choices(expertise, k=4)
        random_styles= random.choice(styles)
        random_cft= random.choices(certificates, k=3)
        trainer_profiles[id]=[user_id,random_exps,random_styles, random_cft, random_url]
    
    return render_template("trainer_profiles.html", trainer_profiles=trainer_profiles)

@app.route('/exercises')
def show_exercise():
    """Show the list of exercises on menu.html"""

    exercises = Exercise.query.all() 
    
    
    return render_template("exercises_catalog.html", exercises=exercises)


# AJAX request for getting exercise 
@app.route('/search_exercise.json')
def search_exercise():
    """Search exercise name for exercise text box"""

    search_name=request.args.get("search_name")
    print(search_name)
    
    exercises_options = Exercise.query.filter(Exercise.exercise.ilike(f"%{search_name}%")).all()
    print(exercises_options)

    res =[]
    for exercise in exercises_options:
        ex = {}
        ex["id"] = exercise.exercise_id 
        ex["name"]= exercise.exercise
        res.append(ex)

    return jsonify(res)

@app.route('/build_menu', methods=["POST"]) #from exercises_catalog's form submit 
def get_selected_exes():
    """Receive and Send selected exercises to show_menu.html """
    
    selected_ids = request.form.getlist("checkboxes")
    print(selected_ids)
    selected_exes=[]

    for id in selected_ids:
        selected_ex = Exercise.query.filter_by(exercise_id=id).one()
        selected_exes.append(selected_ex)

    return render_template("show_menu.html", selected_exes=selected_exes)

@app.route('/create_menu_db', methods=["POST"])
def save_menu_DB():
    """Add one menu to database"""

    name = request.form["menu_name"]
    creator = request.form["menu_type"]
    new_menu = Menu(name=name, creator=creator, user_id="Tina") 
    # this has to be updated with session user_id
    db.session.add(new_menu)
    db.session.commit()
    res = new_menu.menu_id
    return jsonify(res)

@app.route('/menu', methods=["POST"])
def exerciseMenu_DB():
    """Add one ExerciseMenu to database"""

    exes = request.form.getlist('ex')
    menu_id = request.form.get("menu_id")
    print(request.form)
    print(exes)
    for ex_id in exes:
        
        weight=request.form.get("{}_weight".format(ex_id))
        reps=request.form.get("{}_reps".format(ex_id))
        total_set=request.form.get("{}_set".format(ex_id))

        new_exercsie_menu=ExerciseMenu(
            ex_id=ex_id, 
            menu_id= menu_id, 
            weight=weight,
            reps=reps, 
            total_set= total_set)

        db.session.add(new_exercsie_menu)

    db.session.commit()

    flash("Successfully added a new menu")

    return render_template("exercises_catalog.html")

@app.route('/calendar')
def show_calendar():
    """show calender page"""

    return render_template('calendar.html')

@app.route('/add_event', methods=["POST"])
def add_event():
    """Add an event to session & schedule model"""

    user_id= request.form["userName"]
    date = request.form["date"]
    place = request.form["place"]
    
    schedule = Schedule(user_id=user_id)
    db.session.add(schedule)
    db.session.commit()

    sched_id = schedule.scheduled_id

    res = {"sched_id" : schedule.scheduled_id , "user_id" :user_id, "date" : date, "place" : place}
    
    return jsonify(res)

@app.route('/add_session', methods=["POST"])
def add_session():
    """Add to session model"""

    sched_id = request.form["schedId"]
    date = request.form["date"]
    place = request.form["place"]
    print(date)
    print(place)

    session = Session(
        sched_id=sched_id,
        time=date,
        place=place
    )

    db.session.add(session)
    db.session.commit()

    res = ["don't really need this"]
    return jsonify(res)
 
if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
