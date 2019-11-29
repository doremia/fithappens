
from flask import Flask
from faker import Faker
import random
from datetime import timedelta
from model import User, HealthLog, Exercise, connect_to_db, db
import requests


app = Flask(__name__)
connect_to_db(app)

##--Delete previous data--##

print("Deleting data!")

for table in reversed(db.metadata.sorted_tables):
    db.session.execute(table.delete())

db.session.commit()
fake = Faker()


##--API--##

def get_exercise_names():
    """rget json response from API"""
    #api-endpoint
    URL = "http://wger.de/api/v2/exercise.json/"
    # data-language, 2 is english 
    language = 2
    # status = 1 submitted by random dudes, status = 2 is what I want
    status = 2

    #defining a params dict for the parameters to be sent to the API 
    PARAMS = {"language": language, "status": status}
    response = requests.get(url = URL, params = PARAMS )
    while True:
        for result in response.json()["results"]:
            # print(result["name"])
            exercise = Exercise(exercise=result["name"])
            db.session.add(exercise)
            db.session.commit()
        URL =  response.json()["next"]
        response = requests.get(url = URL, params = PARAMS )
        if response.json()["next"] == None: break
    print("successfully added exercises from API")
    return 

get_exercise_names()

#--ADDING FAKES USERS--##

trainer_id= ["rich","jon","Tina","Patrick","Matt"]
trainers=[]
for trainer in trainer_id:
    trainers.append(
        User(
            user_id=trainer,
            fname=trainer,
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

#########------------ADDING FAKE HEALTHLOGS-----------------------------#########

healthlogs = []

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


##--ADDING MENUS--##

db.session.add_all(trainers)
db.session.add_all(trainees)
# db.session.add_all(healthlogs)

db.session.commit()

print("ADDED NEW DATA FOR TESTING!!")