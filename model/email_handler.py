# email_handler.py
import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EmailHandler:
    def __init__(self):
        self.email_account = os.getenv("EMAIL_ACCOUNT")
        self.email_password = os.getenv("EMAIL_PASSWORD")
      
       
    def fetch_code_emails(self):
      
            try:
                mail = imaplib.IMAP4_SSL("imap.gmail.com")
                mail.login(self.email_account, self.email_password)
                mail.select("inbox")
                print("Checking mail...")

                status, email_ids = mail.search(None, '(SUBJECT "Your login OTP")')
                email_ids = email_ids[0].split()


                if not email_ids:
                    print("No OTP emails found.")
                    return

                latest_email_id = email_ids[-1]  # Get the latest one
                status, data = mail.fetch(latest_email_id, "(RFC822)")

                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")

                       
                        otp_code = subject[:3]
                        #print("Extracted OTP:", otp_code)
                        
                    # Mark as read
                    mail.store(latest_email_id, "+FLAGS", "\\Seen")

                    mail.close()
                    mail.logout()
                    return otp_code

            except Exception as e:
                print("Email fetch error:", str(e))
