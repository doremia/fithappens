
from flask import Flask
from faker import Faker
import random
from datetime import timedelta
from model import User, HealthLog, Exercise, connect_to_db, db

app = Flask(__name__)
connect_to_db(app)

print("Deleting data!")

for table in reversed(db.metadata.sorted_tables):
    db.session.execute(table.delete())
db.session.commit()

fake = Faker()

##########------------ADDING FAKES USERS-----------------------------#########

    # user_id = db.Column(db.String(25), unique=True, nullable = False)
    # fname = db.Column(db.String(25), nullable = False)
    # lname = db.Column(db.String(25), nullable = False)
    # email = db.Column(db.String(64))
    # trainer_img_url = db.Column(db.String(150))
    # trainee_membership= db.Column(db.Integer) #month as unit
    # user_type = db.Column(db.String(25))
    # trainee_trainer_id = db.Column(db.String(25), db.ForeignKey('users.user_id'))
    # password_hash = db.Column(db.String(30), nullable=False) #storing passwords as byte string

trainer_id= ["rich","jon","Tina","Patrick","Matt"]
trainers=[]
for trainer in trainer_id:
    trainers.append(
        User(
            user_id=trainer,
            fname=fake.first_name(),
            lname=fake.last_name(),
            email=fake.email(),
            trainer_img_url=fake.image_url(),
            user_type="trainer",
            password_hash=fake.name(),
        )
    )

trainees=[]
for trainer_name in trainer_id:
    trainees.append(
        User(
            user_id=fake.name(),
            fname=fake.first_name(),
            lname=fake.last_name(),
            email=fake.email(),
            trainee_membership=random.randint(1,20),
            user_type="trainee",
            trainee_trainer_id=trainer_name,
            password_hash=fake.name()
        )
    )

##########------------ADDING FAKE HEALTHLOGS-----------------------------#########

healthlogs = []
# health_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     user_id = db.Column(db.String(25), db.ForeignKey('users.user_id'))
#     height = db.Column(db.Integer)  
#     body_weight = db.Column(db.Integer)
#     fat_percentage = db.Column(db.Integer)
#     log_date = db.Column(db.DateTime)


for trainee in trainees:
    start_date = fake.date_this_year()
    for i in range(10):
        log_date = start_date + timedelta(days=i*7)
        healthlogs.append(HealthLog( 
                                    height = random.randint(100,180),
                                    body_weight = random.randint(40,80),
                                    fat_percentage=random.randint(5,30),
                                    log_date= log_date, 
                                    user_id = trainee.user_id)
                                    )

##########------------ADDING EXERCISES----------------#########

exercises=[
            "Squat",
            "Romanian Deadlift",
            "Dumbell Squat",
            "Front Squat",
            "Staircase",
            "Tippy Toes",
            "Single Leg Squat",
            "Jumping Jack",
            "Burpee",
            "Barbell Benchpress",
            "Toe touches",
            "Push up",
            "Cable Butterfy"]

exercises_object=[]
for exercise in exercises:
    exercises_object.append( Exercise(exercise=exercise) )

################--------ADDING MENUS--------------##############




db.session.add_all(trainers)
db.session.add_all(trainees)
db.session.add_all(healthlogs)
db.session.add_all(exercises_object)

db.session.commit()

print("ADDED NEW DATA FOR TESTING!!")