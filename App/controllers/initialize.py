from .user import create_user
from .course import create_course
from .lecturer import create_lecturer
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_course('comp1600','comp','comppass')
    #create_lecturer('nicholas', 'mendez', 'nicholasmendez@email.com')
