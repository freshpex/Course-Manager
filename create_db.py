from database import Students,engine,Base,Session,Course,Instructor,StudentCourse


Base.metadata.create_all(engine)