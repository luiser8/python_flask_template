import os
import smtplib
from email.message import EmailMessage
from middleware.randomCode import randomCode

class mailerSendSrv:
    def __init__(self):
        self.smtp_port = 587
        self.smtp_server = "smtp.office365.com"
        self.username = "pruebas@smartwork.com.ec"
        self.password = "wYEWvr4ZxrgWEyQb"
        self.server = EmailMessage()

    def sendSrv(self, email):
        if email:
            return randomCode().generate()
            # self.server.set_content('Message content here')
            # self.server['Subject'] = 'Your subject here'
            # self.server['From'] = self.username
            # self.server['To'] = email

            # smtp_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # smtp_server.starttls()
            # smtp_server.login(self.username, self.password)
            # smtp_server.send_message(self.server)
            # smtp_server.quit()
