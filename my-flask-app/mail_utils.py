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


def send_gmail(fromuser, receiver, input_subject, input_body, content_hmtl = None):
    if not receiver:
        err = "No one to send the email to"
        print(err)
        return err
    try: 
        ms = "tring to send the email to " + str(receiver)
        print(ms)
        message_string = Message(subject = input_subject, body = input_body, recipients = receiver)
        if content_hmtl:
            message_string.html = content_hmtl
        else:
            message_string.html = "<h2> Hello There, it looks like your friend " + str(fromuser) + " made some changes to there schedule!</h2>"

        mail.send(message_string)
        return "Sent Message"
    except Exception as ex:
        print(ex)
        return None

