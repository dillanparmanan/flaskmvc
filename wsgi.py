import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Course
from App.models import Lecturer
from App.models import Ta
from App.models import Tutor
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers import ( create_course, get_all_courses, get_all_courses_json )
from App.controllers import ( create_lecturer, get_all_lecturers, get_all_lecturers_json)
from App.controllers import ( create_ta )
from App.controllers import ( create_tutor )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)

@app.cli.command('get-users')
def get_users():
# gets all objects of a model
  users = User.query.all()
  print(users)

@user_cli.command('delete-user')
@click.argument('username', default='bob')
def delete_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  db.session.delete(bob)
  db.session.commit()
  print(f'{username} deleted')

  # this command will delete user bob

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

# this command will flask user list

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

'''
COURSE COMMANDS
'''

course_cli = AppGroup('course', help='Course object commands') 

@course_cli.command("create-course", help="Creates a new course")
@click.argument("code", default="comp1600")
@click.argument("name", default="Computing")
def create_course_command(code, name):
    create_course(code, name)
    print(f'{code} created!')

@course_cli.command("get-course", help="Retrieves a Course")
@click.argument('code', default='comp')
def get_course(code):
  comp = Course.query.filter_by(code=code).first()
  if not comp:
    print(f'{code} not found!')
    return
  print(comp)

@app.cli.command('get-courses')
def get_courses():
# gets all objects of a model
  courses = Course.query.all()
  print(courses)

@course_cli.command('delete-course')
@click.argument('code', default='comp')
def delete_course(code):
  comp = Course.query.filter_by(code=code).first()
  if not comp:
      print(f'{code} not found!')
      return
  db.session.delete(comp)
  db.session.commit()
  print(f'{code} deleted')

  # this command will delete user bob

@course_cli.command("list", help="Lists courses in the database")
@click.argument("format", default="string")
def list_course_command(format):
    if format == 'string':
        print(get_all_courses())
    else:
        print(get_all_courses_json())


app.cli.add_command(course_cli)

'''
LECTURER COMMANDS
'''
lecturer_cli = AppGroup('lecturer', help='User object commands') 

@app.cli.command("create-lecturer", help="Creates a lecturer")
@click.argument("firstname", default="nicholas")
@click.argument("lastname", default="mendez")
@click.argument("email", default="nicholasmendez@email.com")
def create_lecturer_command(firstname, lastname, email):
    create_lecturer(firstname, lastname, email)
    print(f'{firstname} created!')

@app.cli.command('get-lecturers')
@click.argument('name', default='comp')
def get_course_lecturers(name):
   comp = Course.query.filter_by(name=name).first()
   if not comp:
      print(f'{name} not found!')
      return
   print(comp.lecturers)

# Creates the lecture and adds it into the course
@app.cli.command('create-add-lecturer')
@click.argument('code', default='comp')
@click.argument('firstname', default='nicholas')
@click.argument('lastname', default='mendez')
@click.argument('email', default='nicholasmendez@email.com')
def add_lecturer(code, firstname, lastname, email):
  comp = Course.query.filter_by(code=code).first()
  if not comp:
     print(f'{code} not found!')
     return
  new_lecturer = Lecturer(firstname=firstname, lastname=lastname, email=email)
  comp.lecturers.append(new_lecturer)
  db.session.add(comp)
  db.session.commit()

# Finds the already created lecturer and adds it to course
@app.cli.command('add-lecturer')
@click.argument('code', default='comp1600')
@click.argument('firstname', default='nicholas')
def add_lecturer(code, firstname):
  course = Course.query.filter_by(code=code).first()
  if not course:
     print(f'{code} not found!')
     return
  add_lecturer = Lecturer.query.filter_by(firstname=firstname).first()
  course.lecturers.append(add_lecturer)
  print(f'{add_lecturer.firstname} was added to {course.code}')
  db.session.add(course)
  db.session.commit()


@app.cli.command("create-ta", help="Creates a ta")
@click.argument("firstname", default="sergio")
@click.argument("lastname", default="math")
@click.argument("email", default="sergiomath@email.com")
def create_ta_command(firstname, lastname, email):
    create_ta(firstname, lastname, email)
    print(f'{firstname} created!')

@app.cli.command('get-tas')
@click.argument('name', default='comp')
def get_course_tas(name):
   comp = Ta.query.filter_by(name=name).first()
   if not comp:
      print(f'{name} not found!')
      return
   print(comp.tas)


@app.cli.command('create-add-ta')
@click.argument('username', default='comp')
@click.argument('firstname', default='sergio')
@click.argument('lastname', default='math')
@click.argument('email', default='sergiomath@email.com')
def add_ta(username, firstname, lastname, email):
  comp = Course.query.filter_by(username=username).first()
  if not comp:
     print(f'{username} not found!')
     return
  new_ta = Ta(firstname=firstname, lastname=lastname, email=email)
  comp.tas.append(new_ta)
  db.session.add(comp)
  db.session.commit()

@app.cli.command('add-ta')
@click.argument('code', default='comp1600')
@click.argument('firstname', default='nicholas')
def add_ta(code, firstname):
  course = Course.query.filter_by(code=code).first()
  if not course:
     print(f'{code} not found!')
     return
  add_ta = Ta.query.filter_by(firstname=firstname).first()
  course.tas.append(add_ta)
  print(f'{add_ta.firstname} was added to {course.code}')
  db.session.add(course)
  db.session.commit()

@app.cli.command("create-tutor", help="Creates a tutor")
@click.argument("firstname", default="sergio")
@click.argument("lastname", default="math")
@click.argument("email", default="sergiomath@email.com")
def create_tutor_command(firstname, lastname, email):
    create_tutor(firstname, lastname, email)
    print(f'{firstname} created!')

@app.cli.command('get-tutors')
@click.argument('name', default='comp')
def get_course_tutors(name):
   comp = Tutor.query.filter_by(name=name).first()
   if not comp:
      print(f'{name} not found!')
      return
   print(comp.tutors)

@app.cli.command('create-add-tutor')
@click.argument('username', default='comp')
@click.argument('firstname', default='sergio')
@click.argument('lastname', default='math')
@click.argument('email', default='sergiomath@email.com')
def add_ta(username, firstname, lastname, email):
  comp = Course.query.filter_by(username=username).first()
  if not comp:
     print(f'{username} not found!')
     return
  new_tutor = Tutor(firstname=firstname, lastname=lastname, email=email)
  comp.tas.append(new_tutor)
  db.session.add(comp)
  db.session.commit()

@app.cli.command('add-tutor')
@click.argument('code', default='comp1600')
@click.argument('firstname', default='nicholas')
def add_tutor(code, firstname):
  course = Course.query.filter_by(code=code).first()
  if not course:
     print(f'{code} not found!')
     return
  add_tutor = Tutor.query.filter_by(firstname=firstname).first()
  course.tutors.append(add_ta)
  print(f'{add_tutor.firstname} was added to {course.code}')
  db.session.add(course)
  db.session.commit()




app.cli.add_command(lecturer_cli)