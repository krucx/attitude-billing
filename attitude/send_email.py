from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib

EMAIL_TO = 'takadiyas@gmail.com'
EMAIL_FROM = 'kritarth.jain11@gmail.com'
SMTP_USERNAME = 'kritarth.jain11@gmail.com'
EMAIL_SUBJECT = 'ATTITUDE SALE BOOKS'
MESSAGE_BODY = 'Please find attached'
SMTP_PASSWORD = 'cncrlrcopgxizgxc'

def send_mail():
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText(MESSAGE_BODY, 'plain')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    with open('bill_records.csv','rb') as file:
    # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=file.name))

    # Create SMTP object
    smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # Login to the server
    smtp_obj.login(SMTP_USERNAME, SMTP_PASSWORD)

    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()

#send_mail()
 