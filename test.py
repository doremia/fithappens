from model import db, connect_to_db, User, Exercise, Menu, ExerciseMenu

def test():
    # exercises = Exercise.query.filter(Exercise.exercise.ilike('%ab%')).all()
    exercises = Exercise.query.all()

    print(exercises)

    return 

test()
