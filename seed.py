
from flask import Flask
from faker import Faker
import random
from datetime import timedelta

app = Flask(__name__)
connect_to_db(app)

print("Deleting data!")

for table in reversed(db.metadata.sorted_tables):
    db.session.execute(table.delete())
db.session.commit()

fake = Faker()
trainers = []

for _ in range(10):
    trainers.append(
        Trainer(
            fname=fake.first_name(),
            lname=fake.last_name(),
            email=fake.email(),
            img_url=fake.image_url()
        )
    )

trainees = []

for trainer in trainers:
    for _ in range(2):
        trainees.append(
            Trainee(
                fname=fake.first_name(),
                lname=fake.last_name(),
                email=fake.email(),
                membership_plan = 5,
                trainer = trainer
            )
        )

healthlogs = []

# health_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     trainee_id = db.Column(db.Integer, db.ForeignKey('trainees.trainee_id'))
#     height = db.Column(db.Integer)  
#     body_weight = db.Column(db.Integer)
#     fat_percentage = db.Column(db.Integer)
#     log_date = db.Column(db.DateTime)

for trainee in trainees:
    start_date = fake.date_this_year()
    for i in range(10):
        log_date = start_date + timedelta(days=i*7)
        healthlogs.append(HealthLog( height = random.randint(100,180),body_weight = random.randint(40,80),fat_percentage=random.randint(5,30),log_date= log_date, trainee = trainee))



db.session.add_all(trainers)
db.session.add_all(trainees)
db.session.add_all(healthlogs)
db.session.commit()
