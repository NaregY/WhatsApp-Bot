# utils.py

import logging
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Set up Twilio credentials
twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(twilio_account_sid, twilio_auth_token)
twilio_number = os.environ.get("TWILIO_NUMBER")

# Initialize Twilio client
client = Client(twilio_account_sid, twilio_auth_token)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=twilio_number,
            body=body_text,
            to=to_number
        )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")
