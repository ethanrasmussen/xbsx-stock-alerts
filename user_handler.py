import json
import imaplib
import email
import text_handler as th


# get credentials from .txt
with open('credentials.txt', 'r') as f:
    lines = f.read()
    email_address, password = lines.split('\n')

# continuous email listener
while True:
    # tries to read unread emails; if not present, prints "Waiting..."
    try:
        # login/authenticate via IMAP + SSL
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_address, password)
        # select main inbox
        mail.select()
        # get unread emails
        return_code, data = mail.search(None, 'UnSeen')
        # decode mail ID's and split into a list
        mail_ids = data[0].decode()
        id_list = mail_ids.split()
        # if there are 0 mail ID's (no unread emails), the script will error out
        if len(id_list) == 0:
            raise ValueError()

        # process all unread emails within list
        for id in id_list:
            print("Processing trigger...")
            # fetch email data from msg w/ matching ID
            typ, data = mail.fetch(str(id), '(RFC822)')
            # navigate email message data
            for response_part in data:
                # decode email message
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                # process subject of message
                subject: str = str(msg['subject'])
                print(f"Processed subject: {subject}")
                # process name and email address of sender
                sender = list(msg['from'].replace('>', '').split('<'))
                sender_name = sender[0]
                sender_email = sender[1]
                print(f"Processed sender: {sender_name} | {sender_email}")
                # process message body
                body = ""
                try:
                    # walk through msg and get plain text body
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            # get as bytes
                            body = part.get_payload(decode=True)
                            # convert to string
                            body: str = body.decode('utf-8')
                except:
                    pass
                print(f"Processed body: {body}")

                # check subject for trigger & execute action
                if subject == "add-user-json":
                    # read JSON log if exists
                    with open('users.json', 'r') as fp:
                        users = json.load(fp)
                    # split user details from body
                    phone, carrier, name, zipcode = body.split("|||")
                    users[phone] = {
                        'carrier': carrier,
                        'name': name,
                        'zip': zipcode
                    }
                    # update JSON
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp)
                    print("Added new user: JSON updated.")

                    # send welcome text to new user
                    # TODO: ADD FORM LINK FOR UNSUB
                    txt_msg = f"Hi {name}, welcome to the stock-checker text alert system made by Ethan! Should the item this system is tracking become in stock, you'll get a text. Please note that the system might accidentally confuse website changes as something becoming in/out of stock, so there may be the occasional false positive. If you'd like to unsubscribe from these texts, go to the link here:"
                    th.text_on_new_user(th.create_phone_email(phone, carrier), txt_msg)

                elif subject == "del-user-json":
                    # read JSON log if exists
                    with open('users.json', 'r') as fp:
                        users = json.load(fp)
                    # split user details from body
                    phone = body
                    # delete user from dict
                    users.pop(phone, None)
                    # update JSON
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp)
                    print("Removed user: JSON updated.")
    except:
        pass