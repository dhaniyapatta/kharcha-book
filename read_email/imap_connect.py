import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import re

class IMAPClient:
    
    def __init__(self, server, email, password):
        self.server = server
        self.email = email
        self.password = password
        self.connection = None
    
    def connect(self):
        self.connection = imaplib.IMAP4_SSL(self.server)
        self.connection.login(self.email, self.password)
        


    def fetch_emails(self, count, inbox, email_from,DATE_FROM,DATE_TO):
        self.connect()
        self.connection.select(inbox)
        email_data=[]
        status, messages = self.connection.search(None, f'FROM "{email_from}" SINCE {DATE_FROM} BEFORE {DATE_TO}')
        email_ids = messages[0].split()
        
        emails = []
        for i in email_ids:
            res, msg =self.connection.fetch(i, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    # Parse the bytes email into a message object
                    msg = email.message_from_bytes(response_part[1])
                    # Decode email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # If it's a bytes type, decode to str
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    # Decode email sender
                    from_ = msg.get("From")
                    
                    # Extract the date of the email
                    date = msg.get("Date")
                    
                    # Extract the body of the email
                    if msg.is_multipart():
                        # Iterate over email parts
                        for part in msg.walk():
                            # Extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            try:
                                # Get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                    else:
                        # Extract content type of email
                        content_type = msg.get_content_type()
                        
                        # Get the email body
                        body = msg.get_payload(decode=True).decode()

                    email_data.append({
                        "subject": subject,
                        "from": from_,
                        "body": body,
                        "date": date,
                        "txn method": "",
                        "credit_debit":"",
                        "amount":"",
                    })
        self.disconnect()
        return email_data



    def disconnect(self):
        self.connection.close()
        self.connection.logout()