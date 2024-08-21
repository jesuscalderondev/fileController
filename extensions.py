from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

class FMail:
    mail = Mail()
    sender = os.environ['MAIL_USERNAME']

    def sendMessage(self, name:str, subject:str, body:str, recipients:list, response, failed):
        try:
            html_content = f"""
                            <html>
                            <body>
                                <h1>¡Hola! {name}</h1>
                                <p>{body}</p>
                                <hr>
                                <footer>Este es un correo generado de manera automática, por favor evite responder, si presenta alguna duda, por favor escriba a los canales de comunicación</footer>
                            </body>
                            </html>
                            """
            message = Message(subject, recipients, html=html_content, sender=self.sender)
            self.mail.send(message)
            return response
        except Exception as e:
            print(e)
            raise Exception(failed)

