from App.models import Course
from App.database import db

def create_course(code, name):
    newcourse = Course(code=code, name=name)
    db.session.add(newcourse)
    db.session.commit()
    return newcourse

def get_course_by_code(code):
    return Course.query.filter_by(code=code).first()

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

def update_coursecode(id, code):
    course = get_course(id)
    if course:
        course.code = code
        db.session.add(course)
        return db.session.commit()
    return None