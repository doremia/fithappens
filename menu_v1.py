from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, User, Exercise, Menu, ExerciseMenu


app = Flask(__name__)

app.secret_key = "MuahMuahMuah"

app.jinja_env.undefined = StrictUndefined


@app.route('/exercises')
def show_exercise():
    """Show the list of exercises on menu.html"""

    exercises = Exercise.query.all() 

    
    return render_template("exercises.html", exercises=exercises)


@app.route('/exercises', methods=['POST'])
def send_selected_exercises():
    """Add exercises to one Menu """

    name=request.form["input_menu_name"]
    creator= request.form["menu_type"]
    exercises = request.form.getlist('exercise')
    
    # user_id = session['user_id']  
    new_menu=Menu(name=name, creator=creator, user_id="jon") 
    # this has to be updated with session user_id
    db.session.add(new_menu)
    db.session.commit()

    # new_menu_id=new_menu.menu_id

    selected_exercises=[]
    for exercise_id in exercises:
        selected_exercise = Exercise.query.filter_by(exercise_id= exercise_id).one()
        selected_exercises.append(selected_exercise)

    # flash("Hooray! One workout menu added!")

    return render_template("selected_exercises.html", 
        new_menu=new_menu, 
        selected_exercises=selected_exercises)
    


# @app.route('/menu_<new_menu_id>')
# def show_selecred_exercises(new_menu_id):

#     return render_template("menu_v1.html")

@app.route('/menu/<int:new_menu_id>')
def show_selected_exercises(new_menu_id):

    menu_id=new_menu_id

    return render_template("selected_exercises.html",new_menu_id=menu_id)

@app.route('/menu/<int:new_menu_id>', methods=['POST'])
def build_menu(new_menu_id):


    exs = request.form.getlist('exercise')
    print(exs)
    for ex_id in exs:
        weight=request.form.get("{}_weight".format(ex_id))
        reps=request.form.get("{}_reps".format(ex_id))
        print(reps)
        total_set=request.form.get("{}_set".format(ex_id))
        new_exercsie_menu=ExerciseMenu(
            ex_id=ex_id , 
            menu_id= new_menu_id, 
            weight=weight,
            reps=reps, 
            total_set= total_set)
        db.session.add(new_exercsie_menu)

    db.session.commit()

        

    return render_template("show_menu.html")



# def add_exercise():
#     """Add an exercise to exercise's list"""

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
