from django.core.mail import send_mail
import uuid
from django.conf import settings

# def send_forget_password_mail(email, token):
    
#     subject = 'your forget password link '
#     message = f'hi, click on the link to reset your password http://127.0.0.1:8000/change_password/{token}/'
#     from_email = 'electronshop409@gmail.com'
#     recipient_list = [email]
#     print(email)
#     print(recipient_list,"ivide ethi")
#     send_mail(subject, message, from_email, recipient_list)


import smtplib
from email.message import EmailMessage

def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    message = f'Hi, click on the link to reset your password: http://127.0.0.1:8001/reset_password/{token}/'
    from_email = 'electronshop409@gmail.com'
    recipient_list = [email]

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(recipient_list)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('electronshop409@gmail.com', 'awuftnbvslyljwys')
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)

