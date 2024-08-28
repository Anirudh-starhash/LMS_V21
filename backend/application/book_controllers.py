from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import Book_catalogue,Book_issue,User,Section
from application.database import db
from datetime import timedelta,datetime
from flask import current_app as app
from flask_caching import Cache
cache=Cache(app)

book_blueprint=Blueprint("book",__name__)


    
@cache.cached(timeout=60)        
@book_blueprint.route("/addBook",methods=['POST','GET'])
def addBook():
    data=request.get_json()
    title=data.get("title")
    date=data.get("date") 
    no_of_pages=data.get("no_of_pages")
    img_url=data.get("img_url")
    pdf_link=data.get("pdf_link")
    auth_fname=data.get("auth_fname")
    auth_lname=data.get("auth_lname")
    publisher=data.get("publisher")
    id=data.get("id")
    
    s=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.title==title)).scalar()
    
    if s==None:
        book=Book_catalogue(title=title,year=date,no_of_pages=no_of_pages,book_img_url=img_url,pdf_link=pdf_link,auth_fname=auth_fname,auth_lname=auth_lname,publisher=publisher,section_id=id)
        db.session.add(book)
        db.session.commit()
    
        return jsonify({
          'msg':'Added successfully'
        }),200
        
    else:
        return jsonify({
            'msg':'Book already exists'
        }),201
        
    
@cache.cached(timeout=60)     
@book_blueprint.route("/editBook",methods=['POST','GET'])
def editBook():
    data=request.get_json()
    title=data.get("title")
    date=data.get("date") 
    no_of_pages=data.get("no_of_pages")
    img_url=data.get("img_url")
    pdf_link=data.get("pdf_link")
    auth_fname=data.get("auth_fname")
    auth_lname=data.get("auth_lname")
    publisher=data.get("publisher")
    id=data.get("id")
    isbn=data.get("isbn")
    
    s=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.ISBN_no==isbn)).scalar()
    
    if s==None:
    
        return jsonify({
          'msg':'No Book!'
        }),201
        
    else:
        s.no_of_pages=no_of_pages
        s.auth_lname=auth_lname
        s.auth_fname=auth_fname
        s.publisher=publisher
        s.book_img_url=img_url
        s.pdf_link=pdf_link
        s.year=date
        s.title=title
        db.session.commit()
        return jsonify({
            'msg':'Book Edit Successful!'
        }),200
        
@cache.cached(timeout=60) 
@book_blueprint.route("/getBook/<int:ISBN>",methods=['GET','POST'])
def getBook(ISBN):
    book=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.ISBN_no==ISBN)).scalar()
    book_info={
        'title':book.title,
        'date':book.year,
        'auth_fname':book.auth_fname,
        'auth_lname':book.auth_lname,
        'publisher':book.publisher,
        'no_of_pages':book.no_of_pages,
        'img_url':book.book_img_url,
        'pdf_link':book.pdf_link
    }
    
    return jsonify({
        'msg':'Retrieved Easily',
        'book_info':book_info
    }),200
    
@cache.cached(timeout=60) 
@book_blueprint.route("/getBooks",methods=['GET','POST'])
def getBooks():
    books=db.session.execute(db.select(Book_catalogue)).scalars().all()
    book_info=[]
    for book in books:
        book_info.append({
            'id':book.section_id,
            'title':book.title,
            'date':book.year,
            'auth_fname':book.auth_fname,
            'auth_lname':book.auth_lname,
            'publisher':book.publisher,
            'no_of_pages':book.no_of_pages,
            'img_url':book.book_img_url,
            'pdf_link':book.pdf_link,
            'ISBN':book.ISBN_no
        })
    
    return jsonify({
        'msg':'Success',
        'books':book_info
    }),200

@cache.cached(timeout=60)     
@book_blueprint.route("/getAllReviews/<int:user_id>/<int:id>",methods=['GET','POST'])
def getReviews(user_id,id):
    books_info=db.session.execute(db.select(Book_issue).where(Book_issue.ISBN_no==id)).scalars().all()
    print(books_info)
    reviews=[]
    if books_info==[]:
        return jsonify({
            'msg':'Currently no information Do visit Later'
        }),201
    
    else:
        yes=False
        for x in books_info:
            print(x.user_id)
            if x.return_date!=None:
                user=db.session.execute(db.Select(User).where(User.user_id==x.user_id)).scalar()
                if x.user_id==user_id: 
                    yes=True
                reviews.append({
                    'user_id':x.user_id,
                    'name':user.user_fname+" "+user.user_lname,
                    'ISBN':x.ISBN_no,
                    'feedback':x.feedback,
                    'rating':x.rating,
                    "is_him":yes
                });
        return jsonify({
            'reviews':reviews
        }),200
        
