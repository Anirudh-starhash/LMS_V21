from flask import Blueprint, jsonify, request, Flask
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import Librarian,Book_issue,Book_catalogue,User,Section
from application.database import db
from datetime import timedelta,datetime
from celery import shared_task
from fpdf import *
from flask_mail import Mail, Message
from celery.contrib.abortable import AbortableTask
from application.tasks import *
import smtplib,os
lib_blueprint=Blueprint("lib",__name__)

#admin_login  
@lib_blueprint.route("/admin_login",methods=['GET','POST'])
def admin_login():
    if request.method=="POST":
        data=request.get_json()
        email=data.get("email")
        password=data.get("password")
        
        lib=db.session.execute(db.select(Librarian).where(Librarian.librarian_email==email)).scalar()
        if lib is None:
            return jsonify({
                'message':'Incorrect Credentials Librarian Does\'nt exist with this email id', 
            }),201
        
        if lib.password!=password:
            return jsonify({
                'message':'Wrong Password!', 
            }),202
        
        access_token=create_access_token(identity=lib.librarian_id,expires_delta=timedelta(days=1))
        info={
            'id':lib.librarian_id,
            'email':lib.librarian_email,
            'role':'admin'
        }
        
        return jsonify({
            'access_token':access_token,
            'info':info,
        }),200
        
        
@lib_blueprint.route("/admin_logout",methods=['GET','POST'])
@jwt_required()
def admin_logout():
    if request.method=="POST":
        response=jsonify({
            'message':'Logged out Successfully'
        })
        
        unset_jwt_cookies(response)
        return response,200
    
@lib_blueprint.route("/lib_check_permission",methods=['GET','POST'])
@jwt_required()

def is_permitted():
    lib_identity=get_jwt_identity()
    lib=Librarian.query.get(lib_identity)
    print(lib)
    
    
    if lib:
        response= jsonify({
            'msg':'Access Granted'
        })
        unset_jwt_cookies(response)
        return response,200
    
    else:
        response= jsonify({
            'msg':'Access Denied'
        })
        unset_jwt_cookies(response)
        return response,201
        
        
@lib_blueprint.route("/getAllRequests",methods=['GET','POST'])
def getRequests():
    bi_info=db.session.execute(db.Select(Book_issue)).scalars().all()
    if bi_info==[]:
        return jsonify({
            'msg':'Currently no info dude!'
        }),201
    else:
        issued_books=[]
        requested_books=[]
        returned_books=[]
        
        for x in bi_info:
            b=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.ISBN_no==x.ISBN_no)).scalar()
            if x.doi!=None:
                if datetime.today()<x.due_date:
                    if b!=None:
                        issued_books.append({
                            'user_id':x.user_id,
                            'title':b.title,
                            'ISBN':x.ISBN_no,
                            'issue_date':x.doi,
                            'due_date':x.due_date
                        })
                    else:
                        issued_books.append({
                            'user_id':x.user_id,
                            'title':'Deleted Book By You',
                            'ISBN':x.ISBN_no,
                            'issue_date':x.doi,
                            'due_date':x.due_date
                        })
                        
                else:
                    x.issue_date=None
                    x.return_date=datetime.today()
                    db.session.commit()
                
            if x.return_date!=None:
                if b!=None:
                    returned_books.append({
                        'user_id':x.user_id,
                        'title':b.title,
                        'ISBN':x.ISBN_no,
                        'return_date':x.return_date,
                        'status':x.status,
                        "re_issue":x.re_issue
                    })
                else:
                    returned_books.append({
                        'user_id':x.user_id,
                        'title':'Deleted Book By You',
                        'ISBN':x.ISBN_no,
                        'return_date':x.return_date,
                        'status':x.status,
                        "re_issue":x.re_issue
                    })
                    
                
            if x.request_date!=None:
                if b!=None:
                    requested_books.append({
                        'user_id':x.user_id,
                        'title':b.title,
                        'ISBN':x.ISBN_no,
                        'request_date':x.request_date,
                    })
                else:
                    requested_books.append({
                        'user_id':x.user_id,
                        'title':'Deleted Book by You',
                        'ISBN':x.ISBN_no,
                        'request_date':x.request_date,
                    })
                    
        return jsonify({
            'msg':'All updates Successfull!',
            'issued_books':issued_books,
            'requested_books':requested_books,
            'returned_books':returned_books
        }),200
        
    
