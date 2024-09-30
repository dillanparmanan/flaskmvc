import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Course
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers import ( create_course, get_all_courses, get_all_courses_json )

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
@click.argument("name")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_course_command(name, username, password):
    create_course(name, username, password)
    print(f'{username} created!')

@course_cli.command("get-course", help="Retrieves a Course")
@click.argument('username', default='bob')
def get_user(username):
  comp = Course.query.filter_by(username=username).first()
  if not comp:
    print(f'{username} not found!')
    return
  print(comp)

@app.cli.command('get-courses')
def get_courses():
# gets all objects of a model
  courses = Course.query.all()
  print(courses)

@course_cli.command('delete-course')
@click.argument('username', default='comp')
def delete_course(username):
  comp = Course.query.filter_by(username=username).first()
  if not comp:
      print(f'{username} not found!')
      return
  db.session.delete(comp)
  db.session.commit()
  print(f'{username} deleted')

  # this command will delete user bob

@course_cli.command("list", help="Lists courses in the database")
@click.argument("format", default="string")
def list_course_command(format):
    if format == 'string':
        print(get_all_courses())
    else:
        print(get_all_courses_json())


app.cli.add_command(course_cli)