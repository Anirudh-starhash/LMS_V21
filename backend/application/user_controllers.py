from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import User,Book_issue,Book_catalogue,Section,Schedule
from application.database import db
from datetime import timedelta,datetime
from flask import current_app as app,Flask
from flask_caching import Cache
from celery import shared_task
from fpdf import *
from flask_mail import Mail, Message
from celery.contrib.abortable import AbortableTask
from application.tasks import *
from celery.result import AsyncResult
# above things are imports 


app=Flask(__name__)
user_blueprint=Blueprint("user",__name__)
cache=Cache(app)
@user_blueprint.route("/",methods=['GET','POST'])
def hello():
    return jsonify({
        'msg':'Hello You are connected from Backend!'
    })
    
# initialization stuff
    
#user_register
@user_blueprint.route("/user_register",methods=['GET','POST'])
def user_register():
    if request.method=="POST":
        data=request.get_json()
        email=data.get("email")
        password=data.get("password")
        firstname=data.get("firstname")
        lastname=data.get("lastname")
        type=data.get("type")
        profile_pic=data.get("profile_pic")
        
        hashed_password=generate_password_hash(password,method='pbkdf2:sha256',salt_length=8)
        
        u=db.session.execute(db.select(User).where(User.user_email==email)).scalar()
        # print(u.user_email)
        
        if u is None:
            # means a new user
            
            new_user=User(user_email=email,
                          password=hashed_password,
                          user_fname=firstname,
                          user_lname=lastname,
                          type=type,
                          profile_pic=profile_pic)
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({
                'msg':'Registered Successful!'
            }),200
        
        else:
            return jsonify({
                'msg':'Oops! You are already registered go to login page!'
            }),201
        
        
#user_login
@user_blueprint.route("/user_login",methods=['GET','POST'])
def user_login():
    if request.method=="POST":
        data=request.get_json()
        email=data.get("email")
        password=data.get("password")
        
        u=db.session.execute(db.select(User).where(User.user_email==email)).scalar()
        if u is None:
            return jsonify({
                'message':'Incorrect Credentials User Does\'nt exist with this email id', 
            }),201
        
        if not check_password_hash(u.password,password):
            return jsonify({
                'message':'Wrong Password!', 
            }),202
        
        access_token=create_access_token(identity=u.user_id,expires_delta=timedelta(days=1))
        info={
            'id':u.user_id,
            'email':u.user_email,
            'name':u.user_fname+" "+u.user_lname,
            'role':'user'
        }
        
        return jsonify({
            'access_token':access_token,
            'info':info,
        }),200
        
#user_logout      
@user_blueprint.route("/user_logout",methods=['GET','POST'])
@jwt_required()

def user_logout():
    if request.method=="POST":
        response=jsonify({
            'message':'Logged out Successfully'
        })
        
        unset_jwt_cookies(response)
        return response,200
    
#user_check_permission
@user_blueprint.route("/user_check_permission",methods=['GET','POST'])
@jwt_required()

def is_permitted():
    user_identity=get_jwt_identity()
    user=User.query.get(user_identity)
    
    if user:
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
    
#user_info
    