@cache.cached(timeout=60) 
@book_blueprint.route("/getAReview/<int:user_id>/<int:id>",methods=['GET','POST'])
def getAReview(user_id,id):
    x=db.session.execute(db.select(Book_issue).where(Book_issue.ISBN_no==id).where(Book_issue.user_id==user_id)).scalar()
    reviews={}
    if x==[]:
        return jsonify({
            'msg':'Currently no information Do visit Later'
        }),201
    
    else:
        if x.return_date!=None:
            user=db.session.execute(db.Select(User).where(User.user_id==x.user_id)).scalar()
            reviews={
                'user_id':x.user_id,
                'name':user.user_fname+" "+user.user_lname,
                'ISBN':x.ISBN_no,
                'feedback':x.feedback,
                'rating':x.rating,
                "is_him":True
            };
        return jsonify({
            'reviews':reviews
        }),200
        
@cache.cached(timeout=60) 
@book_blueprint.route("/deleteReview",methods=['GET','POST'])
def deleteReview():
    data=request.get_json()
    user_id=data.get("user_id")
    book_id=data.get("book_id")
    
    status=db.session.execute(db.Select(Book_issue).where(Book_issue.user_id==user_id).where(Book_issue.ISBN_no==book_id)).scalar()
    if status==None:
        return jsonify({
            'msg':'Some Error!'
        }),201
        
    else:
        status.feedback="";
        status.rating=""
        db.session.commit()
        
        return jsonify({
            'msg':'Success!'
        }),200
    
    
@book_blueprint.route("/deleteBook",methods=['GET','POST'])
def deleteBook():
    data=request.get_json()
    book_id=data.get("book_id")
    info=db.session.execute(db.Select(Book_issue).where(Book_issue.ISBN_no==book_id)).scalars().all()
    
    if info!=[]:
        # means book is being associated with some users
        for x in info:
            if x.request_date!=None:
                user=db.session.execute(db.Select(User).where(User.user_id==x.user_id)).scalar()
                if user.count==1: user.count=None
                else: user.count-=1
                x.re_issue=0
                db.session.delete(x)
                db.session.commit()
                
            elif x.doi!=None:
                user=db.session.execute(db.Select(User).where(User.user_id==x.user_id)).scalar()
                if user.count==1: user.count=None
                else: user.count-=1
                x.return_date=datetime.today()
                x.re_issue=0
                x.doi=None
                x.due_date=None
                x.status='Book is deleted by Librarian so returned abruptly to get deleted!'
                db.session.commit()
            
            else:
                x.status='Returned Book deleted by Librarian can\'t be re-issued'
                x.re_issue=0
                db.session.commit()
                
        
    book_info=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.ISBN_no==book_id)).scalar()
    print(book_id)
    if book_info==None:
        return jsonify({
            'msg':'Some Error!'
        }),201
        
    db.session.delete(book_info)
    db.session.commit()
    
    return jsonify({
        'msg':'Book deleted!'
    }),200
    
@book_blueprint.route("/getBooks/<string:section_name>",methods=['GET','POST'])
def getBooksSection(section_name):
    s=db.session.execute(db.select(Section).where(Section.title==section_name)).scalar()
    if s==None:
        return jsonify({
            'msg':'Some Error!'
        }),201
    
    else:
        books=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.section_id==s.section_id)).scalars().all()
        books_info=[]
        for book in books:
            books_info.append({
                'id':book.section_id,
                'title':book.title,
                'date':book.year,
                'auth_fname':book.auth_fname,
                'auth_lname':book.auth_lname,
                'publisher':book.publisher,
                'no_of_pages':book.no_of_pages,
                'img_url':book.book_img_url,
                'pdf_link':book.pdf_link,
                'ISBN':book.ISBN_no
            })
            
        return jsonify({
            "books":books_info
        }),200
                
@book_blueprint.route("/getBooksA/<string:auth_name>",methods=['GET','POST'])
def getBooksAuth(auth_name):
    names=auth_name.split("_")
    b=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.auth_fname==names[0]).where(Book_catalogue.auth_lname==names[1])).scalars().all()
    if b==[]:
        return jsonify({
            'msg':'Some Error!'
        }),201
    
    else:
        books_info=[]
        for book in b:
            books_info.append({
                'id':book.section_id,
                'title':book.title,
                'date':book.year,
                'auth_fname':book.auth_fname,
                'auth_lname':book.auth_lname,
                'publisher':book.publisher,
                'no_of_pages':book.no_of_pages,
                'img_url':book.book_img_url,
                'pdf_link':book.pdf_link,
                'ISBN':book.ISBN_no
            })
            
        return jsonify({
            "books":books_info
        }),200
                
@book_blueprint.route("/getParticularBook/<string:book_name>",methods=['GET','POST'])
def getBooksP(book_name):
    names=book_name.split("_")
    new_book=names[0]+" "+names[1]
    book=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.title==new_book)).scalar()
    if book==None:
        return jsonify({
            'msg':'Some Error!'
        }),201
    
    else:
        books_info=[]
        books_info.append({
            'id':book.section_id,
            'title':book.title,
            'date':book.year,
            'auth_fname':book.auth_fname,
            'auth_lname':book.auth_lname,
            'publisher':book.publisher,
            'no_of_pages':book.no_of_pages,
            'img_url':book.book_img_url,
            'pdf_link':book.pdf_link,
            'ISBN':book.ISBN_no
        })

         
            
        return jsonify({
            "books":books_info
        }),200
                
        

