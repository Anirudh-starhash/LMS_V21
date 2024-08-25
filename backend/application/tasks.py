from application.worker import celery
from datetime import datetime
from application.database import db
from application.models import User,Book_catalogue,Book_issue
from PIL import Image
from fpdf import FPDF
import os,smtplib
from flask import current_app as app



#PDF class
class PDF(FPDF):
    def header(self):
        self.set_fill_color(240, 248, 255)
        self.rect(0, 0, 210, 297, 'F')
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Activity Report', 0, 1, 'C')
        self.ln(10)

    def chapter_ttle(self, title):
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

@celery.task(bind=True)
def generate_pdf(self,activities):
    try:
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
    except Exception as e:
        self.retry(exc=e)
        




@celery.task(bind=True)
def send_activity_report(self):
    try:
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

        pdf_bytes = generate_pdf.delay(activities).get(timeout=10)
        send_report_email.delay('anirudhpabbaraju1103@gmail.com', pdf_bytes)
        
    except ValueError as ve:
        # Handle ValueError specifically
        print(f"ValueError occurred: {ve}")
        app.logger.error(f"ValueError in task {self.request.id}: {ve}")
    
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        # You can also log the error or take other actions
        app.logger.error(f"Error in task {self.request.id}: {e}")
        
    finally:
        # Optional: Code that runs after try-except, regardless of success or failure
        print("Task execution finished.")

@celery.task(bind=True)
def send_report_email(email, pdf):
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    import logging
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
    try:
        # Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient, msg.as_string())
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        
@celery.task(bind=True)
def send_email(email, email_body):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    msg = MIMEMultipart()
    sender = "anirudhpabbaraju1103@gmail.com"
    recipient = email
    password = 'atnipcvnvvxvcghn'

    # Set the basic email parameters
    msg['Subject'] = "Activities!"
    msg['From'] = sender
    msg['To'] = recipient
    
    
    
    # Attach the email body as plain text
    msg.attach(MIMEText(email_body, 'plain'))

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipient, msg.as_string())
        
        
@celery.task(bind=True)
def get_activity(self,id):
    user=db.session.execute(db.Select(User).where(User.user_id==id)).scalar()
    info=db.session.execute(db.Select(Book_issue).where(Book_issue.user_id==id)).scalars().all()
    
    

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
    email_body = generate_email_body.delay(user_info).get(timeout=10)
    send_email.delay(user.user_email, email_body)

from datetime import datetime
@celery.task(bind=True)
def generate_email_body(user_info):
    user_name = user_info["name"]
    issued_books = user_info["issued_books"]
    returned_books = user_info["returned_books"]
    requested_books = user_info["requested_books"]

    # Start constructing the email body
    email_body = f"Hey {user_name},\n\n"
    email_body += "This is LMS_API_BOT sending you an email regarding your book status.\n\n"

    # Add issued books section
    if issued_books:
        email_body += "Issued Books:\n"
        for book in issued_books:
            doi_str = book["doi"].strftime('%Y-%m-%d') if book["doi"] else "N/A"
            due_date_str = book["due_date"].strftime('%Y-%m-%d') if book["due_date"] else "N/A"
            email_body += f"Title: {book['title']}\n"
            email_body += f"Date of Issue: {doi_str}\n"
            email_body += f"Due Date: {due_date_str}\n"
            email_body += f"Feedback: {book['feedback']}\n"
            email_body += f"Rating: {book['rating']}/5\n"
            email_body += f"Book Image: {book['book_img']}\n\n"

            # Check if due date is within the next 2 days
            if book["due_date"]:
                days_left = (book["due_date"].date() - datetime.now().date()).days
                if days_left in [0, 1, 2]:
                    email_body += "**You have a deadline! Please submit your book on or before the due date.**\n\n"

    # Add returned books section
    if returned_books:
        email_body += "Returned Books:\n"
        for book in returned_books:
            return_date_str = book["return_date"].strftime('%Y-%m-%d') if book["return_date"] else "N/A"
            email_body += f"Title: {book['title']}\n"
            email_body += f"Return Date: {return_date_str}\n"
            email_body += f"Feedback: {book['feedback']}\n"
            email_body += f"Rating: {book['rating']}/5\n"
            email_body += f"Book Image: {book['book_img']}\n\n"

    # Add requested books section
    if requested_books:
        email_body += "Requested Books:\n"
        for book in requested_books:
            request_date_str = book["request_date"].strftime('%Y-%m-%d') if book["request_date"] else "N/A"
            email_body += f"Title: {book['title']}\n"
            email_body += f"Request Date: {request_date_str}\n"
            email_body += f"Book Image: {book['book_img']}\n\n"

    email_body += "Best regards,\nLMS_API_BOT"

    return email_body

# sending email














