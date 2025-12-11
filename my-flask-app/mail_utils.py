from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def config_mail(flaskApp):
    flaskApp.config['MAIL_SERVER'] = 'smtp.gmail.com'
    flaskApp.config['MAIL_PORT'] = 465
    flaskApp.config['MAIL_USE_SSL'] = True
    flaskApp.config['MAIL_USERNAME'] = os.getenv("GMAIL_USER") 
    flaskApp.config['MAIL_PASSWORD'] = os.getenv("GMAIL_PW")
    flaskApp.config['MAIL_DEFAULT_SENDER'] = ('gatherup', os.getenv('GMAIL_USER'))
    mail.init_app(flaskApp)

def create_template(fromuser, category = 'updated'):
    html = f"<h2> Hello! </h2>"
    if category == 'updated':
        html += f"<p>Your friend <strong>{fromuser}</strong> has updated their schedule!</p>"
        html += "<p> Please check their schedule for the update! </p>"
    
    html += "<p>Best regards, <br> GatherUp Team </p>"

    return html

def send_gmail(fromuser, receiver, input_subject, input_body, content_html = None):
    if not receiver:
        err = "No one to send the email to"
        print(err)
        return err
    try: 
        ms = "trying to send the email to " + str(receiver)
        print(ms)
        message_string = Message(subject = input_subject, body = input_body, recipients = receiver)
        if content_html:
            message_string.html = content_html
        else:
            message_string.html = "<h2> Hello There, it looks like your friend " + str(fromuser) + " made some changes to their schedule!</h2>"

        mail.send(message_string)
        return "Sent Message"
    except Exception as ex:
        print(ex)
        return None

