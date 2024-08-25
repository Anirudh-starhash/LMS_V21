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
import smtplib,os
from PIL import Image
from fpdf import FPDF
from PIL import Image
import os

#PDF class
class PDF(FPDF):
    def header(self):
        self.set_fill_color(240, 248, 255)
        self.rect(0, 0, 210, 297, 'F')
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Activity Report', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def is_valid_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                return img.format.lower() in ['png', 'jpeg', 'jpg', 'webp']
        except IOError:
            return False

    def add_profile_picture(self, pic_path):
        if os.path.exists(pic_path) and self.is_valid_image(pic_path):
            if self.get_y() + 30 > 297:  # Check if adding image would overflow the page
                self.add_page()
            try:
                self.image(pic_path, x=10, y=self.get_y(), w=30, h=30)
                self.set_xy(50, self.get_y())  # Align text to the right of the image
            except Exception as e:
                print(f"Error adding profile picture: {e}")
        else:
            self.set_font('Arial', 'B', 12)
            self.cell(40, 30, 'No Profile Picture', align='L')
            self.set_xy(50, self.get_y())

    def add_user_details(self, name, email):
        self.set_text_color(0, 0, 255)  # Blue color for text
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"Name: {name} | Email: {email}", ln=True, align='C')
        self.ln(10)  # Add space after the details
        self.set_text_color(0, 0, 0)  # Reset color to black

    def add_book_section_title(self, title):
        self.set_text_color(255, 0, 0)  # Red color for section title
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(5)
        self.set_text_color(0, 0, 0)  # Reset color to black

    def add_book_cover(self, cover_path):
        current_y = self.get_y()
        if os.path.exists(cover_path) and self.is_valid_image(cover_path):
            if current_y + 45 > 297:  # Check if adding image would overflow the page
                self.add_page()
            try:
                self.image(cover_path, x=10, y=current_y, w=30, h=45)
                self.set_xy(50, current_y)  # Align text to the right of the book cover
            except Exception as e:
                print(f"Error adding book cover: {e}")
        else:
            self.set_font('Arial', 'B', 12)
            self.cell(40, 45, 'No Cover Image', align='L')
            self.set_xy(50, current_y)

    def add_book_details(self, book, is_returned_book=False):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"Title: {book['title']}", ln=True, align='C')
        
        if book.get('doi'):
            self.cell(0, 10, f"DOI: {book['doi'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        if book.get('due_date'):
            self.cell(0, 10, f"Due Date: {book['due_date'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        if book.get('request_date'):
            self.cell(0, 10, f"Request Date: {book['request_date'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        if is_returned_book and book.get('return_date'):
            self.cell(0, 10, f"Return Date: {book['return_date'].strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        
        if book.get('feedback'):
            self.cell(0, 10, f"Feedback: {book['feedback']}", ln=True, align='C')
        if book.get('rating'):
            self.cell(0, 10, f"Rating: {book['rating']}", ln=True, align='C')

        self.ln(10)  # Add space after each book entry

#generate_pdf 
def generate_pdf(activities):
    pdf = PDF()
    pdf.add_page()

    for activity in activities:
        # Add profile picture
        profile_pic_path = os.path.join('C:\\MY_PROJECTS\\MY_PROJECTS\\LMS_v2\\frontend\\src\\assets\\images', activity['profile_pic'])
        pdf.add_profile_picture(profile_pic_path)

        # Add user details
        pdf.set_xy(50, pdf.get_y())
        pdf.add_user_details(activity['name'], activity['email'])

        # Add issued books
        pdf.add_book_section_title("Issued Books")
        if activity.get('issued_books'):
            current_y = pdf.get_y()
            for book in activity['issued_books']:
                cover_path = os.path.join('C:\\MY_PROJECTS\\MY_PROJECTS\\LMS_v2\\frontend\\src\\assets\\images', book["book_img"])
                pdf.add_book_cover(cover_path)
                pdf.add_book_details(book)
                current_y = pdf.get_y() + 10  # Update current Y position for the next entry
        else:
            pdf.cell(0, 10, "None", ln=True, align='C')

        # Add requested books
        pdf.add_book_section_title("Requested Books")
        if activity.get('requested_books'):
            current_y = pdf.get_y()
            for book in activity['requested_books']:
                cover_path = os.path.join('C:\\MY_PROJECTS\\MY_PROJECTS\\LMS_v2\\frontend\\src\\assets\\images', book["book_img"])
                pdf.add_book_cover(cover_path)
                pdf.add_book_details(book)
                current_y = pdf.get_y() + 10
        else:
            pdf.cell(0, 10, "None", ln=True, align='C')

        # Add returned books
        pdf.add_book_section_title("Returned Books")
        if activity.get('returned_books'):
            current_y = pdf.get_y()
            for book in activity['returned_books']:
                cover_path = os.path.join('C:\\MY_PROJECTS\\MY_PROJECTS\\LMS_v2\\frontend\\src\\assets\\images', book["book_img"])
                pdf.add_book_cover(cover_path)
                pdf.add_book_details(book, is_returned_book=True)
                current_y = pdf.get_y() + 10
        else:
            pdf.cell(0, 10, "None", ln=True, align='C')

        pdf.ln(10)  # Add space between users

    pdf_output = pdf.output(dest='S').encode('latin1')  # Return as bytes
    return pdf_output

lib_blueprint=Blueprint("lib",__name__)


@shared_task(bind=True,base=AbortableTask)
def send_activity_report(self):
    users=User.query.all()
    activities=[]
    for user in users:
        # Get books issued by the user
        info=db.session.execute(db.Select(Book_issue).where(Book_issue.user_id==user.user_id)).scalars().all()
        # print(info)
        issued_books=[]
        returned_books=[]
        requested_books=[]
        for x in info:
            if x.doi!=None and x.re_issue==1:
                issued_books.append(x)
            elif x.return_date!=None and x.re_issue==1:
                returned_books.append(x)
            else:
                if x.re_issue==1:
                    requested_books.append(x)
                
        # print(issued_books)
        # print(requested_books)
        # print(returned_books)
                
        issued_books_list = [
            {
                "title": db.session.execute(db.Select(Book_catalogue).where(Book_catalogue.ISBN_no==issue.ISBN_no)).scalar().title,
                "doi": issue.doi,
                "due_date": issue.due_date,
                "feedback": issue.feedback,
                "rating": issue.rating,
                "request_date":None,
                "return_date":None,
                "book_img":db.session.execute(db.Select(Book_catalogue).where(Book_catalogue.ISBN_no==issue.ISBN_no)).scalar().book_img_url,
            }
            for issue in issued_books
        ]

        # Get books returned by the user
        returned_books_list = [
            {
                "title":db.session.execute(db.Select(Book_catalogue).where(Book_catalogue.ISBN_no==issue.ISBN_no)).scalar().title,
                "return_date": issue.return_date,
                "feedback": issue.feedback,
                "rating": issue.rating,
                "doi":None,
                "request_date":None,
                "book_img":db.session.execute(db.Select(Book_catalogue).where(Book_catalogue.ISBN_no==issue.ISBN_no)).scalar().book_img_url,
            }
            for issue in returned_books
        ]

        # Get books requested by the user
        requested_books_list = [
            {
                "title": db.session.execute(db.Select(Book_catalogue).where(Book_catalogue.ISBN_no==issue.ISBN_no)).scalar().title,
                "request_date": issue.request_date,
                "doi":None,
                "return_date":None,
                "book_img":db.session.execute(db.Select(Book_catalogue).where(Book_catalogue.ISBN_no==issue.ISBN_no)).scalar().book_img_url,
            }
            for issue in requested_books
        ]

        # Compile the data for the user
        user_info = {
            "name": f"{user.user_fname} {user.user_lname}",
            "profile_pic": user.profile_pic,
            "email": user.user_email,
            "issued_books": issued_books_list,
            "returned_books": returned_books_list,
            "requested_books": requested_books_list,
        }

        # Add the user's info to the activities list
        activities.append(user_info)

    pdf = generate_pdf(activities)
    send_report_email('anirudhpabbaraju1103@gmail.com', pdf)



def send_report_email(email, pdf):
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    # Create a multipart message
    msg = MIMEMultipart()
    sender = "anirudhpabbaraju1103@gmail.com"
    recipient = email
    password = 'atnipcvnvvxvcghn'

    # Set the basic email parameters
    msg['Subject'] = "Activities!"
    msg['From'] = sender
    msg['To'] = recipient

    # Attach the PDF
    part = MIMEApplication(pdf, Name="report.pdf")
    part['Content-Disposition'] = 'attachment; filename="report.pdf"'
    msg.attach(part)

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipient, msg.as_string())




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
    send_activity_report()
    return jsonify({'status': 'Report generation started!'}),200


  
