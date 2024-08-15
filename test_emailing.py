from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64

# Path to your service account credentials JSON file
creds = service_account.Credentials.from_service_account_file(
    r'C:\Users\Joel Jones\AppData\Roaming\gspread_pandas\emailsenderthingy.json',
    scopes=['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']
)

# Connect to the Gmail API
service = build('gmail', 'v1', credentials=creds)


# Function to create a message
def create_message(sender, to, subject, message_text):
    if not sender or not to or not subject or not message_text:
        raise ValueError("All fields (sender, to, subject, message_text) must be provided and non-empty.")

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}


# Function to create a draft
def create_draft(service, user_id, message_body):
    try:
        draft = service.users().drafts().create(userId=user_id, body={'message': message_body}).execute()
        print(f"Draft ID: {draft['id']}")
        return draft
    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Error details: {error.content.decode('utf-8')}")


# Specify the email details
sender = "drinkh20bois@gmail.com"
to = "drinkh20bois@gmail.com"
subject = "Your Subject Here"
message_text = "This is a test email draft created using Gmail API."

# Create the message
message = create_message(sender, to, subject, message_text)

# Create the draft
create_draft(service, 'me', message)
