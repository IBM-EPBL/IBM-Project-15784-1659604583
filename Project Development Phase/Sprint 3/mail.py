import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='empire44440@gmail.com',
    to_emails='thangarajgeek@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)