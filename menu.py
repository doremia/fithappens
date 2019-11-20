from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, User, Exercise, Menu, ExerciseMenu


app = Flask(__name__)

app.secret_key = "MuahMuahMuah"

app.jinja_env.undefined = StrictUndefined


@app.route('/menu')
def show_exercise():
    """Show the list of exercises on menu.html"""

    exercises = Exercise.query.all() 

    
    return render_template("menu.html", exercises=exercises)


@app.route('/menu', methods=['POST'])
def create_a_menu():
    """Add menu to the Menu database"""

    # class ExerciseMenu(db.Model):
    # """Association data table for menu and exercise"""

    # __tablename__ = "exercise_menus"

    # ex_me_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    # ex_id =  db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable = False) 
    # menu_id =  db.Column(db.Integer, db.ForeignKey('menus.menu_id'), nullable = False) 
    # weight = db.Column(db.Integer, nullable = False)
    # reps = db.Column(db.Integer, nullable = False)
    # total_set = db.Column(db.Integer, nullable = False)

    # exercise = db.relationship("Exercise", backref="exercise_menus")
    # menu = db.relationship("Menu", backref="exercise_menus")


    # menu_id =  db.Column(db.Integer, primary_key = True, autoincrement = True)
    # name = db.Column(db.String(25), nullable = False) # 
    # creator = db.Column(db.String(25)) #(default, ) #(users can create their own categories)
    # user_id = db.Column(db.String(25), db.ForeignKey('users.user_id'), nullable = False)
    
    # name=request.form["input_menu_name"]
    # exercises = request.form.getlist('exercise')
    # creator= request.form["menu_type"]
    # user_id = session['user_id']
    # user_id="Tina"
    # weight=
    # reps=
    # total_set=

    # new_menu=Menu(name=name, creator=menu_type, user_id=user_id)

    # new_exercsie_menu=ExerciseMenu(ex_id= , menu_id= , weight= ,
    #     reps= , total_set= )


    # db.session.add(new_menu)
    # db.session.commit()

    flash("Hooray! One workout menu added!")

    return render_template("show_menu.html")



# def add_exercise():
#     """Add an exercise to exercise's list"""

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")