@user_blueprint.route("/getInfo/<int:id>",methods=['GET','POST'])
def getInfo(id):
    books=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==id)).scalars().all()
    if books==[]:
        return jsonify({
            'msg':'Currently no info dude!'
        }),201
    
    else:
        issued_books=[]
        requested_books=[]
        returned_books=[]
        
        for x in books:
            b=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.ISBN_no==x.ISBN_no)).scalar()
            if x.doi!=None:
                if datetime.today()<x.due_date:
                    if b!=None:
                        issued_books.append({
                            'title':b.title,
                            'ISBN':x.ISBN_no,
                            'issue_date':x.doi,
                            'pdf':b.pdf_link,
                            'due_date':x.due_date
                        })
                    else:
                        issued_books.append({
                            'title':'Deleted Book',
                            'ISBN':x.ISBN_no,
                            'issue_date':x.doi,
                            'pdf':'Deleted PDF',
                            'due_date':x.due_date
                        })
                        
                else:
                    x.issue_date=None
                    x.return_date=datetime.today()
                    x.status=f"Returned Automatically as due_date passed!"

                    db.session.commit()
                
            if x.return_date!=None:
                if b!=None:
                    returned_books.append({
                        'title':b.title,
                        'ISBN':x.ISBN_no,
                        'return_date':x.return_date,
                        'status':x.status,
                        "re_issue":x.re_issue
                    })
                else:
                    returned_books.append({
                        'title':'Deleted Book',
                        'ISBN':x.ISBN_no,
                        'return_date':x.return_date,
                        'status':x.status,
                        "re_issue":x.re_issue
                    })
                    
                
            if x.request_date!=None:
                if b!=None:
                    requested_books.append({
                        'title':b.title,
                        'ISBN':x.ISBN_no,
                        'request_date':x.request_date,
                    })
                else:
                    requested_books.append({
                        'title':'Deleted Book',
                        'ISBN':x.ISBN_no,
                        'request_date':x.request_date,
                    })
                    
        return jsonify({
            'msg':'All updates Successfull!',
            'issued_books':issued_books,
            'requested_books':requested_books,
            'returned_books':returned_books
        }),200
        
#request a book
@user_blueprint.route("/request_book",methods=['GET','POST'])
def request_book():
    # check whether is this user eligible to take a book
    data=request.get_json()
    user_id=data.get("user_id")
    book_id=data.get("book_id")
    
    status=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==user_id).where(Book_issue.ISBN_no==book_id)).scalar()
    print(status)
    if status==None:
        is_eligible=False
        user=db.session.execute(db.select(User).where(User.user_id==user_id)).scalar()
        
        if user.count==None:
            user.count=1
            db.session.commit()
            is_eligible=True
            
        elif user.count<5:
            user.count+=1
            db.session.commit()
            is_eligible=True
            
        if is_eligible:
            request_date=datetime.today()
            new_instruction=Book_issue(user_id=user_id,ISBN_no=book_id,request_date=request_date)
            db.session.add(new_instruction)
            db.session.commit()
            
            return jsonify({
                'msg':'Request registered Successfully!'
            }),200
        
        else:
            return jsonify({
                'msg':'Max requests Sent!'
            }),202
            
    elif status.request_date==None and status.doi==None:
            status.request_date=datetime.today()  
            status.return_date=None
            status.feedback=None
            status.rating=None
            db.session.commit()
            return jsonify({
                'msg':'Request registered Successfully!'
            }),200
            
    else:
        return jsonify({
            'msg':'This pair of the user and the book are related by some means\
                eitherissued or requested etc!'
        }),201
        
#withdraw a book     
@user_blueprint.route("/withDrawBook",methods=['GET','POST'])
def withDraw():
    data=request.get_json()
    user_id=data.get("user_id")
    book_id=data.get("book_id")
    
    status=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==user_id).where(Book_issue.ISBN_no==book_id)).scalar()
    if status==None:
        return jsonify({
            'msg':'Some error!'
        }),201
        
    else:
        user=db.session.execute(db.select(User).where(User.user_id==user_id)).scalar()
        if user.count==1:
            user.count=None
            db.session.commit()
        else:
            user.count-=1
            db.session.commit()
            
        db.session.delete(status)
        db.session.commit()
        
        return jsonify({
            'msg':'Withdraw Successful!'
        }),200
        
#return a book
@user_blueprint.route("/returnBook",methods=['GET','POST'])
def retrunBook():
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
        if days_left>0:
            status.status=f"Returned before due_date by {days_left} days!"
        
        status.doi=None
        status.due_date=None
        db.session.commit()
        # updated in book_issue now in user count too
        
        user=db.session.execute(db.Select(User).where(User.user_id==user_id)).scalar()
        
        if(user.count==1): user.count=None
        else:  user.count-=1
        
        db.session.commit()
        
        return jsonify({
            'msg':'return successfull!'
        }),200
        
