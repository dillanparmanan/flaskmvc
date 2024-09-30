from App.models import Course
from App.database import db

def create_course(name, username, password):
    newcourse = Course(name=name, username=username, password=password)
    db.session.add(newcourse)
    db.session.commit()
    return newcourse

def get_course_by_username(username):
    return Course.query.filter_by(username=username).first()

def get_course(id):
    return Course.query.get(id)

def get_all_courses():
    return Course.query.all()

def get_all_courses_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses = [courses.get_json() for course in courses]
    return courses

def update_course(id, username):
    course = get_course(id)
    if course:
        course.username = username
        db.session.add(course)
        return db.session.commit()
    return None