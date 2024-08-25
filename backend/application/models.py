from .database import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_fname=db.Column(db.String(128),nullable=False)
    user_lname=db.Column(db.String(128))
    user_email=db.Column(db.String(128))
    password=db.Column(db.String(128))
    type=db.Column(db.String(128))
    count=db.Column(db.Integer)# max value 5
    profile_pic=db.Column(db.String(128))

class Librarian(db.Model):
    __tablename__='librarian'
    librarian_id=db.Column(db.VARCHAR,primary_key=True)
    librarian_fname=db.Column(db.VARCHAR,nullable=False)
    librarian_lname=db.Column(db.VARCHAR)
    librarian_email=db.Column(db.VARCHAR)
    password=db.Column(db.VARCHAR)
    
    
class Section(db.Model):
    __tablename__='section'
    section_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String)
    date=db.Column(db.String)
    description=db.Column(db.String,nullable=False)
    img_url=db.Column(db.String,nullable=False)
    
class Book_catalogue(db.Model):
    __tablename__='book_catalogue'
    auth_fname=db.Column(db.VARCHAR,nullable=False)
    auth_lname=db.Column(db.VARCHAR)
    title=db.Column(db.VARCHAR)
    publisher=db.Column(db.VARCHAR)
    year=db.Column(db.VARCHAR)
    ISBN_no=db.Column(db.Integer,primary_key=True,autoincrement=True)
    section_id=db.Column(db.Integer,db.ForeignKey(Section.section_id))
    no_of_pages=db.Column(db.Integer)
    book_img_url=db.Column(db.String)
    pdf_link=db.Column(db.String)
    
   
class Book_issue(db.Model):
    __tablename__='book_issue'
    user_id=db.Column(db.Integer,db.ForeignKey(User.user_id),primary_key=True)
    ISBN_no=db.Column(db.Integer,db.ForeignKey(Book_catalogue.ISBN_no),primary_key=True)
    doi=db.Column(db.DateTime)
    request_date=db.Column(db.DateTime)
    return_date=db.Column(db.DateTime)
    due_date=db.Column(db.DateTime)
    feedback=db.Column(db.VARCHAR)
    rating=db.Column(db.Integer)
    status=db.Column(db.String(128))
    re_issue=db.Column(db.Integer,default=1)
    
class Schedule(db.Model):
    __tablename__="schedule"
    id=db.Column(db.String(128),db.ForeignKey(User.user_id),primary_key=True)
    timing=db.Column(db.String(128),default=None)
    