#submit a review
@user_blueprint.route("/submitReview",methods=['GET','POST'])
def submitReview():
    data=request.get_json()
    user_id=data.get("user_id")
    book_id=data.get("book_id")
    rating=data.get("ratings")
    feedback=data.get("review")
    
    status=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==user_id).where(Book_issue.ISBN_no==book_id)).scalar()
    
    if status==None:
        return jsonify({
            'msg':'Some Error!'
        }),201
        
    else:
        status.feedback=feedback
        status.rating=rating
        db.session.commit()
        # updated in book_issue now in user count too
        
      
        
        return jsonify({
            'msg':'return successfull!'
        }),200
        

        
#reissue a book
@user_blueprint.route("/reissue",methods=['GET','POST'])
def reissue():
    data=request.get_json()
    user_id=data.get("user_id")
    book_id=data.get("book_id")
    
    status=db.session.execute(db.select(Book_issue).where(Book_issue.user_id==user_id).where(Book_issue.ISBN_no==book_id)).scalar()
    
    if status!=None:
        status.return_date=None
        status.request_date=datetime.today()
        status.feedback=None
        status.rating=None
        db.session.commit()
        
        user=db.session.execute(db.Select(User).where(User.user_id==user_id)).scalar()
        if user.count==None:
            user.count=1
        else:
            user.count+=1
        
        db.session.commit()
            
        return jsonify({
            'msg':'Request registered Successfully!'
        }),200
            
    
    else:
        return jsonify({
            'msg':'Some Error!'
        }),201
    
#get Profile   
@user_blueprint.route("/getProfile/<int:id>",methods=['GET','POST'])
def getProfile(id):
    user=db.session.execute(db.Select(User).where(User.user_id==id)).scalar()
    
    if user==None:
        return jsonify({
            'msg':'Some Error!'
        }),201
        
    else:
        profile_details={
            'user_id':user.user_id,
            'name':user.user_fname+" "+user.user_lname,
            'firstname':user.user_fname,
            'lastname':user.user_lname,
            'profile_pic':user.profile_pic,
            'type':user.type,
            'email':user.user_email,
        }
        return jsonify({
            'profile_details':profile_details
        }),200
        
#edit_profile
@user_blueprint.route("/edit_profile",methods=['GET','POST'])
def edit_profile():
    data=request.get_json()
    id=data.get("id")
    firstname=data.get("firstname")
    lastname=data.get("lastname")
    email=data.get("email")
    type=data.get("type")
    profile_pic=data.get("profile_pic")
    
    user=db.session.execute(db.Select(User).where(User.user_id==id)).scalar()
    
    if user==None:
        return jsonify({
            'msg':'Some Error!'
        }),201
        
    else:
        user.profile_pic=profile_pic
        user.user_fname=firstname
        user.user_lname=lastname
        user.user_email=email
        user.type=type
        db.session.commit()
        
        return jsonify({
            'msg':'Success!'
            
        }),200
    
#get info of a book
@user_blueprint.route("/getinfoOfABook/<int:book_id>/<int:user_id>",methods=['GET','POST'])
def getInfoOfABook(book_id,user_id):
    book=db.session.execute(db.Select(Book_issue).where(Book_issue.ISBN_no==book_id).where(Book_issue.user_id==user_id)).scalar()
    get_info=""
    if book.due_date!=None and datetime.today()<book.due_date:
        get_info=f'Due Date of this Book is {book.due_date.strftime("%Y-%m-%d")}\nThere are still {(book.due_date - datetime.today()).days} days left'
        days_left= (book.due_date - datetime.today()).days         
        
        return jsonify({
            'get_info':get_info,
            "days_left":days_left
        }),200
        
    else:
        return jsonify({
            'msg':'Success!'
        }),200
        