@lib_blueprint.route("/grantBook",methods=['GET','POST'])
def grantBook():
    data=request.get_json()
    user_id=data.get("user_id")
    book_id=data.get("book_id")
    
    status=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==user_id).where(Book_issue.ISBN_no==book_id)).scalar()
    
    if status.request_date!=None:
        status.doi=datetime.today()
        user=db.session.execute(db.select(User).where(User.user_id==user_id)).scalar()
        if(user.type=="ug"):
            status.due_date=status.doi+timedelta(days=7)
        elif(user.type=="pg"):
            status.due_date=status.doi+timedelta(days=8)
        elif user.type=="phd":
            status.due_date=status.doi+timedelta(days=9)
        
        elif user.type=="rs":
            status.due_date=status.doi+timedelta(days=10)
        
        else:
            status.due_date=status.doi+timedelta(days=11)
        
        status.request_date=None
        db.session.commit()
        
        return jsonify({
            'msg':'Successfully!',
        }),200
    else:
        return jsonify({
            'msg':'Some Error'
        }),201

@lib_blueprint.route("/rejectBook",methods=['GET','POST'])
def rejectBook():
    data=request.get_json()
    user_id=data.get("user_id")
    book_id=data.get("book_id")
    
    status=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==user_id).where(Book_issue.ISBN_no==book_id)).scalar()
    
    if status!=None:
        db.session.delete(status)
        db.session.commit()
        
        user=db.session.execute(db.Select(User).where(User.user_id==user_id)).scalar()
        if(user.count==1): user.count=None
        else: user.count-=1
        
        db.session.commit()
        
        return jsonify({
            'msg':'reject Successfully done!',
        }),200
    else:
        return jsonify({
            'msg':'Some Error'
        }),201
        
        
@lib_blueprint.route("/revokeBook",methods=['GET','POST'])
def revokeBook():
    data=request.get_json()
    user_id=data.get("user_id")
    book_id=data.get("book_id")
    days_left=data.get("days_left")
    
    status=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==user_id).where(Book_issue.ISBN_no==book_id)).scalar()
    
    if status==None:
        return jsonify({
            'msg':'Some Error!'
        }),201
        
    else:
        status.return_date=datetime.today()
        status.doi=None
        status.status=f"Revoked By librarian before {days_left} days!"
        status.due_date=None
        
        user=db.session.execute(db.Select(User).where(User.user_id==user_id)).scalar()
        if(user.count==1): user.count=None
        else: user.count-=1
        
        db.session.commit()
        
        return jsonify({
            'msg':'Success!'
        }),200
        
@lib_blueprint.route("/getAllUserDetails",methods=['GET','POST'])
def getAllUserDetails():
    u=db.session.execute(db.Select(User)).scalars().all()
    user_list=[]
    for user in u:
        info=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==user.user_id)).scalars().all()
        issued_count=0
        req_count=0
        return_count=0
        for x in info:
            if x.doi!=None:
                issued_count+=1
            elif x.return_date!=None:
                return_count+=1
            else:
                req_count+=1
                
        user_list.append({
            'user_id':user.user_id,
            'email':user.user_email,
            'name':user.user_fname+" "+user.user_lname,
            "type":user.type,
            'profile_pic':user.profile_pic,
            'issued_count':issued_count,
            'req_count':req_count,
            'return_count':return_count
        })
    
    return jsonify({
        'user_list':user_list,
        'msg':'Success!'
    }),200
    
@lib_blueprint.route("/getDetails",methods=['GET','POST'])
def getDetails():
    s=db.session.execute(db.Select(Book_catalogue)).scalars()
    section_info={}
    for x in s:
        section_name=db.session.execute(db.select(Section).where(Section.section_id==x.section_id)).scalar()
        if section_name.title not in section_info:
            section_info[section_name.title]=1
        else:
            section_info[section_name.title]+=1
        
    return jsonify({
        'section_info':section_info
    }),200
    
@lib_blueprint.route('/generate_report', methods=['GET','POST'])
def generate_report():
    job=send_activity_report().delay()
    result=job.wait()
    return jsonify({
        'status': 'Report generation started!',
        'result':result
    }),200


  
