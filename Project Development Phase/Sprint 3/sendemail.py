import smtplib
from flask import Flask
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
app=Flask(__name__)
SUBJECT = "expense tracker"
s = smtplib.SMTP('smtp.gmail.com', 587)

def sendmail(TEXT,email):
    print("sorry we cant process your candidature")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("il.shridhartp24@gmail.com", "oms@1Ram")
    message  = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    s.sendmail("il.shridhartp24@gmail.com", email, message)
    s.quit()
def sendgridmail(user,TEXT):
  
    from_email = Email("shridhartp24@gmail.com") 
    to_email = To(user) 
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain",TEXT)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    # Send an HTTP POST request to /mail/send
    response = s.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)

if __name__=="__main__":
     app.run(debug=True)