#Names of book authors
@user_blueprint.route("/getNames",methods=['GET','POST'])
def getnames():
    sec=db.session.execute(db.select(Section)).scalars().all()
    boo=db.session.execute(db.select(Book_catalogue)).scalars().all()
    
    auth_names=[]
    book_names=[]
    section_names=[]
    
    if sec==[] or boo==[]:
        return jsonify({
            'msg':'Some Error!'
        }),201
    
    for x in sec:
        section_names.append({
            "id":x.section_id,
            "name":x.title
        })
        
    for y in boo:
        auth_names.append({
            "id":y.ISBN_no,
            "name":y.auth_fname+" "+y.auth_lname
        })
        
        book_names.append({
            "id":y.ISBN_no,
            "name":y.title
        })

    return jsonify({
        'msg':'Success',
        "sections":section_names,
        "books":book_names,
        "authors":auth_names
    }),200

# get Particular User details    
@user_blueprint.route("/getUserDetails/<int:id>",methods=['GET','POST'])
def getUserDetails(id):
    bi=db.session.execute(db.Select(Book_issue).where(Book_issue.user_id==id)).scalars().all()
    req_books=0
    returned_books=0
    issued_books=0
    
    for x in bi:
        if x.request_date!=None:
            req_books+=1
        
        elif x.doi!=None:
            issued_books+=1
            
        else:
            returned_books+=1
    list={
        'issued_books':issued_books,
        'returned_books':returned_books,
        'requested_books':req_books
    } 
    return jsonify({
        'section_info':list
    }),200
    
#Change_password
@user_blueprint.route("/change_password",methods=['GET','POST'])
def change_password():
    data=request.get_json()
    id=data.get("id")
    password=data.get("new_password")
    old_password=data.get("old_password")
    u=db.session.execute(db.Select(User).where(User.user_id==id)).scalar()
    if check_password_hash(u.password,old_password):
        u.password=generate_password_hash(password,method='pbkdf2:sha256',salt_length=8)
        db.session.commit()
        
        return jsonify({
            'msg':'Password changed! Successful!'
        }),200
        
    else:
        return jsonify({
            'msg':'Password not same'
        }),201
        
        
#getRemainder regarding when to send email
@user_blueprint.route("/getRemainder/<int:user_id>",methods=['GET','POST'])
def getRemainder(user_id):
    x=db.session.execute(db.Select(Schedule).where(Schedule.id==user_id)).scalar()
    print(x)
    if x==None:
        # means still user not set a remainder
        rem=Schedule(id=user_id)
        db.session.add(rem)
        db.session.commit()
        
        return jsonify({
            'msg':'Not Set Yet',
            "time":"",
        }),200
        
    else:
        if x.timing==None:
             return jsonify({
                 'time':"",
             }),200
        else:
            return jsonify({
                'time':x.timing
            }),200
            
#set Timing for a email to sent
            
@user_blueprint.route("/setTiming/<int:user_id>",methods=['GET','POST'])
def setTiming(user_id):
    data=request.get_json()
    time=data.get("time")
    x=db.session.execute(db.Select(Schedule).where(Schedule.id==user_id)).scalar()
    x.timing=time
    db.session.commit()
    
    return jsonify({
        'msg':'Success',
        'time':time
        
    }),200
    
# sendEmail 
@user_blueprint.route("/sendEmail/<int:id>",methods=['GET','POST'])
def sendEmail(id):
    try:
        # Trigger the Celery task
        get_activity(id)
        
        # Return the task ID to the client
        return jsonify({
            'status': 'Done',
        }), 200
    except Exception as e:
        # Log the exception
        app.logger.error(f"Error starting task: {str(e)}")
        
        # Return an error response
        return jsonify({
            'status': 'Error',
            'message': 'An error occurred while starting the task.'
        }), 500
    




   

    

    
    
    
    
    