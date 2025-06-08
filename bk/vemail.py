import imaplib
import email
from email.header import decode_header

# Email account credentials
username = "vasanthrrao@gmail.com"
password = "ylxc kjob sjfe bpds"  # use the app password

# Connect to Gmail IMAP server
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# Login
imap.login(username, password)

# Select the mailbox you want to use
imap.select("inbox")

# Search for all emails
status, messages = imap.search(None, 'ALL')

# Get list of email IDs
email_ids = messages[0].split()

# Fetch the latest email
latest_email_id = email_ids[-1]

# Fetch the email by ID
res, msg = imap.fetch(latest_email_id, "(RFC822)")

for response in msg:
    if isinstance(response, tuple):
        # Parse email bytes to message
        msg = email.message_from_bytes(response[1])

        # Decode subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        print("Subject:", subject)
        print("From:", msg.get("From"))

        # Extract email body
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print("Body:", body)
                    break
        else:
            body = msg.get_payload(decode=True).decode()
            print("Body:", body)

# Close and logout
imap.close()
imap.logout()
