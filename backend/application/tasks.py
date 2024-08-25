from application.worker import celery
from datetime import datetime
from application.database import db
from application.models import User,Book_catalogue,Book_issue

from PIL import Image
from fpdf import FPDF
import os,smtplib


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
@celery.task()
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




@celery.task()
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

    pdf = generate_pdf(activities).delay()
    send_report_email('anirudhpabbaraju1103@gmail.com', pdf).delay()


@celery.task()
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







