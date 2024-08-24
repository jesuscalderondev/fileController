from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

class FMail:
    mail = Mail()
    sender = os.environ['MAIL_USERNAME']

    def sendMail(self, data:dict, archive=None):
        try:
            subject = data["subject"]
            recipients = data["recipients"]
            body = data["body"]
            message = Message(subject = subject, sender= os.environ["MAIL_USERNAME"], recipients=recipients)
            message.body = body

            if archive != None:
                extension = archive.filename.split(".")[-1]
                if extension in ["xlsx", "xls"]:
                    typeFile = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                elif extension in ["pdf"]:
                    typeFile = 'application/pdf'
                elif extension in ["xdoc, doc"]:
                    typeFile = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                message.attach(archive.filename, typeFile, archive.read())
                
            self.mail.send(message)
        except Exception as e:
            print(e)
            raise Exception()
        
def getWorkSpace():
    return os.environ["WORKSPACE"]

def getBackUp():
    return os.environ["BACKUP"]

mailer = FMail()

