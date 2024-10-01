from App.models import Tutor
from App.database import db

def create_tutor(firstname, lastname, email):
    newtutor = Tutor(firstname=firstname, lastname=lastname, email=email)
    db.session.add(newtutor)
    db.session.commit()
    return newtutor

def get_tutor_by_firstname(firstname):
    return Tutor.query.filter_by(firstname=firstname).first()

def get_tutor(id):
    return Tutor.query.get(id)

def get_all_tutors():
    return Tutor.query.all()

def get_all_tutors_json():
    tutors = Tutor.query.all()
    if not tutors:
        return []
    tutors = [tutor.get_json() for tutor in tutors]
    return tutors

def update_tutor(id, firstname):
    tutor = get_tutor(id)
    if tutor:
        tutor.firstname = firstname
        db.session.add(tutor)
        return db.session.commit()
    return None