import requests, os

api_key = os.environ.get('MAILGUN_API_KEY')

def send_email(recipient_email, subject, content):
    return requests.post(
    "https://api.mailgun.net/v3/sandbox5b69c279f56b4d82b74c6b5b9fc837fc.mailgun.org/messages",
    auth=("api", api_key),
    data={"from": "Excited User <igor@mrjacobs.eu>",
        "to": [recipient_email],
        "subject": subject,
        "text": content})