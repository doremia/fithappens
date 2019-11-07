from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy() #Instantiate a SQLAlchemy object. 


class Exercise(db.Model):
    """Data model for an exercise"""

    __tablename__ = "exercises"

    exercise_id =  db.Column(db.Integer, primary_key = True, autoincrement = True) 
    exercise = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Exercise: exercise={self.exercise} >"


class Menu(db.Model):
    """Data model for a Workout menu"""

    __tablename__ = "menus"

    menu_id =  db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(25), nullable = False) # (Cardio, Compound, Strength, Endurance)
    creator = db.Column(db.String(25)) #(default, )
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'), nullable = False)
    trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'), nullable = False)

    trainer = db.relationship("Trainer", backref="menus")
    trainee = db.relationship("Trainee", backref="menus")

class ExerciseMenu(db.Model):
    """Association data table for menu and exercise"""

    __tablename__ = "exercise_menus"

    ex_me_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ex_id =  db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable = False) 
    menu_id =  db.Column(db.Integer, db.ForeignKey('menus.menu_id'), nullable = False) 
    weight = db.Column(db.Integer, nullable = False)
    reps = db.Column(db.Integer, nullable = False)
    total_set = db.Column(db.Integer, nullable = False)

    exercise = db.relationship("Exercise", backref="exercise_menus")
    menu = db.relationship("Menu", backref="exercise_menus")

class Trainer(db.Model):
    """Data model for a trainer"""

    __tablename__ = "trainers"

    trainer_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fname = db.Column(db.String(25), nullable = False)
    lname = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(64))
    img_url = db.Column(db.String(150))

class Trainee(db.Model):
    """Data model for a trainee"""

    __tablename__ = "trainees"

    trainee_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'))
    fname = db.Column(db.String(25), nullable = False)
    lname = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(64))
    membership_plan = db.Column(db.Integer) #month as unit

    trainer = db.relationship("Trainer", backref="trainees")

class HealthLog(db.Model):
    """Data model for a health log"""

    __tablename__ = "healthlogs"

    health_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'))
    height = db.Column(db.Integer)  
    body_weight = db.Column(db.Integer)
    fat_percentage = db.Column(db.Integer)
    log_date = db.Column(db.DateTime)

    trainee = db.relationship("Trainee", backref="healthlogs")

class Session(db.Model):
    """"Data model for one training session"""

    __tablename__ = "sessions"

    session_id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    time = db.Column(db.DateTime)
    place = db.Column(db.String(50))
    sched_id = db.Column(db.Integer, db.ForeignKey('schedules.scheduled_id'), nullable = False)

    schedule = db.relationship("Schedule", backref="sessions")

class Schedule(db.Model):
    """Data model association of trainer and trainee's sessions""" 
    __tablename__ = "schedules"

    scheduled_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'), nullable = False)
    trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'), nullable = False)

    trainer = db.relationship("Trainer", backref="schedules")
    trainee = db.relationship("Trainee", backref="schedules")

def connect_to_db(app):
    """Connect the database to the Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fithappens'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    print("Connected to DB.")
