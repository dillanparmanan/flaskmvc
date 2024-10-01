from App.models import Lecturer
from App.database import db

def create_lecturer(firstname, lastname, email):
    newlecturer = Lecturer(firstname=firstname, lastname=lastname, email=email)
    db.session.add(newlecturer)
    db.session.commit()
    return newlecturer

def get_lecturer_by_firstname(firstname):
    return Lecturer.query.filter_by(firstname=firstname).first()

def get_lecturer(id):
    return Lecturer.query.get(id)

def get_all_lecturers():
    return Lecturer.query.all()

def get_all_lecturers_json():
    lecturers = Lecturer.query.all()
    if not lecturers:
        return []
    lecturers = [lecturer.get_json() for lecturer in lecturers]
    return lecturers

def update_lecturer(id, firstname):
    lecturer = get_lecturer(id)
    if lecturer:
        lecturer.firstname = firstname
        db.session.add(lecturer)
        return db.session.commit()
    return None
    