import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# get credentials from .txt
with open('credentials.txt', 'r') as f:
    lines = f.read()
    email_address, email_password = lines.split('\n')


def send_text(phone_email, title, text):
    # create message
    message = MIMEMultipart()
    message['From'], message['To'], message['Subject'] = email_address, phone_email, title
    message.attach(MIMEText(text, 'plain'))
    text = message.as_string()
    # auth w/ email server using SSL, then send text
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(email_address, email_password)
        server.sendmail(email_address, phone_email, text)


def create_phone_email(phone, carrier):
    carrier_emails = {
        'att': 'txt.att.net',
        'boost_mobile': 'sms.myboostmobile.com',
        'cricket': 'mms.cricketwireless.net',
        'google_proj_fi': 'msg.fi.google.com',
        'republic': 'text.republicwireless.com',
        'sprint': 'messaging.sprintpcs.com',
        'straight_talk': 'vtext.com',
        'tmobile': 'tmomail.com',
        'ting': 'message.ting.com',
        'tracfone': 'mmst5.tracfone.com',
        'us_cellular': 'email.uscc.net',
        'verizon': 'vtext.com',
        'virgin_mobile': 'vmobl.com'
    }
    return f'{phone}@{carrier_emails[carrier]}'


def text_on_new_user(phone_email, text):
    # create message
    message = MIMEMultipart()
    message['From'], message['To'], message['Subject'] = email_address, phone_email, "Hey there!"
    message.attach(MIMEText(text, 'plain'))
    text = message.as_string()
    # auth w/ email server using SSL, then send text
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(email_address, email_password)
        server.sendmail(email_address, phone_email, text)