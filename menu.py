from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect,session
from flask_debugtoolbar import DebugToolbarExtension


from model import db, connect_to_db, User, Exercise, Menu


app = Flask(__name__)

app.secret_key = "MuahMuahMuah"

app.jinja_env.undefined = StrictUndefined


@app.route('/menu')
def show_exercise():
    """Show the list of exercises on menu.html"""

    exercises = Exercise.query.all() 
    
    return render_template("menu.html", exercises=exercises)


# @app.route('/menu', methods=['POST'])
# def create_a_menu():
#     """Add menu to the Menu database"""

#     # menu_id =  db.Column(db.Integer, primary_key = True, autoincrement = True)
#     # name = db.Column(db.String(25), nullable = False) # (Cardio, Compound, Strength, Endurance)
#     # creator = db.Column(db.String(25)) #(default, )
#     # user_id = db.Column(db.String(25), db.ForeignKey('users.user_id'), nullable = False)
    
#     new_menu=Menu()

#     db.session.add(new_menu)
#     db.session.commit()

#     flash("Hooray! one workout menu added!")

#     return render_template("menu.html", exercises=exercises_names)



# def add_exercise():
#     """Add an exercise to exercise's list"""

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")





