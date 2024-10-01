from App.models import Ta
from App.database import db

def create_ta(firstname, lastname, email):
    newta = Ta(firstname=firstname, lastname=lastname, email=email)
    db.session.add(newta)
    db.session.commit()
    return newta

def get_ta_by_firstname(firstname):
    return Ta.query.filter_by(firstname=firstname).first()

def get_ta(id):
    return Ta.query.get(id)

def get_all_Tas():
    return Ta.query.all()

def get_all_tas_json():
    tas = Ta.query.all()
    if not tas:
        return []
    tas = [ta.get_json() for ta in tas]
    return tas

def update_ta(id, firstname):
    ta = get_ta(id)
    if ta:
        ta.firstname = firstname
        db.session.add(ta)
        return db.session.commit()
    return None