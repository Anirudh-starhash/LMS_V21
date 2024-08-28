from flask import Blueprint, jsonify, request
from application.models import Section,Book_catalogue,Book_issue,User
from application.database import db
from datetime import datetime
from flask_caching import Cache



sec_blueprint=Blueprint("sec",__name__)


@sec_blueprint.route("/getSections",methods=['GET','POST'])
def get():
    sec=db.session.execute(db.select(Section)).scalars().all()
    section_info=[]
    for x in sec:
        section_info.append({
            'id':x.section_id,
            'title':x.title,
            'date':x.date,
            'description':x.description,
            'img_url':x.img_url
        })
    # print(section_info)
    return jsonify({
        'sections':section_info
    }),200
    

@sec_blueprint.route("/getSection/<int:id>",methods=['GET','POST'])
def get_sec(id):
    sec=db.session.execute(db.select(Section).where(Section.section_id==id)).scalar()
    section_info={
            'id':sec.section_id,
            'title':sec.title,
            'date':sec.date,
            'description':sec.description,
            'img_url':sec.img_url
    }
    # print(section_info)
    return jsonify({
        'section_info':section_info
    }),200
    
     
@sec_blueprint.route("/addSection",methods=['POST','GET'])
def add():
    data=request.get_json()
    title=data.get("title")
    date=data.get("date") 
    description=data.get("description")
    img_url=data.get("img_url")
    
    s=db.session.execute(db.select(Section).where(Section.title==title)).scalar()
    
    if s==None:
        section=Section(title=title,date=date,description=description,img_url=img_url)
        db.session.add(section)
        db.session.commit()
    
        return jsonify({
          'msg':'Added successfully'
        }),200
        
    else:
        return jsonify({
            'msg':'Section already exists'
        }),201
        

@sec_blueprint.route("/editSection/<int:id>",methods=['POST','GET'])
def edit(id):
    data=request.get_json()
    title=data.get("title")
    date=data.get("date") 
    description=data.get("description")
    img_url=data.get("img_url")
    
    s=db.session.execute(db.select(Section).where(Section.section_id==id)).scalar()
    
    if s==None:
        return jsonify({
          'msg':'Section Does\'nt exist'
        }),201
        
    else:
        s.title=title
        s.date=date
        s.description=description
        s.img_url=img_url
        db.session.commit()
        return jsonify({
            'msg':'Editted Successfully!'
        }),200
        

@sec_blueprint.route("/getBooks/<int:id>",methods=['GET','POST'])
def getBooks(id):
    books=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.section_id==id)).scalars().all()
    
    section_info=[]
    for x in books:
        section_info.append({
            'id':x.section_id,
            'title':x.title,
            'date':x.year,
            'no_of_pages':x.no_of_pages,
            'img_url':x.book_img_url,
            'auth_fname':x.auth_fname,
            'auth_lname':x.auth_lname,
            'publisher':x.publisher,
            'ISBN':x.ISBN_no
        })
    # print(section_info)
    return jsonify({
        'sections':section_info
    }),200
    

@sec_blueprint.route("/deleteSection",methods=['GET','POST'])
def deleteSection():
    data=request.get_json()
    section_id=data.get("section_id")
    sec=db.session.execute(db.select(Section).where(Section.section_id==section_id)).scalar()
    info=db.session.execute(db.select(Book_catalogue).where(Book_catalogue.section_id==section_id)).scalars().all()
    if sec==None:
        return jsonify({
            'msg':'Already Deleted!'
        }),202
        
    if info==None:
        db.session.delete(sec)
        return jsonify({
            'msg':'No Books'
        }),200
        
    else:
        for book in info:
            book_info=db.session.execute(db.select(Book_issue).where(Book_issue.ISBN_no==book.ISBN_no)).scalars().all()
            if book_info!=[]:
            # means book is being associated with some users
                for x in book_info:
                    if x.request_date!=None:
                        user=db.session.execute(db.Select(User).where(User.user_id==x.user_id)).scalar()
                        if(user.count==1): user.count=None
                        else: user.count-=1
                        x.re_issue=0
                        db.session.delete(x)
                        db.session.commit()
                        
                    elif x.doi!=None:
                        user=db.session.execute(db.Select(User).where(User.user_id==x.user_id)).scalar()
                        if(user.count==1): user.count=None
                        else: user.count-=1
                        x.return_date=datetime.today()
                        x.re_issue=0
                        x.doi=None
                        x.due_date=None
                        x.status='Section is deleted by Librarian so book is returned abruptly to get deleted along with Section!'
                        db.session.commit()
                    
                    else:
                        x.status='Returned Book deleted by Librarian can\'t be re-issued as This Section does\'nt exist!'
                        x.re_issue=0
                        db.session.commit()
                
            db.session.delete(book)
            db.session.commit()
            
        
        db.session.delete(sec)
        db.session.commit()
        
        return jsonify({
            'msg':'Section Deleted!'
        }),200
                
               
            