import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from base64 import urlsafe_b64encode
from novel_list import novels


# a list of the novel links
novel_links = {}
for novel_id in novels:
    link = 'https://www.royalroad.com/fiction/{0}'.format(novel_id)
    novel_links[novel_id] = link

# a list of all the responses obtained from opening the links
responses = {}
for novel_id in novel_links:
    response = requests.get(novel_links[novel_id], timeout=3)
    responses[novel_id] = response

# a list of the contents obtained from accessing each response
contents = {}
for novel_id in responses:
    content = BeautifulSoup(responses[novel_id].content, "html.parser")
    contents[novel_id] = content

# storing the latest chapter name for each novel ID
latest = {}
for novel_id in contents:
    chapters = ['']
    for tag in contents[novel_id].find_all(style="cursor: pointer"):
        for tag_2 in tag.find('td'):
            chapters.append(tag_2)
    length = len(chapters)
    latest[novel_id] = chapters[length-2]['href']

# reading the previous links stored in file
chap_file = open('chap_list.txt', 'r')
previous = chap_file.read().splitlines()
chap_file.close()

# comparing the previous links with the newly generated ones
# and sending the links for the new chapters, by email, to the 
# user so that they can read the newly released chapter

# creating the gmail service API and its associated functions
SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_message = urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_message.decode()}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                    .execute())
        print('Message Id: %s' % message['id'])
        return message
    except: #errors.HttpError, error
        print('An error occurred: %s' % errors)


# sending the message if not the same links    
i = 0
address = 'yasoobkhalid1@gmail.com'
for novel_id in latest:
    try:
        if previous[i] != latest[novel_id]:
            text = 'https://www.royalroad.com/' + latest[novel_id]
            subject = 'New chapter for {0}'.format(novels[novel_id])
            email = create_message(address, address, subject, text)
            send_message(service, 'me', email)  
        else:
            print('No new chapter.')
        i += 1
    except:
        print('No previous record of {0}. New record created'.format(novels[novel_id]))

# overriding the previous file to store the latest chapter links 
chap_file = open('chap_list.txt', 'w') 
for novel_id in latest:
    chap_file.write(latest[novel_id]+'\n')
chap_file.close()
