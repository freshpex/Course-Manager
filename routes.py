from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session
)
import sqlite3


from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)



from app import create_app,db,login_manager,bcrypt
from models import User
from forms import login_form,register_form
from flask import  request, g, redirect



# this part of the authentication for login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

# this part of the authentication for login
@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

# this part of the authentication sends to the homepage after login
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html",title="Home")

# this part of the authentication for login forms
@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )



# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data
            
            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )


#send to the logout page
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



##########################################################################################
############################################################################################
#############################################################################################
##############################################################################################
################################################################################################


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, MetaData   # <--- here
from sqlalchemy.orm import sessionmaker
from database import Students,Course, Base
from flask import g, jsonify, request, Response, session, redirect, url_for, render_template
from sqlalchemy.orm import query
import sqlite3
import json
from sqlalchemy.exc import IntegrityError


# We created a database engine that connects to the "database.db" SQLite database file.
engine = create_engine('sqlite:///database.db', echo=False)

# create session
# We created a session factory using the engine.
# We created a session from the session factory.

Session = sessionmaker(engine)
session = Session()

# create table
# We created all the tables defined in the Base class using the engine.

Base.metadata.create_all(engine)

#We defined a function called "save" that commits changes to the session.
def save():
    session.commit()

#We defined a view function for the index page that renders the "index.html" template.
@app.post("/login")
def loginpost():
    username=request.form['username']
    result = session.query(User).filter_by(user_name=username).first()
    session.close()
    print(result)
    if result is None:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("dash"))


@app.post("/dash")
def dash():
    username=request.form['username']
    return render_template("dash.html", username=username)

@app.get("/dash")
def dash_get():
    return render_template("dash.html")

@app.get('/login')
def logining():
    return render_template('login.html')

#students section
@app.route('/students', methods=["GET", "POST", "PATCH"])
def students():
    if request.method == "POST":
        student_to_delete = request.form["delete_student"]
        to_delete = session.query(Students).filter_by(id = student_to_delete).delete()
        save()
        session.close()
        return redirect(url_for("students"))
        
    elif request.method == "GET":
        result = (
            session.query(Students).all()
        )
        session.close()
        return(render_template('student/students.html',  students = result))

    # elif request.method == "PATCH":
    #     student_to_update = request.args["update_student"]
    #     return render_template("/student/<student_id>", student_to_update = student_to_update)
    

@app.route("/update", methods=["POST"])
def update():
        student_to_update = request.form["update_student"]
        result = session.query(Students).filter_by(id=student_to_update).first()
        
        return render_template("student/student.html", student_to_update=student_to_update)
    
        


@app.route('/courses', methods= ["GET", "POST"])
def courses():
    if request.method == "POST":
        course_to_delete = request.form["delete_course"]
        to_delete = session.query(Course).filter_by(id = course_to_delete).delete()
        save()
        session.close()
        return redirect(url_for("courses"))
    elif request.method == "GET":
        result = (
            session.query(Course).all()
        )
        session.close()
        return(render_template('course/courses.html', courses = result))
    
@app.route('/add_student', methods= ["GET", "POST"])
def add_student():
    if request.method == "GET":
        return(render_template("student/enroll_student.html"))
    if request.method == "POST":
        name_to_add = request.form["student_name"]
        email_to_add = request.form["student_email"]
        new_student = Students(student_name=name_to_add, email=email_to_add)
        to_add = session.add(new_student)
        try:
          save()
          session.commit()
          session.close()
          return redirect(url_for("students"))
        except IntegrityError:
            session.rollback()
            raise Exception("student name has already been taken")



@app.route("/student/<student_id>", methods=["GET", "POST"])
def view_student(student_id):
    if request.method == "GET":
        result = session.query(Students).filter_by(id=student_id).first()
        session.close()
        try:
            if result.course_id is not None:
                result = session.query(Students.id,Students.student_name,Students.email,Students.course_id,Course.course_name).select_from(Students).join(Course, Students.course_id == Course.id).filter_by(id=student_id).first()
                session.close()
        except AttributeError:
            return render_template("404_error.html", error_message="Student not found")
        
        return render_template("student/student.html", student_info=result, course_id=str(result.course_id))
    
    if request.method == "POST":
        course_id = request.form["course_id"]
        result = session.query(Students).filter_by(id=student_id).first()
        result.course_id = course_id
        save()
        result = session.query(Students).filter_by(id=student_id).first()
        session.close()
        student_course_id = True
        return render_template("student/student.html", student_info=result)

@app.route('/add_course', methods= ["GET", "POST"])
def add_course():
    if request.method == "GET":
        return(render_template("course/enroll_course.html"))
    if request.method == "POST":
        course_to_add = request.form["course_name"]
        new_course = Course(course_name=course_to_add)
        session.add(new_course)
        try:
          save()
          session.commit()
          session.close()
          return redirect(url_for("courses"))
        except IntegrityError:
            session.rollback()
            raise Exception("Course name has already been taken")

        
@app.route("/course/<course_id>", methods=["GET", "POST"])
def view_course(course_id):
    if request.method == "GET":
        result = session.query(Course).filter_by(id=course_id).first()
        session.close()
        if str(result.student_id) != "None":
            result= session.query(Course.id,Course.course_name,Course.student_id,Students.student_name,Students.email).join(Students, Course.student_id == Students.id).filter_by(id=course_id).first()
            session.close()
        else:
            result = session.query(Course).filter_by(id=course_id).first()
            session.close()
        print(str(result.student_id))
        return(render_template("course/course.html", course_info = result, student_id = str(result.student_id)))
    if request.method == "POST":
        student_id = request.form["student_id"]
        result = session.query(Course).filter_by(id=course_id).first()
        result.student_id = student_id
        save()
        result = session.query(Course).filter_by(id=course_id).first()
        session.close()
        course_student_id = True
        return(render_template("course/course.html", course_info = result))


if __name__ == "__main__":
    app.run(debug=True)
