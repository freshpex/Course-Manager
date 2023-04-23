from app import db
from flask_login import UserMixin
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Enrollment(Base):
    __tablename__ = "enrollments"
    student_id = Column("student_id", ForeignKey("students.id"), primary_key=True)
    course_id = Column("course_id", ForeignKey("courses.id"), primary_key=True)
    student = relationship("Student", back_populates="courses")
    course = relationship("Course", back_populates="students")

    def __repr__(self):
        return f"enrolled in {self.course.name}"


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    courses = relationship("Enrollment", back_populates="student")

    def __getitem__(self, field):
        if field == "courses":
            return self.courses
        return self.__dict__[field]


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    hours = Column(Integer)
    students = relationship("Enrollment", back_populates="course")

    def __getitem__(self, field):
        if field == "students":
            return self.students
        return self.__dict__[field]


class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.username