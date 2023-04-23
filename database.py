from sqlalchemy.orm import declarative_base,sessionmaker,relationship
from sqlalchemy import Column, Integer, String, ForeignKey,create_engine,Table,MetaData
import os

Base = declarative_base()

class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer(),primary_key=True)
    student_name = Column(String(25),nullable=False)
    email = Column(String(25),nullable=False,unique=True)
    course_id = Column(Integer(), ForeignKey('course.id'))

    

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer(), primary_key=True)
    course_name = Column(String(25),nullable=False,unique=True)
    student_id = Column(Integer(), ForeignKey('students.id'))

class StudentCourse(Base):
    __tablename__ = 'studentcourse'
    id = Column(Integer(), primary_key=True)
    student_id = Column(Integer(), ForeignKey('students.id'))
    course_id = Column(Integer(), ForeignKey('course.id'))    

