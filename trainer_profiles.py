from model import User
import random

def show_trainers():
    """Show profile for each trainer"""
    trainers= User.query.filter_by(user_type="trainer").all()
    print(trainers)
    expertise=["Boxing", "Powerlifting", "Olympic Weightlifting","Endurance","Brazilian Combat","Thai Boxing", "Brzilian JiuJitsu", "Triathlon", "Hypertrophy"
                "Core", "Nutrition", "Weight Loss", "Weight Management", "Muscle", "Strength","H.I.I.T","Fat Loss", "Shred", "Athletic", "Speed", "Flexibility"
                "Muay Thai", "MMA", "Mobility Training", "Lean Muscle Development", "Corrective Exercise", "Stability", " Bodybuilding", "Circuits", "Spartan Race", 
                "Yoga", "Dance", "Toning", "Body Re-Composition", "Gymnastics", "CrossFit", "KickBoxing", "Martial Arts"]
    styles=["Hell", "No mercy", "Best friends forever", "Gentle", "Like your mom", "Sweat is just your fat crying"]
    certificates=["NCCA", "ACE", "ACSM", "NASM", "ISSA"]
    img_urls= ["/static/hulk.png","/static/bear.png","/static/thor.jpg","/static/queen.jpg"]

    trainer_profiles={}
    #[{"1":[fname, lname, _exps, _stles, cft]},
    # {"2":[fname, lname, _exps, _stles, cft]},
    # {"3":[fname, lname, _exps, _stles, cft]},...]
    for trainer in trainers:
        print(trainer)
        id= trainer.id
        fname= trainer.fname
        random_exps= random.choices(expertise, k=4)
        random_styles= random.choice(styles)
        random_cft= random.choices(certificates, k=3)
        random_url= random.choice(img_urls)
        trainer_profiles[fname]=[id,random_exps,random_styles, random_cft, random_url]

    